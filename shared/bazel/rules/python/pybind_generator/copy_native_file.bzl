load("@aspect_bazel_lib//lib:copy_file.bzl", "copy_file")


def copy_native_file(name, library):
    copy_file(
        name = name + ".win_copy_lib",
        src = library,
        out = "lib/{}.dll".format(name),
        visibility = ["//visibility:public"]
    )

    copy_file(
        name = name + ".unix_copy_lib",
        src = library,
        out = "lib/lib{}.so".format(name),
        visibility = ["//visibility:public"]
    )


    native.alias(
        name = "copy_lib",
        actual = select({
            "@rules_bazelrio//conditions:windows": name + ".win_copy_lib",
            "//conditions:default": name + ".unix_copy_lib",
        }),
        visibility = ["//visibility:public"]
    )