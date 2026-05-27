from kalico import Kalico, gcode_macro


def save_status(k: Kalico):
    resume.vars.extruder_target = k.status.extruder.target
    resume.vars.bed_target = k.status.heater_bed.target
    resume.vars.fan = k.status.fan.speed

    k.gcode.save_gcode_state(name="pause")


def restore_status(k: Kalico):
    if k.status.heater_bed.target != resume.vars.bed_target:
        k.gcode.display(f"🔥 Restoring bed to {int(resume.vars.bed_target)}C")
        k.heaters.set_temperature("heater_bed", resume.vars.bed_target, wait=True)

    if k.status.extruder.target != resume.vars.extruder_target:
        k.gcode.display(f"🔥 Restoring extruder to {int(resume.vars.extruder_target)}C")
        k.heaters.set_temperature("extruder", resume.vars.extruder_target, wait=True)

    k.fans.set_speed("fan", k.status.fan.speed)
    k.gcode.restore_gcode_state(name="pause", move=True)


@gcode_macro(rename_existing="BASE_PAUSE")
def pause(k: Kalico):
    k.gcode.push_notification(
        title="Ganymede Paused",
        body=f"{k.status.virtual_sdcard.progress}% of {k.status.virtual_sdcard.file_path}",
    )

    save_status(k)
    k.gcode.base_pause()

    if k.status.extruder.can_extrude:
        k.move(de=-1, speed=35)
    k.gcode.park_toolhead(location="REAR")


@gcode_macro
def m600(k: Kalico, next_color: str = "unknown"):
    k.gcode.push_notification(
        title="Ganymede Paused",
        body=f"Filament change required, next color is {next_color}",
    )

    save_status(k)
    k.gcode.base_pause()

    if k.status.extruder.can_extrude:
        k.move(de=-1, speed=35)

    k.gcode.park_toolhead(location="FRONT")


@gcode_macro(rename_existing="BASE_RESUME")
def resume(k: Kalico):
    restore_status(k)
    k.gcode.base_resume()
    k.gcode.clear_display()
