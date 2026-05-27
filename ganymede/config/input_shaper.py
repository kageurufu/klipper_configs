from kalico import config


config("printer", max_accel=8800)
config(
    "input_shaper",
    shaper_freq_x=49.2,
    shaper_type_x="ei",
    # damping_ratio_x=0.1,
    shaper_freq_y=41.2,
    shaper_type_y="mzv",
    # damping_ratio_y=0.1,
)
