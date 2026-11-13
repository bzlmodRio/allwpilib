load("//shared/bazel/rules:cc_rules.bzl", "wpilib_cc_library")

def wpilib_halsim_extension(
        name,
        native_srcs_root = "src/main/native/",
        **kwargs):
    """
    Helper wrapper for creating a HALSIM extension. Provides some of the default arguments for creating the library.

    Params:
        native_srcs_root: Package-relative prefix of the cpp/include directories. Use "" when invoked
            from the src/main/native package itself.
    """
    wpilib_cc_library(
        name = name,
        includes = [native_srcs_root + "include"],
        srcs_pkg_root = native_srcs_root + "cpp",
        hdrs_pkg_root = native_srcs_root + "include",
        target_compatible_with = select({
            "@wpilib_toolchains//constraints/is_systemcore:systemcore": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        visibility = ["//visibility:public"],
        **kwargs
    )
