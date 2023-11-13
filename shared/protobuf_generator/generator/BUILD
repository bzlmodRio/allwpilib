load("@allwpilib_pip_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "helpers",
    srcs = glob(["*.py"]),
    visibility = ["//visibility:public"],
    data = glob(["templates/**"]),
    deps = [
        "//wpimath/src/main/proto:py_proto",
        requirement("jinja2"),
    ],
)
