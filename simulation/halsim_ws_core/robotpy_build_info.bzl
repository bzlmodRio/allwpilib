
load("@rules_python//python:packaging.bzl", "py_wheel")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "copy_native_file")
load("@rules_pycross//pycross/private:wheel_library.bzl", "pycross_wheel_library")

def define_python_library(name):
    copy_native_file(
        name = "halsim_ws_client",
        base_path = "src/main/python/halsim_ws/client/",
        library = "//simulation/halsim_ws_client:shared/halsim_ws_client",
    )

    copy_native_file(
        name = "halsim_ws_server",
        base_path = "src/main/python/halsim_ws/server/",
        library = "//simulation/halsim_ws_server:shared/halsim_ws_server",
    )

    native.py_library(
        name = "robotpy-halsim-ws.lib",
        srcs = native.glob(["src/main/python/**/*.py"]),
        data = [
            ":halsim_ws_client.copy_lib",
            ":halsim_ws_server.copy_lib",
        ],
        imports = ["src/main/python"],
        visibility = ["//visibility:public"],
        deps = [
            "//hal:robotpy-native-wpihal",
            "//wpinet:robotpy-native-wpinet",
        ],
    )

    py_wheel(
        name = "robotpy-halsim-ws-wheel",
        distribution = "robotpy_halsim_ws.lib",
        strip_path_prefixes = ["simulation/halsim_ws_core/src/main/python/"],
        tags = ["robotpy"],
        version = "2027.0.0a3",  # TODO(pj)
        deps = ["robotpy-halsim-ws.lib"],
    )

    pycross_wheel_library(
        name = "robotpy-halsim-ws",
        tags = ["manual"],
        visibility = ["//visibility:public"],
        wheel = "robotpy-halsim-ws-wheel",
        deps = [
            "//hal:robotpy-hal",
        ],
    )
