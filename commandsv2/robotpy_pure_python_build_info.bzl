load("@allwpilib_pip_deps//:requirements.bzl", "requirement")
load("@rules_pycross//pycross/private:wheel_library.bzl", "pycross_wheel_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")

def define_python_library(name):
    py_library(
        name = "commandsv2-py",
        srcs = native.glob(["src/main/python/**/*.py"]),
        imports = ["src/main/python"],
        visibility = ["//visibility:public"],
        deps = [
            "//wpilibc:robotpy-wpilib",
            requirement("typing-extensions"),
        ],
    )

    py_wheel(
        name = "commandsv2-wheel",
        distribution = "robotpy-commands-v2",
        strip_path_prefixes = ["commandsv2/src/main/python/"],
        tags = ["robotpy"],
        version = "2027.0.0a3",  # TODO(pj) #{PYBIND_VERSION}
        deps = ["commandsv2-py"],
        summary = "WPILib command framework v2",
        project_urls = {"Source code": "https://github.com/robotpy/robotpy-commands-v2"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        description_content_type = "text/markdown",
        description_file = "generate.bzl",
        requires = ["typing-extensions<5,>=4.1.0", "wpilib==2027.0.0a3"],
        license = "BSD-3-Clause",
    )

    pycross_wheel_library(
        name = "commandsv2-import",
        tags = ["manual"],
        visibility = ["//visibility:public"],
        wheel = "commandsv2-wheel",
        deps = [
            "//wpilibc:robotpy-wpilib",
            requirement("typing-extensions"),
        ],
    )
