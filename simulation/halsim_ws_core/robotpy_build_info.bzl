load("@rules_pycross//pycross/private:wheel_library.bzl", "pycross_wheel_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("//shared/bazel/rules/gen:gen-version-file.bzl", "generate_version_file")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "copy_native_file")

def define_python_library(name):
    generate_version_file(
        name = "{}.generate_version".format(name),
        output_file = "src/main/python/halsim_ws/version.py",
        template = "//shared/bazel/rules/robotpy:version_template.in",
    )

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

    native.filegroup(
        name = name + ".py.typed",
        srcs = [
            "src/main/python/halsim_ws/py.typed",
        ],
    )

    data_files = [
        ":halsim_ws_client.copy_lib",
        ":halsim_ws_server.copy_lib",
        name + ".py.typed",
    ]
    py_library(
        name = "robotpy-halsim-ws.lib",
        srcs = native.glob(["src/main/python/**/*.py"]) + [
            "{}.generate_version".format(name),
        ],
        data = data_files,
        imports = ["src/main/python"],
        deps = [
            "//hal:robotpy-native-wpihal",
            "//wpinet:robotpy-native-wpinet",
        ],
    )

    py_wheel(
        name = "robotpy-halsim-ws-wheel",
        distribution = "robotpy-halsim-ws",
        strip_path_prefixes = ["simulation/halsim_ws_core/src/main/python/"],
        tags = ["robotpy", "no-cache"],
        version = "2027.0.0a3",  # TODO(pj)
        deps = ["robotpy-halsim-ws.lib"] + data_files,
        summary = "WPILib simulator websim Extensions",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-native-wpihal==2027.0.0a3", "robotpy-native-wpinet==2027.0.0a3"],
        license = "BSD-3-Clause",
        entry_points = {
            "robotpy_sim.2027": ["ws-client = halsim_ws.client", "ws-server = halsim_ws.server"],
        },
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
