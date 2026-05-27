from kalico import Kalico, gcode_macro, event_handler
import typing


# fmt: off
FILAMENT_DEFAULTS = {
    ## ( density, heat capacity )  # suggested heat capacity range
    "PLA"       : ( 1.25, 2.20 ),  # 1.80 - 2.20
    "PETG"      : ( 1.27, 2.20 ),  # 1.70 - 2.20
    "PC+ABS"    : ( 1.15, 2.20 ),  # 1.50 - 2.20
    "ABS"       : ( 1.06, 2.40 ),  # 1.25 - 2.40
    "ASA"       : ( 1.07, 2.10 ),  # 1.30 - 2.10
    "PA6"       : ( 1.12, 2.50 ),  # 2.00 - 2.50
    "PA"        : ( 1.15, 2.50 ),  # 2.00 - 2.50
    "PC"        : ( 1.20, 1.90 ),  # 1.10 - 1.90
    "TPU"       : ( 1.21, 2.00 ),  # 1.50 - 2.00
    "TPU-90A"   : ( 1.15, 2.00 ),  # 1.50 - 2.00
    "TPU-95A"   : ( 1.22, 2.00 ),  # 1.50 - 2.00
    "ABS-CF"    : ( 1.11, 2.40 ),  # 1.25 - 2.40
    "ASA-CF"    : ( 1.11, 2.10 ),  # 1.30 - 2.10
    "PA6-CF"    : ( 1.19, 2.50 ),  # 2.00 - 2.50
    "PC+ABS-CF" : ( 1.22, 2.20 ),  # 1.50 - 2.20
    "PC+CF"     : ( 1.36, 1.90 ),  # 1.10 - 1.90
    "PLA-CF"    : ( 1.29, 2.20 ),  # 1.80 - 2.20
    "PETG-CF"   : ( 1.30, 2.20 ),  # 1.70 - 2.20
}
# fmt: on

str_upper = typing.Annotated[str, str.upper]


@event_handler("klippy:ready")
def _setup_defaults(k: Kalico):
    if "mpc_materials" not in k.saved_vars:
        k.saved_vars["mpc_materials"] = {}


def get_material_by_name(k: Kalico, material: str_upper) -> None | tuple[float, float]:
    if material in k.saved_vars["mpc_materials"]:
        return k.saved_vars["mpc_materials"][material]

    if material in FILAMENT_DEFAULTS:
        return FILAMENT_DEFAULTS[material]


def get_mpc_defaults(k: Kalico, heater: str = "extruder") -> tuple[float, float]:
    density = k.status.configfile.settings[heater].filament_density
    heat_capacity = k.status.configfile.settings[heater].heat_capacity

    return density, heat_capacity


@gcode_macro
def mpc_set_material(k: Kalico, material: str_upper, heater: str = "extruder"):
    "Set heater MPC parameters for a given material"

    if settings := get_material_by_name(k, material):
        density, heat_capacity = settings
        k.respond("🔥", f"Configuring {heater} MPC for {material}. {density=}, {heat_capacity=}")

    else:
        density, heat_capacity = get_mpc_defaults(k)
        k.respond("🔥", f"Unknown material {material!r}, using {heater} defaults")

    k.gcode.mpc_set(heater=heater, filament_density=density, filament_heat_capacity=heat_capacity)


@gcode_macro
def mpc_query_material(k: Kalico, material: str_upper):
    "Get the defined density and heat capacity for a material."

    if settings := get_material_by_name(k, material):
        (density, heat_capacity) = settings
        k.respond_info(f"Material {material}: {density=}, {heat_capacity=}")

    else:
        k.respond_info(f"Material {material} not found")


@gcode_macro
def mpc_update_material(k: Kalico, material: str_upper, density: float, heat_capacity: float):
    "Change the saved density and heat capacity for a named material"

    k.saved_vars["mpc_materials"][material] = (density, heat_capacity)
    k.respond("💾", f"New MPC parameters for {material} saved")


@gcode_macro
def mpc_reset_material(k: Kalico, material: str_upper, density: float, heat_capacity: float):
    "Clear any user saved configuration for a material"

    if material not in k.saved_vars["mpc_materials"]:
        k.respond("❔", f"Material {material} has no saved settings to clear")
        return

    density, heat_capacity = k.saved_vars["mpc_materials"].pop(material)

    if material in FILAMENT_DEFAULTS:
        k.respond("🔥", f"Material {material} reverted to default settings")

    else:
        k.respond("⚠️", f"Material {material} removed with no default. Previous values {density=} {heat_capacity=}")
