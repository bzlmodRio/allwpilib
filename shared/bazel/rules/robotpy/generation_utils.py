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
        return "simulation/halsim_ws_core/src/main/python"
    if name == "halsim_gui":
        return "simulation/halsim_gui"
    if name == "wpimath_test":
        return "wpimath/src/test/python"
    if name == "robotpy_apriltag":
        return "apriltag"
    if name == "robotpy_fields":
        return "fields"
    return name


def fixup_native_lib_name(name):
    return name


def fixup_pybind_package_name(name):
    """
    Maps a project's dependency-name-derived key to the Bazel package its
    *pybind* targets (the "-casters" cc_library, "{dep}_pybind_library", the
    generated casters .pybind11.json, etc.) currently live in.

    This is separate from fixup_root_package_name because a project's native
    wrapper and production library always stay at its top-level package, but
    its pybind-specific targets can be split into a nested package (e.g.
    <project>/src/main/python) on their own schedule - so the two mappings
    diverge project by project as each one gets split.

    Add an entry here (not to fixup_root_package_name) when a project's pybind
    block moves into a subpackage.
    """
    if name == "wpiutil":
        return "wpiutil/src/main/python"
    if name == "wpinet":
        return "wpinet/src/main/python"
    if name == "wpilog":
        return "datalog/src/main/python"
    if name == "pyntcore":
        return "ntcore/src/main/python"
    if name == "ntcore":
        return "ntcore/src/main/python"
    if name == "wpihal":
        return "hal/src/main/python"
    if name == "hal":
        return "hal/src/main/python"
    if name == "wpimath":
        return "wpimath/src/main/python"
    if name == "wpilib":
        return "wpilibc/src/main/python"
    return fixup_root_package_name(name)


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
