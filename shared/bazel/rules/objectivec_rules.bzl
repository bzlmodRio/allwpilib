load("@rules_cc//cc:defs.bzl", "objc_library")

OBJC_C_COMPILER_FLAGS = [
    "-stdlib=libc++",
    "-fobjc-weak",
    "-fobjc-arc",
    "-fPIC",
]

OBJC_CXX_COMPILER_FLAGS = OBJC_C_COMPILER_FLAGS + ["-std=c++20"]

def wpilib_objc_library(
        name,
        srcs = [],
        deps = [],
        copts = [],
        **kwargs):
    objc_library(
        name = name,
        srcs = srcs,
        copts = copts + OBJC_CXX_COMPILER_FLAGS,
        tags = ["manual"],  # This makes it so the other platforms will still build OK
        deps = deps,
        **kwargs
    )
