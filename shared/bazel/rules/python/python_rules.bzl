load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@allwpilib_pip_deps//:requirements.bzl", "requirement")

load("@rules_python_pytest//python_pytest:defs.bzl", "py_pytest_test")


def wpilib_py_test(name, tests, conftest = None, deps = [], extra_sources = [], **kwargs):
    for test_file in tests:
        py_pytest_test(
            name = test_file[:-3],
            size = "small",
            srcs = [test_file] + extra_sources + conftest,
            deps = deps + [
                requirement("pytest"),
            ],
            target_compatible_with = select({
                "@rules_bzlmodrio_toolchains//constraints/is_bullseye32:bullseye32": ["@platforms//:incompatible"],
                "@rules_bzlmodrio_toolchains//constraints/is_bullseye64:bullseye64": ["@platforms//:incompatible"],
                "@rules_bzlmodrio_toolchains//constraints/is_raspi32:raspi32": ["@platforms//:incompatible"],
                "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["@platforms//:incompatible"],
                "//conditions:default": [],
            }),
            legacy_create_init = 0,
            **kwargs
        )