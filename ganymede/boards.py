from kalico import config

config.include("../boards.d/bigtreetech/skr_pico.cfg")
config.include("../boards.d/ldo/nitehawk-36.cfg")


pico = config("mcu", "pico", serial="/dev/serial/by-id/usb-Kalico_rp2040_pico-if00")

toolhead = config("mcu", "toolhead", serial="/dev/serial/by-id/usb-Kalico_rp2040_nitehawk-if00")

config("board_pins", "bigtreetech_skr_pico", mcu="pico")
config("board_pins", "ldo_nitehawk_36", mcu="toolhead")


config("temperature_sensor", "Pico", sensor_type="temperature_mcu", sensor_mcu="pico")
config("temperature_sensor", "Nitehawk", sensor_type="temperature_mcu", sensor_mcu="toolhead")


# Z0 Stepper - Front Left
# Z1 Stepper - Rear Left
# Z2 Stepper - Rear Right
# Z3 Stepper - Front Right

config("stepper_z", step_pin="pico:E0_STEP", dir_pin="!pico:E0_DIR", enable_pin="!pico:E0_EN")
config("stepper_z1", step_pin="pico:X_STEP", dir_pin="pico:X_DIR", enable_pin="!pico:X_EN")
config("stepper_z2", step_pin="pico:Y_STEP", dir_pin="!pico:Y_DIR", enable_pin="!pico:Y_EN")
config("stepper_z3", step_pin="pico:Z_STEP", dir_pin="pico:Z_DIR", enable_pin="!pico:Z_EN")

TMC_STEPPER_Z = dict(
    uart_pin="pico:STEPPER_UART_RX",
    tx_pin="pico:STEPPER_UART_TX",
    sense_resistor=0.110,
    run_current=0.8,
    home_current=0.4,
    interpolate=False,
    stealthchop_threshold=0,
)

config("tmc2209", "stepper_z", uart_address=3, **TMC_STEPPER_Z)
config("tmc2209", "stepper_z1", uart_address=0, **TMC_STEPPER_Z)
config("tmc2209", "stepper_z2", uart_address=2, **TMC_STEPPER_Z)
config("tmc2209", "stepper_z3", uart_address=1, **TMC_STEPPER_Z)


config("heater_bed", heater_pin="pico:HEATER_BED", sensor_pin="pico:THERMISTOR_BED")


#####################################################################
# 	Fan Control
#####################################################################

config("controller_fan", "electronics_fan", pin="pico:HE0")
config("temperature_sensor", "chamber", sensor_pin="pico:TH0")
config("fan_generic", "nevermore", pin="pico:FAN3")
config("neopixel", "chamber_lights", pin="pico:RGB")

## Toolhead

config(
    "tmc2209",
    "extruder",
    uart_pin="toolhead:UART",
    interpolate=False,
    # run_current= 0.5,    # CW2
    run_current=0.6,  # Galileo 2
    sense_resistor=0.110,
    stealthchop_threshold=0,
)

config(
    "extruder",
    step_pin="toolhead:STEP",
    dir_pin="!toolhead:DIR",
    enable_pin="!toolhead:EN",
    heater_pin="toolhead:HE",
    sensor_pin="toolhead:TH",
)

config("heater_fan", "hotend_fan", pin="toolhead:HEF")

config("fan", pin="toolhead:PCF")

config(
    "adxl345",
    "nitehawk",
    cs_pin="toolhead:ADXL_CS",
    spi_software_sclk_pin="toolhead:ADXL_CLK",
    spi_software_mosi_pin="toolhead:ADXL_MOSI",
    spi_software_miso_pin="toolhead:ADXL_MISO",
    axes_map="x,y,z",
)

config("neopixel", "stealthburner", pin="toolhead:RGB")
