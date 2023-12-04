load("@pybind11_bazel//:build_defs.bzl", "pybind_extension", "pybind_library")
load("//shared/bazel/rules:cc_rules.bzl", "wpilib_cc_library")

def create_pybind_library(
        name,
        strip_include_prefix = None,
        includes = [],
        extra_srcs = [],
        extra_hdrs = [],
        deps = [],
        entry_point = [],
        rpy_include_dir = None,
        xxxx = ""):
    print("Making pybind library", name)

    generation_subdir = xxxx + name
    rpy_include_dir = rpy_include_dir or "generated/rpy-include/{}/rpy-include".format(name)
    print(rpy_include_dir)
    rpy_includes = native.glob([rpy_include_dir + "/rpygen/*.hpp".format(name)])
    print(rpy_includes)
    rpy_hdr_deps = []
    if rpy_includes:
        print("Has rpy_includes: ", rpy_includes)

        wpilib_cc_library(
            name = "{}_rpy_includes".format(name),
            hdrs = rpy_includes,
            strip_include_prefix = rpy_include_dir,
        )
        rpy_hdr_deps.append("{}_rpy_includes".format(name))

    generated_srcs = native.glob(["generated/gensrc/{}/**/*.cpp".format(generation_subdir)])

    # print(generated_srcs)
    pybind_library(
        name = "{}_pybind_library".format(name),
        srcs = generated_srcs + extra_srcs + native.glob(["generated/gensrc/" + generation_subdir + "/*.hpp"]),
        hdrs = extra_hdrs,
        deps = [
            "//shared/bazel/rules/python/pybind_generator:robotpy_includes",
        ] + deps + rpy_hdr_deps,
        copts = select({
            "@bazel_tools//src/conditions:darwin": ["-Wno-sign-compare", "-Wno-unused-value", "-Wno-pessimizing-move", "-Wno-delete-abstract-non-virtual-dtor", "-Wno-delete-non-abstract-non-virtual-dtor"],
            "@bazel_tools//src/conditions:windows": [],
            "@rules_bzlmodrio_toolchains//constraints/combined:is_linux": ["-Wno-attributes", "-Wno-redundant-move", "-Wno-sign-compare", "-Wno-deprecated", "-Wno-unused-value"],
        }),
        local_defines = ["RPYBUILD_MODULE_NAME=_{}".format(name), "PYBIND11_DETAILED_ERROR_MESSAGES=1"],
        defines = ["PYBIND11_USE_SMART_HOLDER_AS_DEFAULT=1"],
        strip_include_prefix = strip_include_prefix,
        includes = includes,
        visibility = ["//visibility:public"],
        tags = [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
        ],
    )

    pybind_extension(
        name = "_{}".format(name),
        srcs = entry_point + native.glob(["generated/gensrc/" + generation_subdir + "/*.hpp"]),
        deps = [":{}_pybind_library".format(name)],
        defines = ["RPYBUILD_MODULE_NAME=_{}".format(name)],
        visibility = ["//visibility:private"],
        includes = ["generated/gensrc/" + generation_subdir],
        tags = [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
        ],
    )


def pybind_python_library(name, tags = [], **kwargs):
    native.py_library(
        name = name,
        tags = tags + [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
        ],
        **kwargs
    )
    

def pybind_python_test(name, tags = [], **kwargs):
    native.py_test(
        name = name,
        tags = tags + [
            "no-bullseye",
            "no-raspi",
            "no-roborio",
        ],
        **kwargs
    )