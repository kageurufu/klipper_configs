from kalico import config


config(
    "danger_options",
    allow_plugin_override=True,
    log_statistics=False,
    # log_bed_mesh_on_startup=False,
    log_velocity_limit_changes=False,
    log_pressure_advance_changes=False,
)
