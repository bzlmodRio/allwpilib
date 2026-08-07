# THIS FILE IS AUTO GENERATED

load("//shared/bazel/rules/gen:gen-version-file.bzl", "generate_version_file")
load("//shared/bazel/rules/robotpy:robotpy_rules.bzl", "copy_native_file", "robotpy_library")

def define_pybind_library(name, pkgcfgs = []):
    copy_native_file(
        name = "halsim_ds_socket",
        base_path = "src/main/python/halsim_ds_socket/",
        library = "shared/halsim_ds_socket",
    )

    generate_version_file(
        name = "{}.generate_version".format(name),
        output_file = "src/main/python/halsim_ds_socket/version.py",
        template = "//shared/bazel/rules/robotpy:version_template.in",
    )

    robotpy_library(
        name = name,
        distribution = "robotpy-halsim-ds-socket",
        srcs = native.glob(["src/main/python/halsim_ds_socket/**/*.py"]) + [
            "{}.generate_version".format(name),
        ],
        data = [
            ":halsim_ds_socket.copy_lib",
        ],
        imports = ["src/main/python"],
        deps = [
            "//hal:robotpy-native-wpihal",
            "//wpinet:robotpy-native-wpinet",
        ],
        strip_path_prefixes = ["simulation/halsim_ds_socket/src/main/python", "simulation/halsim_ds_socket"],
        summary = "WPILib simulator DS Socket Extension",
        project_urls = None,
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-native-wpihal==0.0.0", "robotpy-native-wpinet==0.0.0"],
        python_requires = ">=3.11",
        entry_points = {
            "robotpy_sim.2027": ["ds-socket = halsim_ds_socket"],
        },
        visibility = ["//visibility:public"],
    )
