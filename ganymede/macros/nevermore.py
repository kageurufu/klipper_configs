from kalico import Kalico, gcode_macro


@gcode_macro
def air_filter_start(k: Kalico, speed: float = 0.6):
    k.fans.set_speed("nevermore", speed)


@gcode_macro
def air_filter_stop(k: Kalico, delay: float = None):
    def callback(k: Kalico, _=None):
        k.fans.set_speed("nevermore", 0)

    if delay:
        k.timer(delay, callback)
    else:
        callback(k)
