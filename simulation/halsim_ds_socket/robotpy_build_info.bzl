load("@rules_pycross//pycross/private:wheel_library.bzl", "pycross_wheel_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("//shared/bazel/rules/gen:gen-version-file.bzl", "generate_version_file")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "copy_native_file")

def define_python_library(name):
    generate_version_file(
        name = "{}.generate_version".format(name),
        output_file = "src/main/python/halsim_ds_socket/version.py",
        template = "//shared/bazel/rules/robotpy:version_template.in",
    )

    copy_native_file(
        name = "halsim_ds_socket",
        base_path = "src/main/python/halsim_ds_socket/",
        library = "shared/halsim_ds_socket",
    )

    native.filegroup(
        name = name + ".py.typed",
        srcs = [
            "src/main/python/halsim_ds_socket/py.typed",
        ],
    )

    data_files = [
        ":halsim_ds_socket.copy_lib",
        name + ".py.typed",
    ]
    py_library(
        name = "robotpy-halsim-ds-socket.lib",
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
        name = "robotpy-halsim-ds-socket-wheel",
        distribution = "robotpy-halsim-ds-socket",
        strip_path_prefixes = ["simulation/halsim_ds_socket/src/main/python/"],
        tags = ["robotpy"],
        version = "2027.0.0a3",  # TODO(pj)
        deps = ["robotpy-halsim-ds-socket.lib"] + data_files,
        summary = "WPILib simulator DS Socket Extension",
        project_urls = None,
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-native-wpihal==2027.0.0a3", "robotpy-native-wpinet==2027.0.0a3"],
        license = "BSD-3-Clause",
        entry_points = {
            "robotpy_sim.2027": ["ds-socket = halsim_ds_socket"],
        },
    )

    pycross_wheel_library(
        name = "robotpy-halsim-ds-socket",
        tags = ["manual"],
        visibility = ["//visibility:public"],
        wheel = "robotpy-halsim-ds-socket-wheel",
        deps = [
            "//hal:robotpy-hal",
        ],
    )
