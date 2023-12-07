load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@rules_robotpy_utils//rules_robotpy_utils:pybind_rules.bzl", _create_pybind_library = "create_pybind_library")

def create_pybind_library(name, **kwargs):
    _create_pybind_library(name, **kwargs)

def pybind_python_library(name, tags = [], **kwargs):
    py_library(
        name = name,
        tags = tags + [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
        ],
        target_compatible_with = select({
            "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_raspi32:raspi32": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        **kwargs
    )

def pybind_python_binary(name, tags = [], **kwargs):
    py_binary(
        name = name,
        tags = tags + [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
        ],
        target_compatible_with = select({
            "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_raspi32:raspi32": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        **kwargs
    )

def pybind_python_test(name, tags = [], **kwargs):
    py_test(
        name = name,
        tags = tags + [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
            "no-asan",
            "no-tsan",
        ],
        target_compatible_with = select({
            "@rules_bazelrio//conditions:windows": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_raspi32:raspi32": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        **kwargs
    )
