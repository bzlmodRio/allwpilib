# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname, realpath
_root = abspath(join(dirname(realpath(__file__)), "..", "..", "..", ".."))

libinit_import = "ntcore._init_ntcore"
depends = ['wpiutil', 'wpinet']
pypi_package = 'pyntcore'

def get_include_dirs():
    output = [join(_root, "src/main/native/include"), join(_root, "src/main/python/generated/rpy-include/ntcore/rpy-include"), join(_root, "src", "generated", "main", "native", "include")]
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
    return ['ntcore']

def get_library_full_names():
    return ['libntcore.so']