from kalico import config

config(
    "beacon",
    serial="/dev/serial/by-id/usb-Beacon_Beacon_RevH_E4F721055154354D38202020FF0A080F-if00",
    x_offset=0,
    y_offset=-21.953,
    mesh_main_direction="x",
    mesh_runs=2,
    home_xy_position="150, 150",
    home_z_hop=5,
    contact_max_hotend_temperature=180,
    # home_method: contact
    accel_axes_map="-x, -y, z",
)

config(
    "stepper_z",
    endstop_pin="probe:z_virtual_endstop",
    homing_retract_dist=0,
)

config(
    "resonance_tester",
    accel_chip="beacon",
    probe_points="150,150,50",
)
