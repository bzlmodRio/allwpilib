
load("@rules_python//python:packaging.bzl", "py_wheel")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "copy_native_file")

def define_python_library(name):
    copy_native_file(
        name = "halsim_ds_socket",
        base_path = "src/main/python/halsim_ds_socket/",
        library = "shared/halsim_ds_socket",
    )

    native.py_library(
        name = "robotpy-halsim-ds-socket",
        srcs = native.glob(["src/main/python/**/*.py"]),
        data = [
            ":halsim_ds_socket.copy_lib",
        ],
        imports = ["src/main/python"],
        deps = [
            "//hal:robotpy-native-wpihal",
            "//wpinet:robotpy-native-wpinet",
        ],
    )

    py_wheel(
        name = "robotpy-halsim-ds-socket-wheel",
        distribution = "robotpy_halsim_ds_socket",
        strip_path_prefixes = ["simulation/halsim_ds_socket/src/main/python/"],
        tags = ["robotpy"],
        version = "2027.0.0a3",  # TODO(pj)
        deps = ["robotpy-halsim-ds-socket"],
    )
