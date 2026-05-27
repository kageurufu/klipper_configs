from kalico import config, Kalico


idle = config("idle_timeout", timeout=3600)


@idle.gcode("gcode")
def idle_timeout_gcode(k: Kalico):
    if k.status.pause_resume.is_paused:
        k.heaters.set_temperature("extruder", 150)
    else:
        k.heaters.turn_off()

    k.fans.set_speed("fan", 0)
