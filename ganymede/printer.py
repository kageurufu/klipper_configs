from kalico import config


config(
    "printer",
    kinematics="corexy",
    max_velocity=500,
    max_accel=6000,  # Max 4000
    max_z_velocity=30,  # Max 15 for 12V TMC Drivers, can increase for 24V
    max_z_accel=600,
    square_corner_velocity=5.0,
)


#####################################################################
# XY Stepper Settings
#####################################################################

config(
    "stepper_x",
    # rotation_distance=40,
    # microsteps=16,
    # full_steps_per_rotation=200,  #set to 400 for 0.9 degree stepper
    position_min=0,
    position_endstop=305,
    position_max=305,
    homing_speed=40,
    # second_homing_speed= 40,
    # homing_retract_dist= 20,
)

config(
    "stepper_y",
    # rotation_distance=40,
    # microsteps=16,
    # full_steps_per_rotation=200,  #set to 400 for 0.9 degree stepper
    position_min=0,
    position_endstop=305,
    position_max=305,
    homing_speed=40,
    # second_homing_speed=40,
    # homing_retract_dist=20,
    # homing_positive_dir=True,
)


#####################################################################
# Z Stepper Settings
#   Z0 - Front Left
# Z1 - Rear Left
# Z2 - Rear Right
# Z3 - Front Right
#####################################################################

Z_STEPPER = dict(
    rotation_distance=40,
    gear_ratio="80:16",
    microsteps=128,
)

config(
    "stepper_z",
    position_max=290,
    position_min=-5,
    homing_speed=15,
    second_homing_speed=3,
    homing_retract_dist=3,
    **Z_STEPPER,
)

config("stepper_z1", **Z_STEPPER)
config("stepper_z2", **Z_STEPPER)
config("stepper_z3", **Z_STEPPER)


config("autotune_tmc", "stepper_z", motor="omc-17hs19-2004s1")
config("autotune_tmc", "stepper_z1", motor="omc-17hs19-2004s1")
config("autotune_tmc", "stepper_z2", motor="omc-17hs19-2004s1")
config("autotune_tmc", "stepper_z3", motor="omc-17hs19-2004s1")


#####################################################################
# 	Extruder
#####################################################################

# E0 on toolhead


## Afterburner / Clockwork
# rotation_distance: 22.3818568406	# Bondtech 5mm Drive Gears
# gear_ratio: 50:17				    # BMG Gear Ratio
## Clockwork 2
# rotation_distance: 22.6789511
# gear_ratio: 50:10
# microsteps: 32
# full_steps_per_rotation: 200

## LGX Lite
# rotation_distance: 5.7 # 200 * 16 / 562
# full_steps_per_rotation: 200	#200 for 1.8 degree, 400 for 0.9 degree
# microsteps: 16
# gear_ratio: 20:10  # ?

config(
    "extruder",
    ## Galileo 2
    rotation_distance=47.088,
    gear_ratio="9:1",
    microsteps=16,
    nozzle_diameter=0.400,
    filament_diameter=1.75,
    sensor_type="PT1000",
    pullup_resistor=2200,
    min_temp=0,
    max_temp=380,
    max_power=1.0,
    min_extrude_temp=170,
    ##	Try to keep pressure_advance below 1.0
    pressure_advance=0.046,
    ##	Default is 0.040, leave stock
    pressure_advance_smooth_time=0.040,
    max_extrude_only_distance=100,
    max_extrude_cross_section=100,
    # control: mpc
    # heater_voltage: 24
    # heater_power: 88.6
    # heater_power_ambient: 23
    # heater_temperature_coefficient: 0.003131
    # heater_power_1: 28.8
    # heater_temperature_1: 200
    # heater_power_2: 24
    # heater_temperature_2: 265
    ## Rapido 1
    # heater_power_1: 52
    # heater_temperature_1: 180
    # heater_power_2: 46
    # heater_temperature_2: 300
    heater_power=70,
    cooling_fan="fan",
    ambient_temp_sensor="temperature_sensor chamber",
    filament_density=1.2,
    filament_heat_capacity=1.8,
    # Calibrated
)


config(
    "heater_bed",
    sensor_type="Generic 3950",
    max_power=1,
    min_temp=0,
    max_temp=130,
    # control = mpc
    # block_heat_capacity = 1007.53
    # sensor_responsiveness = 0.0220942
    # ambient_transfer = 8.39470
    # fan_ambient_transfer = 8.3947, 7.46411, 8.41315, 7.90361, 6.70618
    # heater_power: 750
    # cooling_fan: fan_generic nevermore
    # ambient_temp_sensor: temperature_sensor chamber
    control="pid",
    pid_kp=61.129,
    pid_ki=3.570,
    pid_kd=261.710,
    pid_version=1,
    pid_target=115.00,
    pid_tolerance=0.0200,
)


config(
    "heater_fan",
    "hotend_fan",
    max_power=1.0,
    kick_start_time=0.5,
    heater="extruder",
    heater_temp=50.0,
    ##	If you are experiencing back flow, you can reduce fan_speed
    fan_speed=0.8,
)


config(
    "fan",
    kick_start_time=0.5,
    ##	Depending on your fan, you may need to increase this value
    ##	if your fan will not start. Can change cycle_time (increase)
    ##	if your fan is not able to slow down effectively
    # off_below=0.10,
)

config(
    "controller_fan",
    "electronics_fan",
    max_power=0.8,
    fan_speed=0.4,
)


config("fan_generic", "nevermore")
config("temperature_sensor", "chamber", sensor_type="ATC Semitec 104GT-2")

# Some required extras
config("display_status")
config("exclude_object")
config("force_move", enable_force_move=True)
config("gcode_arcs", resolution=0.05)
config("pause_resume")
config("respond")
config("virtual_sdcard", path="~/printer_data/gcodes")


##
## [extruder]
## control = pid
## pid_kp = 20.379
## pid_ki = 1.691
## pid_kd = 61.392
## pid_version = 1
## pid_target = 260.00
## pid_tolerance = 0.0200

# [probe]
# z_offset = -0.350
