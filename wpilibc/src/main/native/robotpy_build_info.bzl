# THIS FILE IS AUTO GENERATED

load("@bazel_lib//lib:copy_to_directory.bzl", "copy_to_directory")
load("//shared/bazel/rules/robotpy:robotpy_rules.bzl", "copy_native_file", "generate_native_files", "robotpy_library")

def define_native_wrapper(name, pyproject_toml = None):
    copy_to_directory(
        name = "{}.copy_headers".format(name),
        srcs = native.glob(["include/**"]) + ["//wpilibc:generated-native-include-files"],
        out = "native/wpilib/include",
        root_paths = ["include/"],
        replace_prefixes = {
            "wpilibc/src/generated/main/native/include": "",
            "wpilibc/src/main/native/include": "",
        },
        verbose = False,
        visibility = ["//visibility:public"],
    )

    libinit_files = ["native/wpilib/_init_robotpy_native_wpilib.py"]

    generate_native_files(
        name = name,
        pyproject_toml = pyproject_toml,
        pc_deps = [
            "//ntcore/src/main/native:native/ntcore/robotpy-native-ntcore.pc",
            "//telemetry/src/main/native:native/telemetry/robotpy-native-telemetry.pc",
            "//tunables/src/main/native:native/tunables/robotpy-native-tunables.pc",
            "//hal/src/main/native:native/wpihal/robotpy-native-wpihal.pc",
            "//wpimath/src/main/native:native/wpimath/robotpy-native-wpimath.pc",
            "//wpinet/src/main/native:native/wpinet/robotpy-native-wpinet.pc",
            "//wpiutil/src/main/native:native/wpiutil/robotpy-native-wpiutil.pc",
        ],
        libinit_files = libinit_files,
        pc_files = ["native/wpilib/robotpy-native-wpilib.pc"],
    )

    copy_native_file(
        name = "wpilibc",
        library = "shared/wpilibc",
        base_path = "native/wpilib/",
    )

    robotpy_library(
        name = name,
        distribution = "robotpy-native-wpilib",
        srcs = libinit_files,
        data = [
            name + ".pc_wrapper",
            ":wpilibc.copy_lib",
            "{}.copy_headers".format(name),
        ],
        deps = [
            "//ntcore/src/main/native:robotpy-native-ntcore",
            "//telemetry/src/main/native:robotpy-native-telemetry",
            "//tunables/src/main/native:robotpy-native-tunables",
            "//hal/src/main/native:robotpy-native-wpihal",
            "//wpimath/src/main/native:robotpy-native-wpimath",
            "//wpinet/src/main/native:robotpy-native-wpinet",
            "//wpiutil/src/main/native:robotpy-native-wpiutil",
        ],
        summary = "WPILib Robotics Library",
        requires = ["robotpy-native-wpiutil==0.0.0", "robotpy-native-wpinet==0.0.0", "robotpy-native-ntcore==0.0.0", "robotpy-native-wpimath==0.0.0", "robotpy-native-wpihal==0.0.0", "robotpy-native-telemetry==0.0.0", "robotpy-native-tunables==0.0.0"],
        python_requires = ">=3.11",
        strip_path_prefixes = ["wpilibc/src/main/native"],
        entry_points = {
            "pkg_config": [
                "wpilib = native.wpilib",
            ],
        },
    )
