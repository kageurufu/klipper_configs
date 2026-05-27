from kalico import Kalico, config, event_handler


config(
    "bed_mesh",
    speed=1600,
    horizontal_move_z=10,
    mesh_min="25, 10",
    mesh_max="275, 225",
    fade_start=0.6,
    fade_end=10.0,
    algorithm="bicubic",
    # probe_count="5,5",
    # probe_count='15,15',
    probe_count="30,30",
)


if False:  # Disabled

    @event_handler("klippy:ready")
    def autoload_mesh(k: Kalico):
        k.gcode.bed_mesh_profile(load="default")
