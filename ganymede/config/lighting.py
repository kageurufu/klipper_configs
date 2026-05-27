from kalico import Kalico, config, gcode_macro
import colorsys

config(
    "neopixel",
    "chamber_lights",
    # dangerously_ignore_max_length: True
    chain_count="132",
    initial_RED="0",
    initial_GREEN="0",
    initial_BLUE="0",
    initial_WHITE="0.25",
    color_order="GRBW",
)


@gcode_macro
def set_all_leds(
    k: Kalico,
    led: str = "chamber_lights",
    red: float = 0.0,
    green: float = 0.0,
    blue: float = 0.0,
    white: float = 0.0,
):
    k.gcode.set_led(led=led, red=red, green=green, blue=blue, white=white, trasmit=1)


@gcode_macro
def set_led_hsi(
    k: Kalico,
    led: str,
    hue: int = 0,
    saturation: float = 0.0,
    intensity: float = 0.0,
    **params,
):
    red, green, blue = colorsys.hls_to_rgb(float(hue) / 360.0, intensity, saturation)
    white = min(red, green, blue)

    k.gcode.set_led(led=led, red=red, green=green, blue=blue, white=white, **params)
