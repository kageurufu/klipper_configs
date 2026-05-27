from kalico import config
from .board_pins.fysetc.party_in_the_back_2 import fysetc_party_in_the_back_2


pitb = config("mcu", canbus_uuid="c17fd7c55906")  # pitb2
fysetc_party_in_the_back_2(pitb)

config.include("../boards.d/fysetc/party_in_the_back_2.cfg")
config("board_pins", "fysetc_party_in_the_back_2", mcu="mcu")


config("temperature_sensor", "PITB", sensor_type="temperature_mcu", sensor_mcu="mcu")


AB_STEPPERS = dict(
    rotation_distance=40,
    microsteps=64,
    full_steps_per_rotation=200,
)

config(
    "stepper_x",
    step_pin="MOT2_STEP",
    dir_pin="!MOT2_DIR",
    enable_pin="!MOT2_EN",
    # endstop_pin="tmc5160_stepper_x:virtual_endstop",
    endstop_pin="toolhead:XES",
    **AB_STEPPERS,
)

config(
    "stepper_y",
    step_pin="MOT1_STEP",
    dir_pin="!MOT1_DIR",
    enable_pin="!MOT1_EN",
    # endstop_pin="tmc5160_stepper_y:virtual_endstop",
    endstop_pin="ENDSTOP_Y",
    **AB_STEPPERS,
)

AB_DRIVERS = dict(
    sense_resistor=0.075,  # PITB2
    # spi_bus: spi0a
    spi_software_mosi_pin="MOSI",
    spi_software_miso_pin="MISO",
    spi_software_sclk_pin="SCK",
    run_current=1,
)

config(
    "tmc5160",
    "stepper_x",
    cs_pin="MOT2_CS",
    diag0_pin="^!MOT2_DIAG",
    # endstop_pin="ENDSTOP_X"
    **AB_DRIVERS,
)

config(
    "tmc5160",
    "stepper_y",
    cs_pin="MOT1_CS",
    diag0_pin="^!MOT1_DIAG",
    # endstop_pin="ENDSTOP_Y"
    **AB_DRIVERS,
)
