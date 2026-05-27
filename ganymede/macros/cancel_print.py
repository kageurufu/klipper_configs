from kalico import Kalico, gcode_macro


@gcode_macro(rename_existing="BASE_CANCEL_PRINT")
def cancel_print(k: Kalico):
    k.gcode.clear_pause()
    k.gcode.print_end()
    k.gcode.base_cancel_print()
