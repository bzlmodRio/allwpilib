def fixup_root_package_name(name):
    if name == "wpihal":
        return "hal"
    if name == "wpilib":
        return "wpilibc"
    if name == "wpilog":
        return "datalog"
    if name == "xrp":
        return "xrpVendordep"
    if name == "romi":
        return "romiVendordep"
    if name == "pyntcore":
        return "ntcore"
    if name == "halsim-ws":
        return "simulation/halsim_ws_core"
    if name == "halsim_gui":
        return "simulation/halsim_gui"
    if name == "halsim_ds_socket":
        return "simulation/halsim_ds_socket"
    if name == "wpimath_test":
        return "wpimath"
    if name == "robotpy_apriltag":
        return "apriltag"
    if name == "robotpy_fields":
        return "fields"
    if name == "commands2":
        return "commandsv2"
    return name


def fixup_native_lib_name(name):
    return name


def fixup_native_package_name(name):
    return f"{fixup_root_package_name(name)}"


def fixup_python_package_name(name):
    return f"{fixup_root_package_name(name)}"


def fixup_shared_lib_name(name):
    if name == "wpihal":
        return "wpiHal"
    if name == "hal":
        return "wpiHal"
    if name == "wpilib":
        return "wpilibc"
    if name == "xrp":
        return "xrpVendordep"
    if name == "romi":
        return "romiVendordep"
    return name


def fixup_python_dep_name(name):
    if name == "robotpy-datalog":
        return "robotpy-wpilog"
    if name == "robotpy-ntcore":
        return "pyntcore"
    if name == "wpilib":
        return "robotpy-wpilib"
    return name


def try_tomli_lookup(tomli_map, str_key, default_value=None):
    keys = str_key.split(".")
    submap = tomli_map

    try:
        for key in keys:
            submap = submap[key]
    except KeyError:
        return default_value

    return submap