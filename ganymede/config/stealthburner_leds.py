from kalico import Kalico, event_handler, config

config("neopixel", "stealthburner", chain_count=3, color_order="GRBW")

config(
    "display_template",
    "stealthburner_logo",
    text="0.2, 0, 0.2, 0",
)

config(
    "display_template",
    "stealthburner_nozzle",
    text="""
        {% if printer.idle_timeout.state == 'Printing' %}
            0, 0, 0, 0.6
        {% else %}
            {% set red = ((100.0 / (printer['extruder'].temperature - 100), 0.0) | max, 1.0) | min%}
            {red}, 0, 0, 0.2
        {% endif %}
    """,
)

config(
    "display_template",
    "chamber_lights",
    text="""
        {% if printer.idle_timeout.state == 'Printing' %}
            0, 0, 0, 0.6
        {% elif printer.idle_timeout.state == 'Ready' %}
            0, 0, 0, 0.3
        {% else %}
            0, 0, 0, 0.1
        {% endif %}
    """,
)


@event_handler("klippy:ready")
def on_ready(k: Kalico):
    k.gcode.set_led_template(led="stealthburner", index=1, template="stealthburner_logo")
    k.gcode.set_led_template(led="stealthburner", index=2, template="stealthburner_nozzle")
    k.gcode.set_led_template(led="stealthburner", index=3, template="stealthburner_nozzle")
