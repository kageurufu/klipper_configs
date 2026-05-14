from kalico import Kalico, gcode_macro


@gcode_macro
def present(k: Kalico):
    if "xyz" not in k.status.toolhead.homed_axes:
        k.gcode.g28()

    k.move(
        x=150,
        y=0,
        z=k.status.toolhead.axis_maximum.z / 2,
        speed=200,
    )
