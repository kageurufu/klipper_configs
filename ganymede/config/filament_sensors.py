"""
[save_variables]

[filament_switch_sensor Entry]
switch_pin: !toolhead:FS
pause_on_runout: False
runout_distance: 0
debounce_delay: 0.5
# runout_gcode:
#   RESPOND PREFIX=⚠️ MSG="Entry: Filament not detected"
insert_gcode:
  # RESPOND PREFIX=✅ MSG="Entry: Filament detected"
  {% if not printer['filament_switch_sensor Toolhead'].filament_detected %}
    {% if printer.print_stats.state not in ('printing', 'paused', 'error') %}
      AUTOLOAD_FILAMENT
    {% endif %}
  {% endif %}

[filament_switch_sensor Toolhead]
switch_pin: !toolhead:PROBE
check_on_print_start: True
pause_on_runout: False
debounce_delay: 0.5
# runout_gcode:
#   RESPOND PREFIX=⚠️ MSG="Toolhead: Filament not detected"
# insert_gcode:
#   RESPOND PREFIX=✅ MSG="Toolhead: Filament detected"

[filament_motion_sensor Motion]
switch_pin: pico:gpio16
extruder: extruder
encoder_ppr: 20
encoder_radius: 5. # mm
detection_length: 4.0
pause_on_runout: True
smart: True
runout_gcode:
  RESPOND TYPE=error MSG="Filament stalled!"

[filament_switch_sensor Presence]
switch_pin: ^!pico:gpio29
pause_on_runout: False
runout_distance: 1200
smart: True
immediate_runout_gcode:
    SET_FILAMENT_SENSOR SENSOR=Motion ENABLE=0
    RESPOND TYPE=error MSG="End of filament detected!"
    RESPOND MSG="Printer will runout in {printer.configfile.settings['filament_switch_sensor Presence'].runout_distance}mm"
runout_gcode:
    PAUSE
    RESPOND TYPE=error MSG="Ran out of filament"
    RESPOND MSG="Printer paused until filament inserted"
insert_gcode:
    SET_FILAMENT_SENSOR SENSOR=Motion RESET=1 ENABLE=1
    RESPOND TYPE=command MSG="Filament detected at Presence"

[delayed_gcode _fs_startup]
initial_duration: 0.1
gcode:
    {% set fss_detected = printer['filament_switch_sensor Presence'].filament_detected %}
    SET_FILAMENT_SENSOR SENSOR=Motion ENABLE={1 if fss_detected else 0}

# print_stats.state: standby -> printing, paused -> error, complete, cancelled
# idle_timeout.state: Idle, Printing, Ready
# virtual_sdcard: is_active

[gcode_macro AUTOLOAD_FILAMENT]
gcode:
  UPDATE_DELAYED_GCODE ID=__autoload_filament DURATION=0.01

[delayed_gcode __autoload_filament]
gcode:
  {% if printer.print_stats.state not in ('printing', 'paused', 'error') %}
    M83
    COLD_EXTRUDE HEATER=extruder ENABLE=1
    {% if not printer['filament_switch_sensor Toolhead'].filament_detected %}
      # Load filament until it hits the toolhead sensor
      UPDATE_DELAYED_GCODE ID=__autoload_filament DURATION=0.2
      G0 E1 F300
    {% else %}
      # Feed to the nozzle
      G0 E40 F300
      COLD_EXTRUDE HEATER=extruder ENABLE=0
    {% endif %}
  {% endif %}
"""

from kalico import Kalico, config, gcode_macro, event_handler

ACTIVE_PAUSE_STATES = ("printing", "paused", "error")

fs_entry = config(
    "filament_switch_sensor",
    "Entry",
    switch_pin="!toolhead:FS",
    pause_on_runout=False,
    runout_distance=0,
    debounce_delay=0.5,
    runout_gcode=lambda k: k.respond("⚠️", "Entry: Filament not detected"),
)


@fs_entry.gcode("insert_gcode")
def fs_entry_insert(k: Kalico):
    if not k.status[fs_toolhead.section].filament_detected:
        if k.status.print_stats.state not in ACTIVE_PAUSE_STATES:
            autoload_filament(k)


fs_toolhead = config(
    "filament_switch_sensor",
    "Toolhead",
    switch_pin="!toolhead:PROBE",
    check_on_print_start=True,
    pause_on_runout=False,
    debounce_delay=0.5,
    # runout_gcode=lambda k: k.respond("⚠️", "Toolhead: Filament not detected"),
    # insert_gcode=lambda k: k.respond("✅", "Toolhead: Filament detected"),
)

fs_motion = config(
    "filament_motion_sensor",
    "Motion",
    switch_pin="pico:gpio16",
    extruder="extruder",
    encoder_ppr=20,
    encoder_radius=5.0,  # mm
    detection_length=4.0,
    pause_on_runout=True,
    smart=True,
)


@fs_motion.gcode("runout_gcode")
def fs_motion_runout(k: Kalico):
    k.respond("!!", "Filament stalled!")


fs_presence = config(
    "filament_switch_sensor",
    "Presence",
    switch_pin="^!pico:gpio29",
    pause_on_runout=False,
    runout_distance=1200,
    smart=True,
)


@fs_presence.gcode("immediate_runout_gcode")
def fs_presence_immediate_runout_gcode(k: Kalico):
    k.gcode.set_filament_sensor(sensor="Motion", enable=0)
    k.respond("!!", "End of filament detected!")
    k.respond_info(f"Printer will runout in {fs_presence.get('runout_distance')}mm")


@fs_presence.gcode("runout_gcode")
def fs_presence_runout_gcode(k: Kalico):
    k.gcode.pause()
    k.respond("!!", "Ran out of filament")
    k.respond_info("Printer paused until filament inserted")


@fs_presence.gcode("insert_gcode")
def fs_presence_insert_gcode(k: Kalico):
    k.gcode.set_filament_sensor(sensor="Motion", reset=1, enable=1)
    k.respond_info("Filament detected at Presence")


@event_handler("klippy:ready")
def _fs_startup(k: Kalico):
    k.gcode.set_filament_sensor(
        sensor="Motion",
        enable=int(k.status[fs_presence.section].filament_detected),
    )


# print_stats.state: standby -> printing, paused -> error, complete, cancelled
# idle_timeout.state: Idle, Printing, Ready
# virtual_sdcard: is_active


@gcode_macro
def autoload_filament(k: Kalico):
    if k.status.print_stats.state in ACTIVE_PAUSE_STATES:
        return

    k.gcode.cold_extrude(heater="extruder", enable=1)
    while not k.status[fs_toolhead.section].filament_detected:
        k.move(de=1, speed=10)
    k.move(de=40, speed=10)
    k.gcode.cold_extrude(heater="extruder", enable=0)
