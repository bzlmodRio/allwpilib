import json

import jinja2


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
    if name == "halsim-ds-socket":
        return "simulation/halsim_ds_socket"
    if name == "commands-v2":
        return "commandsv2"
    if name == "wpimath_test":
        return "wpimath"
    if name == "robotpy_apriltag":
        return "apriltag"
    if name == "wpilib_drivers":
        return "drivers"
    if name == "robotpy_fields":
        return "fields"
    return name


def fixup_native_lib_name(name):
    return name.replace("_", "-")


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


def maven_dep_to_library(maven_dep, lib):
    """
    Maps a hatch-robotpy maven_lib_download entry to the allwpilib target that builds the library
    """
    if maven_dep["group_id"] == "org.wpilib.halsim":
        return f"//simulation/{maven_dep['artifact_id']}:shared/{lib}"
    raise ValueError(
        f"Unknown maven dependency {maven_dep['group_id']}:{maven_dep['artifact_id']}"
    )


def try_tomli_lookup(tomli_map, str_key, default_value=None):
    submap = tomli_map
    try:
        for key in str_key.split("."):
            submap = submap[key]
    except KeyError:
        return default_value
    return submap


def jsonify(item):
    if item is None or isinstance(item, jinja2.runtime.Undefined):
        return "None"
    return json.dumps(item)
