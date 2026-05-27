from kalico import Kalico, gcode_macro


@gcode_macro
def m900(kalico: Kalico, k: float):
    kalico.gcode.set_pressure_advance(advance=k)


@gcode_macro
def timelapse_take_frame(k: Kalico):
    "Do nothing"
