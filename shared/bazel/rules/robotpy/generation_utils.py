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
    if name == "wpimath_test":
        return "wpimath"
    if name == "robotpy_apriltag":
        return "apriltag"
    if name == "robotpy_fields":
        return "fields"
    return name


def fixup_native_lib_name(name):
    return name


# def fixup_native_package_name(name):
#     """
#     Maps a project's dependency-name-derived key to the real Bazel package its
#     *native* (C++) targets live in (shared/<x>, robotpy-native-<x>, etc.) now
#     that every project participating in robotpy generation has a
#     src/main/native subpackage. Unlike fixup_pybind_package_name, this is a
#     blanket rule rather than a per-project allowlist, since there is no
#     remaining unmigrated project to preserve backward compatibility with.
#     """
#     return f"{fixup_root_package_name(name)}/src/main/native"


# def fixup_python_package_name(name):
#     """
#     Same as fixup_native_package_name, but for a project's *python*
#     (src/main/python) targets (<x>_pybind_library, etc.).
#     """
#     return f"{fixup_root_package_name(name)}/src/main/python"


def fixup_pybind_package_name(name):
    """
    Maps a project's dependency-name-derived key to the Bazel package its
    *pybind* casters output file (<name>-casters.pybind11.json) currently
    lives in.

    This exists ONLY for ResolveCastersConfig's cross-project caster_deps
    computation in generate_pybind_build_file.py. That code reconstructs a
    generated-output-file label directly from a physical bazel-out path
    (treating the first path segment as the package and the rest as the
    in-package target name) - which breaks once a project's pybind block
    moves into its own subpackage, because the physical path is identical
    either way (files never move, only which BUILD.bazel package declares
    them does) and an alias can't paper over it: Bazel forbids a target name
    whose prefix collides with an existing subpackage path (e.g. wpiutil
    can no longer have a target literally named
    "src/main/python/wpiutil/wpiutil-casters.pybind11.json" once
    wpiutil/src/main/python is a real package). Every other cross-project
    label in this generator keeps working through a same-named alias at the
    project's old top-level location - this is the one narrow exception.

    Add an entry here only for a project that both (a) has been migrated to
    its own src/main/python subpackage, and (b) calls publish_library_casters().
    """
    if name == "wpiutil":
        return "wpiutil/src/main/python"
    if name == "wpimath":
        return "wpimath/src/main/python"
    return name


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
