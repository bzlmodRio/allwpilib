# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname, realpath
_root = abspath(join(dirname(realpath(__file__)), "..", "..", "..", ".."))

libinit_import = "wpiutil._init_wpiutil"
depends = []
pypi_package = 'robotpy-wpiutil'

def get_include_dirs():
    output = [join(_root, "src/main/native/include"), join(_root, "src/main/python/generated/rpy-include/wpiutil/rpy-include"), join(_root, "src", "wpistruct"), join(_root, "src", "type_casters"), join(_root, "src", "main", "python", "wpiutil")]
    import os
    for d in output:
        if not os.path.exists(d):
            print("----------------------------------------" + d + " does not exist!")
    return output

def get_library_dirs():
    return [join(_root, "lib")]

def get_library_dirs_rel():
    return ['lib']

def get_library_names():
    return ['wpiutil']

def get_library_full_names():
    return ['libwpiutil.so']

def get_type_casters_cfg(casters):
    casters.update({'wpi::array': {'hdr': 'wpi_array_type_caster.h'}, 'wpi::json': {'hdr': 'wpi_json_type_caster.h'}, 'std::span': {'hdr': 'wpi_span_type_caster.h'}, 'wpi::SmallSet': {'hdr': 'wpi_smallset_type_caster.h'}, 'wpi::SmallVector': {'hdr': 'wpi_smallvector_type_caster.h'}, 'wpi::SmallVectorImpl': {'hdr': 'wpi_smallvectorimpl_type_caster.h'}, 'wpi::StringMap': {'hdr': 'wpi_string_map_caster.h'}, 'wpi::ct_string': {'hdr': 'wpi_ct_string_type_caster.h'}, 'WPyStruct': {'hdr': 'wpystruct.h'}})

def get_type_casters(casters):
    t = {}
    get_type_casters_cfg(t)
    for k, v in t.items():
        if "hdr" in v:
            casters[k] = v["hdr"]