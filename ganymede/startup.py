from kalico import Kalico, event_handler


@event_handler("klippy:ready")
def on_ready(k: Kalico):
    k.respond("💜", "Starting V2.1112 :: Ganymede")

    k.gcode.set_led_template(
        led="stealthburner", index=1, template="stealthburner_logo"
    )
    k.gcode.set_led_template(
        led="stealthburner", index=2, template="stealthburner_nozzle"
    )
    k.gcode.set_led_template(
        led="stealthburner", index=3, template="stealthburner_nozzle"
    )
