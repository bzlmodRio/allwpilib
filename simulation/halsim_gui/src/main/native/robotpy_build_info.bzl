# THIS FILE IS AUTO GENERATED

load("@bazel_lib//lib:copy_to_directory.bzl", "copy_to_directory")
load("//shared/bazel/rules/robotpy:robotpy_rules.bzl", "copy_native_file", "generate_native_files", "robotpy_library")

def define_native_wrapper(name, pyproject_toml = None):
    copy_to_directory(
        name = "{}.copy_headers".format(name),
        srcs = native.glob(["include/**"]),
        out = "native/halsim_gui/include",
        root_paths = ["include/"],
        replace_prefixes = {
            "simulation/halsim_gui/src/main/native/include": "",
        },
        verbose = False,
        visibility = ["//visibility:public"],
    )

    libinit_files = ["native/halsim_gui/_init_robotpy_native_halsim_gui.py"]

    generate_native_files(
        name = name,
        pyproject_toml = pyproject_toml,
        pc_deps = [
            "//ntcore/src/main/native:native/ntcore/robotpy-native-ntcore.pc",
            "//hal/src/main/native:native/wpihal/robotpy-native-wpihal.pc",
            "//wpimath/src/main/native:native/wpimath/robotpy-native-wpimath.pc",
        ],
        libinit_files = libinit_files,
        pc_files = ["native/halsim_gui/robotpy-native-halsim-gui.pc"],
    )

    copy_native_file(
        name = "halsim_gui",
        library = "shared/halsim_gui",
        base_path = "native/halsim_gui/",
    )

    robotpy_library(
        name = name,
        distribution = "robotpy-native-halsim-gui",
        srcs = libinit_files,
        data = [
            name + ".pc_wrapper",
            ":halsim_gui.copy_lib",
            "{}.copy_headers".format(name),
        ],
        deps = [
            "//ntcore/src/main/native:robotpy-native-ntcore",
            "//hal/src/main/native:robotpy-native-wpihal",
            "//wpimath/src/main/native:robotpy-native-wpimath",
        ],
        summary = "WPILib HALSim GUI native library",
        requires = ["robotpy-native-wpihal==0.0.0", "robotpy-native-wpimath==0.0.0", "robotpy-native-ntcore==0.0.0"],
        python_requires = ">=3.11",
        strip_path_prefixes = ["simulation/halsim_gui/src/main/native"],
        entry_points = {
            "pkg_config": [
                "halsim_gui = native.halsim_gui",
            ],
        },
    )
