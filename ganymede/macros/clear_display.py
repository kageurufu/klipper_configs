from kalico import Kalico, gcode_macro


@gcode_macro
def clear_display(k: Kalico, delay: int = None):
    if delay:
        k.timer(delay, lambda k, _: k.gcode.display(""))
    else:
        k.gcode.display("")
