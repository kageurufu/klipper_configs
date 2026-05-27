from kalico import Kalico, gcode_macro
import math
import itertools
import enum


class Direction(enum.Enum):
    X = "X"
    Y = "Y"


FACTORIALS = [1, 2, 24, 720, 40320, 3628800, 479001600, 87178291200, 20922789888000]


@gcode_macro
def squiggly_purge(
    k: Kalico,
    # Commonly adjusted
    purge_length: float = 100.0,
    periods: int = 10,
    line_height: float = 0.6,
    line_direction: Direction = Direction.X,
    start_x: float = 5.0,
    start_y: float = 3.5,
    # Occasionally adjusted
    flowrate: float = 10.0,
    amplitude: float = 5.0,
    period_length: float = 5.0,
    line_margin: float = 10.0,
    # Rarely changed
    steps: int = 16,
    unretract_length: float = 5.0,
    adaptive_mode: bool = True,
    verbose: bool = True,
    # For prusaslicer, `SIZE={first_layer_print_min[0]}_{first_layer_print_min[1]}_{first_layer_print_max[0]}_{first_layer_print_max[1]}`
    size: str = None,
):
    """
    Draw a sinusoidal purge line
    """

    coordinates_found = False
    xMinSpec, yMinSpec, xMaxSpec, yMaxSpec = 0, 0, 0, 0

    if size and size != "0_0_0_0":
        xMinSpec, yMinSpec, xMaxSpec, yMaxSpec = [float(c.strip()) for c in size.split("_")]
        coordinates_found = True

    elif k.status.exclude_object and k.status.exclude_object.objects:
        points = [point for obj in k.status.exclude_object.objects for point in obj["polygon"]]
        xMinSpec = min(point[0] for point in points)
        yMinSpec = min(point[1] for point in points)
        xMaxSpec = max(point[0] for point in points)
        yMaxSpec = max(point[1] for point in points)
        coordinates_found = True

    prime_line_x = start_x
    prime_line_y = start_y
    center_x = k.status.toolhead.axis_maximum.x / 2
    center_y = k.status.toolhead.axis_maximum.y / 2

    if line_direction == Direction.X:
        offset_x, offset_y = 0, amplitude / 2
    else:
        offset_x, offset_y = amplitude / 2, 0

    if coordinates_found and adaptive_mode:
        prime_line_x = (
            2 * center_x - prime_line_x
            if (prime_line_x > center_x and xMinSpec < center_x) or (prime_line_x < center_x and xMinSpec > center_x)
            else prime_line_x
        )
        prime_line_y = (
            2 * center_y - prime_line_y
            if (prime_line_y > center_y and yMaxSpec < center_y) or (prime_line_y < center_y and yMinSpec > center_y)
            else prime_line_y
        )
        prime_line_x = min(max(prime_line_x, xMinSpec - line_margin - offset_x), xMaxSpec + line_margin + offset_x)
        prime_line_y = min(max(prime_line_y, yMinSpec - line_margin - offset_y), yMaxSpec + line_margin + offset_y)

    prime_line_way = 1
    if (line_direction == Direction.X and prime_line_x > center_x) or (
        line_direction == Direction.Y and prime_line_y > center_y
    ):
        prime_line_way = -1

    extrusion_steps = []
    cur_y = prime_line_y
    prime_line_length = 0.0
    cos = 0.0

    for step in range(1, periods * steps + 1):
        sign = itertools.cycle([1.0, -1.0])
        cos = 0.0
        rad_angle = step / steps * math.tau

        for i, factorial in enumerate(FACTORIALS):
            cos_step = next(sign) * ((rad_angle % math.tau) ** (2 * i) / factorial)
            cos += cos_step

        # dist_x = step * period_length / steps
        dist_y = amplitude * (0.5 - (0.5 * cos))
        rel_x = period_length / steps
        rel_y = prime_line_y + dist_y - cur_y
        e_length = (rel_x**2 + rel_y**2) ** 0.5
        cur_y += rel_y
        prime_line_length += e_length

        extrusion_steps.append((rel_x, rel_y, e_length))

    max_extrude_cross_section = float(k.status.configfile.settings.extruder.max_extrude_cross_section)
    filament_diameter = float(k.status.configfile.settings.extruder.filament_diameter)
    filament_area = math.pi * (filament_diameter / 2) ** 2

    purge_volume = purge_length * filament_area
    line_width = purge_volume / (line_height * prime_line_length)

    if line_height * line_width > max_extrude_cross_section:
        if verbose:
            k.respond_info(
                f"The purge_length of {purge_length:.4f} mm is too high and will exceed the max_extrude_cross_section!"
            )
        purge_length = 0.98 * (max_extrude_cross_section * prime_line_length) / filament_area
        purge_volume = purge_length * filament_area
        line_width = purge_volume / (line_height * prime_line_length)

        if verbose:
            k.respond_info(f"Corrected purge_length to {purge_length:.4f} mm")

    if (line_height / line_width) >= 0.5:
        k.raise_error(
            f"The prime line will be too thin {line_height:.4f} x {line_width:.4f} and will probably not stick properly to the bed. Increase its purge distance or decrease its length!"
        )

    speed = flowrate / (line_height * line_width)

    if k.status.toolhead.position.z < 5:
        k.move(z=5, speed=10)

    # Starting position
    k.move(x=prime_line_x, y=prime_line_y, speed=300)

    # Add some squish to the line
    k.move(z=line_height * 0.8, speed=10)

    # Add pressure in the nozzle
    k.move(de=unretract_length, speed=5)

    # Prime line
    for x, y, e in extrusion_steps:
        if line_direction == "Y":
            x, y = y, x
        k.move(dx=x * prime_line_way, dy=y, de=e / prime_line_length * purge_length, speed=speed)

    # Retract and Z-hop
    k.move(de=-0.2, speed=35)
    k.move(z=3, speed=60)

    # Additional small movement to get out of the line as some slicers directly emmit
    # a Z- move as a first step that make the toolhead crash back in the line and get dirty
    k.move(dx=5, dy=5, speed=300)

    # Flushing Kalico's buffer to ensure the primeline sequence is done before continuing
    k.wait_moves()
