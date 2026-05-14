from kalico import Kalico, gcode_macro


@gcode_macro(rename_existing="BASE_CANCEL_PRINT")
def cancel_print(k: Kalico):
    k.gcode.CLEAR_PAUSE()
    k.gcode.PRINT_END()
    k.gcode.BASE_CANCEL_PRINT()
