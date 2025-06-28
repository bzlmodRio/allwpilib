load("@rules_python_pytest//python_pytest:defs.bzl", "py_pytest_test")

def robotpy_py_test(name, tests, extra_sources = [], **kwargs):
    for test_file in tests:
        py_pytest_test(
            name = test_file[:-3],
            size = "small",
            srcs = [test_file] + extra_sources,
            target_compatible_with = select({
                "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore": ["@platforms//:incompatible"],
                "//conditions:default": [],
            }),
            tags = [
                "no-asan",
                "no-tsan",
            ],
            legacy_create_init = 0,
            **kwargs
        )
