from kalico import Kalico, gcode_macro

from .squiggly_purge import squiggly_purge
from .mpc import mpc_set_material


EXTRUDER_LOW = 150


@gcode_macro
def print_start(
    k: Kalico,
    extruder: float,
    material: str,
    bed: float = 0.0,
    chamber: float = 0.0,
):
    mpc_set_material(k, material=material)
    k.heaters.set_temperature("extruder", EXTRUDER_LOW)
    k.heaters.set_temperature("heater_bed", bed)

    k.gcode.absolute_movement()
    k.move.set_gcode_offset(z=0)

    k.gcode.bed_mesh_clear()
    k.gcode.g28()
    k.move(x=150, y=150, z=20, speed=200)

    if bed:
        k.gcode.display(f"🔥 Waiting for bed {int(bed)}C")
        k.heaters.temperature_wait("heater_bed", min_temp=bed - 1)

    if chamber:
        preheat_chamber(k, chamber)

    if "abs" in material.lower() or "asa" in material.lower():
        k.fans.set_speed("nevermore", 0.6)

    if abs(EXTRUDER_LOW - k.status.extruder.temperature) > 5:
        k.gcode.display(f"🔥 Waiting for extruder {EXTRUDER_LOW}C")
        k.heaters.temperature_wait("extruder", min_temp=EXTRUDER_LOW - 5, max_temp=EXTRUDER_LOW + 5)

    k.gcode.g28("Z", method="contact", calibrate=1)

    k.gcode.display("🎚️ Quad Gantry Level")
    k.gcode.quad_gantry_level()

    k.gcode.display("🎚️ Adaptive Meshing")
    k.gcode.bed_mesh_calibrate(adaptive=True)

    k.gcode.g28("Z", method="contact", calibrate=False)

    k.gcode.display(f"🔥 Waiting for extruder {int(extruder)}C")
    k.heaters.set_temperature("extruder", extruder, wait=True)

    k.gcode.display("💩 Purging")
    squiggly_purge(k)

    k.gcode.display("🏁 Print Starting")
    k.timer(10.0, lambda k, _: k.gcode.clear_display())

    k.gcode.relative_extrusion()
    k.gcode.g92(e=0)
    k.move.set_speed(200)


@gcode_macro
def preheat_chamber(
    k: Kalico,
    chamber: float,
    bed: float = None,
):
    if bed:
        k.heaters.set_temperature("heater_bed", bed)
    else:
        if not k.status.heater_bed.target:
            raise k.raise_error("Cannot preheat the chamber with a cold bed")

    if "xyz" not in k.status.toolhead.homed_axes:
        k.gcode.g28()

    k.move(x=150, y=150, z=20, speed=200)

    if not k.status.extruder.target:
        k.heaters.set_temperature("extruder", 1)
    k.fans.set_speed("fan", 1)

    if chamber:
        previous_speed = k.status["fan_generic nevermore"].speed
        k.fans.set_speed("nevermore", 1.0)
        k.gcode.display(f"🔥 Waiting for chamber {int(chamber)}C")
        k.heaters.temperature_wait("temperature_sensor chamber", min_temp=chamber)
        k.fans.set_speed("nevermore", previous_speed)
