from kalico import Kalico, gcode_macro
from .nevermore import air_filter_stop


@gcode_macro
def _retract_and_lift(k: Kalico, retract: bool = True):
    center_x = (k.status.toolhead.axis_maximum.x - k.status.toolhead.axis_minimum.x) / 2
    center_y = (k.status.toolhead.axis_maximum.y - k.status.toolhead.axis_minimum.y) / 2
    dx = 20 if k.status.toolhead.position.x < center_x else -20
    dy = 20 if k.status.toolhead.position.y < center_y else -20

    if retract:
        k.move(de=-5, speed=60)
    k.move(dx=dx, dy=dy, dz=-0.4, speed=200)
    if retract:
        k.move(de=-25.0, speed=60)


@gcode_macro
def print_end(k: Kalico):
    k.gcode("G92 E0")  # TODO: Is this needed?
    _retract_and_lift(k)

    k.wait_moves()  # M400
    k.heaters.turn_off()
    k.fans.set_speed("fan", 0)

    # Park the toolhead
    if k.status.toolhead.position.z < k.status.toolhead.axis_maximum.z - 10:
        k.move(
            z=min(
                k.status.toolhead.position.z + 5, k.status.toolhead.axis_maximum.z - 10
            ),
            speed=90,
        )
    k.move(
        x=k.status.toolhead.axis_maximum.x - 20,
        y=k.status.toolhead.axis_maximum.y,
        speed=300,
    )

    k.gcode.push_notification(
        title="Print Complete", body=f"{k.status.virtual_sdcard.file_path}"
    )

    air_filter_stop(k, delay=300)
