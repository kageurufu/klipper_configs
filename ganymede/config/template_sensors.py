from kalico import config


config("temperature_sensor_template")
config(
    "temperature_sensor",
    "extruder_block",
    sensor_type="template",
    template="{printer.extruder.control_stats.temp_block}",
)
