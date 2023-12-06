load("@rules_python//python:defs.bzl", "py_library", "py_test")
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
        **kwargs
    )
