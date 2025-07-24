# THIS FILE IS AUTO GENERATED

load("@aspect_bazel_lib//lib:copy_to_directory.bzl", "copy_to_directory")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "native_wrappery_library")

def define_native_wrapper(name, pyproject_toml = None):
    copy_to_directory(
        name = "{}.copy_headers".format(name),
        srcs = native.glob(["src/main/native/include/**"]) + native.glob(["src/generated/main/native/include/**"], allow_empty = True) + native.glob([
            "src/main/native/thirdparty/eigen/include/**",
            "src/main/native/thirdparty/gcem/include/**",
            "src/main/native/thirdparty/sleipnir/include/**",
        ]),
        out = "native/wpimath/include",
        root_paths = ["src/main/native/include/"],
        replace_prefixes = {
            "wpimath/src/generated/main/native/include": "",
            "wpimath/src/main/native/include": "",
            "wpimath/src/main/native/thirdparty/eigen/include": "",
            "wpimath/src/main/native/thirdparty/gcem/include": "",
            "wpimath/src/main/native/thirdparty/sleipnir/include": "",
        },
        verbose = False,
        visibility = ["//visibility:public"],
    )

    native_wrappery_library(
        name = name,
        pyproject_toml = pyproject_toml or "src/main/python/native-pyproject.toml",
        libinit_file = "native/wpimath/_init_robotpy_native_wpimath.py",
        pc_file = "native/wpimath/robotpy-native-wpimath.pc",
        pc_deps = [
            "//wpiutil:native/wpiutil/robotpy-native-wpiutil.pc",
        ],
        deps = [
            "//wpiutil:robotpy-native-wpiutil",
        ],
        headers = "{}.copy_headers".format(name),
        native_shared_library = "shared/wpimath",
        install_path = "native/wpimath/",
        strip_path_prefixes = ["wpimath"],
        requires = ["robotpy-native-wpiutil==2027.0.0a2"],
        summary = "WPILib Math Library",
        entry_points = {
            "pkg_config": [
                "wpimath = native.wpimath",
            ],
        },
    )
