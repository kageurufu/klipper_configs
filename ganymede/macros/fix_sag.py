from kalico import Kalico, gcode_macro


@gcode_macro
def fix_sag(k: Kalico, distance: int = 5):
    if not k.status.quad_gantry_level.applied:
        for i in range(distance):
            k.gcode.force_move(stepper="stepper_z1", distance=1, velocity=10)
            k.gcode.force_move(stepper="stepper_z2", distance=1, velocity=10)
