load("@rules_cc//cc:defs.bzl", "cc_binary", "cc_import", "cc_library", "cc_test")

def wpilib_cc_library(
        name,
        tags = [],
        **kwargs):
    cc_library(
        name = name,
        tags = tags + ["allwpilib-build-cpp"],
        **kwargs
    )

def wpilib_cc_binary(
        name,
        tags = [],
        **kwargs):
    cc_binary(
        name = name,
        tags = tags + ["allwpilib-build-cpp"],
        **kwargs
    )

def wpilib_cc_test(
        name,
        tags = [],
        standard_deps = [],
        wpi_maybe_shared_deps = [],
        create_static_test = True,
        create_shared_test = True,
        **kwargs):
        
    static_deps = [x + ".static" for x in wpi_maybe_shared_deps]
    shared_deps = [x + ".shared" for x in wpi_maybe_shared_deps]

    if create_static_test:
        cc_test(
            name = name + ".static",
            tags = tags + ["allwpilib-build-cpp"],
            deps = standard_deps + static_deps,
            **kwargs
        )
    
    if create_shared_test:
        if not wpi_maybe_shared_deps:
            fail("No maybe-shared deps for " + name + "... consider not creating shared test")
        cc_test(
            name = name + ".shared",
            tags = tags + ["allwpilib-build-cpp"],
            deps = standard_deps + static_deps,
            dynamic_deps = shared_deps,
            **kwargs
        )

def wpilib_cc_shared_library(
        name,
        srcs = [],
        deps = [],
        tags = [],
        visibility = None,
        **shared_binary_kwargs):
    # Make the visibility private, so it can only be available through the alias
    shared_lib_name = name
    wpilib_cc_binary(
        name = shared_lib_name,
        srcs = srcs,
        deps = deps,
        linkshared = 1,
        tags = tags,
        visibility = ["//visibility:private"],
        **shared_binary_kwargs
    )

    # Because we cannot directly depend on cc_binary from other cc rules in deps attribute,
    # we use cc_import as a bridge to depend on the dll.

    # Get the import library for the dll
    native.filegroup(
        name = name + ".shared_import",
        srcs = [":" + shared_lib_name],
        output_group = "interface_library",
        tags = tags,
        visibility = ["//visibility:private"],
    )
    shared_lib_import_name = name + ".import"
    cc_import(
        name = shared_lib_import_name,
        interface_library = select({
            "@bazel_tools//src/conditions:windows": ":" + name + ".shared_import",
            "//conditions:default": None,
        }),
        shared_library = ":" + shared_lib_name,
        visibility = ["//visibility:private"],
    )

    # Finally, create a library that can be depended on
    wpilib_cc_library(
        name = name + ".shared",
        deps = deps + [":" + shared_lib_import_name],
        tags = tags,
        visibility = visibility,
    )

# https://github.com/bazelbuild/bazel/blob/26c7e10739907332e70d31e68d2bd2ff2e9a84fb/examples/windows/dll
def wpilib_cc_static_and_shared_library(
        name,
        srcs = [],
        hdrs = [],
        includes = [],
        features = [],
        defines = [],
        standard_deps = [],
        wpi_maybe_shared_deps = [],
        visibility = None,
        strip_include_prefix = None,
        export_symbols = True):

    print("Making Shared+Static for " + name)

    headers_name = name + ".headers"
    wpilib_cc_library(
        name = headers_name,
        hdrs = hdrs,
        strip_include_prefix = strip_include_prefix,
    )

    # Bundle the sources, so it appears as they are only used once
    native.filegroup(
        name = name + ".sources",
        srcs = srcs,
    )

    static_lib_name = name + ".static"
    static_deps = standard_deps + [x + ".static" for x in wpi_maybe_shared_deps]
    wpilib_cc_library(
        name = static_lib_name,
        srcs = [name + ".sources"],
        includes = includes,
        defines = defines,
        deps = static_deps + [":" + headers_name],
        visibility = visibility,
        linkstatic = True
    )

    dynamic_deps = [x + ".shared" for x in wpi_maybe_shared_deps]

    print(standard_deps)
    print(dynamic_deps)
    
    shared_features = list(features)
    if export_symbols:
        shared_features += ["windows_export_all_symbols"]

    print()
    native.cc_shared_library(
        name = name + "",
        deps = [static_lib_name],
        dynamic_deps = dynamic_deps,
        visibility = ["//visibility:private"],
        features = shared_features,
        # visibility = visibility,
    )

    native.alias(
        name = name + ".shared",
        actual = name,
        visibility = visibility,
    )

    print("\n\n")


def wpilib_dev_binary(
    name,
    wpi_maybe_shared_deps = [],
    **kwargs):

    deps = [x + ".static" for x in wpi_maybe_shared_deps]
    dynamic_deps = [x + ".shared" for x in wpi_maybe_shared_deps]

    wpilib_cc_binary(
        name = name,
        deps = deps,
        dynamic_deps = dynamic_deps,
        **kwargs,
    )

