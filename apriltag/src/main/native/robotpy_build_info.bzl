# THIS FILE IS AUTO GENERATED

load("@bazel_lib//lib:copy_to_directory.bzl", "copy_to_directory")
load("//shared/bazel/rules/robotpy:robotpy_rules.bzl", "copy_native_file", "generate_native_files", "robotpy_library")

def define_native_wrapper(name, pyproject_toml = None):
    copy_to_directory(
        name = "{}.copy_headers".format(name),
        srcs = native.glob(["include/**"]) + native.glob([
            "thirdparty/apriltag/include/**",
        ]),
        out = "native/apriltag/include",
        root_paths = ["include/"],
        replace_prefixes = {
            "apriltag/src/main/native/include": "",
            "apriltag/src/main/native/thirdparty/apriltag/include": "",
        },
        verbose = False,
        visibility = ["//visibility:public"],
    )

    libinit_files = ["native/apriltag/_init_robotpy_native_apriltag.py"]

    generate_native_files(
        name = name,
        pyproject_toml = pyproject_toml,
        pc_deps = [
            "//wpimath/src/main/native:native/wpimath/robotpy-native-wpimath.pc",
            "//wpiutil/src/main/native:native/wpiutil/robotpy-native-wpiutil.pc",
        ],
        libinit_files = libinit_files,
        pc_files = ["native/apriltag/robotpy-native-apriltag.pc"],
    )

    copy_native_file(
        name = "apriltag",
        library = "shared/apriltag",
        base_path = "native/apriltag/",
    )

    robotpy_library(
        name = name,
        distribution = "robotpy-native-apriltag",
        srcs = libinit_files,
        data = [
            name + ".pc_wrapper",
            ":apriltag.copy_lib",
            "{}.copy_headers".format(name),
        ],
        deps = [
            "//wpimath/src/main/native:robotpy-native-wpimath",
            "//wpiutil/src/main/native:robotpy-native-wpiutil",
        ],
        summary = "WPILib AprilTag Library",
        requires = ["robotpy-native-wpiutil==0.0.0", "robotpy-native-wpimath==0.0.0"],
        python_requires = ">=3.11",
        strip_path_prefixes = ["apriltag/src/main/native"],
        entry_points = {
            "pkg_config": [
                "apriltag = native.apriltag",
            ],
        },
    )
