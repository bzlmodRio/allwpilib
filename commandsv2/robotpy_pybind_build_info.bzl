# THIS FILE IS AUTO GENERATED

load("@allwpilib_pip_deps//:requirements.bzl", "requirement")
load("//shared/bazel/rules/robotpy:robotpy_rules.bzl", "robotpy_library")

def define_pybind_library(name, pkgcfgs = []):

    robotpy_library(
        name = name,
        distribution = "robotpy-commands-v2",
        srcs = native.glob(["src/main/python/commands2/**/*.py"]) + [
        ],
        data = [
        ],
        imports = ["src/main/python"],
        deps = [
            "//wpilibc:robotpy-wpilib",
            requirement("typing_extensions"),
        ],
        strip_path_prefixes = ["commandsv2/src/main/python", "commandsv2"],
        summary = "WPILib command framework v2",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["wpilib==0.0.0", "typing_extensions>=4.1.0,<5"],
        python_requires = ">=3.11",
        entry_points = {
        },
        visibility = ["//visibility:public"],
        description_file = "src/main/python/README.md",
    )

