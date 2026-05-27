from kalico import config, Kalico, gcode_macro

# [gcode_macro LOAD_FILAMENT]
# gcode:
#   SAVE_GCODE_STATE NAME=LOAD_FILAMENT
#   M83           ; Relative extrusion
#   G1 E70 F3000  ; Load 70mm quickly
#   G1 E30 F300   ; Purge 30mm
#   RESTORE_GCODE_STATE NAME=LOAD_FILAMENT

# [gcode_macro UNLOAD_FILAMENT]
# gcode:
#   SAVE_GCODE_STATE NAME=UNLOAD_FILAMENT
#   M83           ; Relative extrusion
#   G1 E-5 F300   ; Retract 5mm slowly
#   G1 E4.5 F1200 ; Dip to remove string
#   G1 E-80 F3000 ; Fast full retract
#   RESTORE_GCODE_STATE NAME=UNLOAD_FILAMENT

# Gears to Toolhead: 21mm?
# Toolhead to Nozzle: 54mm

# Ensure save_variables is loaded
config("save_variables")

GEARS_TO_TOOLHEAD = 21
TOOLHEAD_TO_NOZZLE = 54


@gcode_macro
def load_filament(k: Kalico):
    if k.status.extruder.can_extrude:
        k.move(de=60, speed=5)  # Load
        k.move(de=5, speed=2.5)  # Prime

    else:
        k.gcode.cold_extrude(heater="extruder", enable=1)
        k.move(de=60, speed=5)  # Load
        k.gcode.cold_extrude(heater="extruder", enable=0)


@gcode_macro
def unload_filament(k: Kalico):
    if k.status.extruder.can_extrude:
        k.move(de=5, speed=5)  # Extrude to soften tip
        k.move(de=-20, speed=30)  # Retract a small amount
        k.sleep(0.8)  # Short delay to firm up the tip
        k.move(de=-50, speed=60)  # Prime

    else:
        k.gcode.cold_extrude(heater="extruder", enable=1)
        k.move(de=-65, speed=60)  # Unload
        k.gcode.cold_extrude(heater="extruder", enable=0)
