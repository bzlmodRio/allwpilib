load("@aspect_bazel_lib//lib:copy_file.bzl", "copy_file")
load("@pybind11_bazel//:build_defs.bzl", "pybind_extension", "pybind_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")

def create_pybind_library(
        name,
        extension_name = None,
        install_path = "",
        generated_srcs = [],
        extra_hdrs = [],
        extra_srcs = [],
        deps = [],
        dynamic_deps = [],
        semiwrap_header = [],
        copts = [],
        includes = [],
        local_defines = []):
    # srcs = [DAT_TO_CC_DIR + src + ".cpp" for src in dat_to_cc_srcs]
    pybind_library(
        name = "{}_pybind_library".format(name),
        hdrs = extra_hdrs,
        copts = copts + select({
            "@bazel_tools//src/conditions:darwin": [
                "-Wno-deprecated-declarations",
                "-Wno-overloaded-virtual",
                "-Wno-pessimizing-move",
            ],
            "@bazel_tools//src/conditions:linux_x86_64": [
                "-Wno-attributes",
                "-Wno-unused-value",
                "-Wno-deprecated",
                "-Wno-deprecated-declarations",
                "-Wno-unused-parameter",
                "-Wno-redundant-move",
                "-Wno-unused-but-set-variable",
                "-Wno-unused-variable",
                "-Wno-pessimizing-move",
            ],
            "@bazel_tools//src/conditions:windows": [
            ],
        }),
        target_compatible_with = select({
            "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        deps = deps + [
            "//shared/bazel/rules/robotpy:semiwrap_headers",
        ],
        includes = includes,
        visibility = ["//visibility:public"],
        local_defines = local_defines,
    )

    extension_name = extension_name or "_{}".format(name)
    pybind_extension(
        name = install_path + extension_name,
        srcs = extra_srcs + generated_srcs,
        deps = [":{}_pybind_library".format(name)] + semiwrap_header,
        dynamic_deps = dynamic_deps,
        visibility = ["//visibility:private"],
        copts = copts + select({
            "@bazel_tools//src/conditions:darwin": [
                "-Wno-deprecated-declarations",
                "-Wno-overloaded-virtual",
                "-Wno-pessimizing-move",
                "-Wno-unused-value",
            ],
            "@bazel_tools//src/conditions:linux_x86_64": [
                "-Wno-attributes",
                "-Wno-unused-value",
                "-Wno-deprecated",
                "-Wno-deprecated-declarations",
                "-Wno-unused-parameter",
                "-Wno-redundant-move",
                "-Wno-unused-but-set-variable",
                "-Wno-unused-variable",
                "-Wno-pessimizing-move",
            ],
            "@bazel_tools//src/conditions:windows": [
            ],
        }),
        target_compatible_with = select({
            "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        local_defines = local_defines,
    )

def robotpy_library(
        name,
        # package_name,
        strip_path_prefixes,
        # version,
        data = [],
        # deps = [],
        # robotpy_wheel_deps = [],
        # entry_points = {},
        # package_python_tag = "cp311",
        # package_abi = "cp311",
        # package_summary = None,
        # package_project_urls = None,
        # package_author_email = None,
        # package_requires = None,
        # visibility = None,
        python_tag = "cp310",  # TODO
        abi = "cp310",
        summary = None,
        project_urls = None,
        author_email = None,
        entry_points = None,
        requires = None,
        **kwargs):
    py_library(
        name = name,
        data = data,
        **kwargs
    )

    py_wheel(
        name = "{}-wheel".format(name),
        distribution = name,
        platform = select({
            "@bazel_tools//src/conditions:darwin": "macosx_11_0_x86_64",
            "@bazel_tools//src/conditions:windows": "win_amd64",
            "//conditions:default": "manylinux_2_35_x86_64",
        }),
        # python_tag = package_python_tag,
        abi = abi,
        python_tag = python_tag,
        stamp = 1,
        version = "2027.0.0a1.dev0",  # TODO
        summary = summary,
        requires = requires,
        project_urls = project_urls,
        author_email = author_email,
        deps = data + [":{}".format(name)],
        strip_path_prefixes = strip_path_prefixes,
        entry_points = entry_points,
    )

def copy_native_file(name, library, base_path):
    copy_file(
        name = name + ".win_copy_lib",
        src = library,
        out = "{}lib/{}.dll".format(base_path, name),
        tags = ["manual"],
        visibility = ["//visibility:public"],
    )

    copy_file(
        name = name + ".osx_copy_lib",
        src = library,
        out = "{}lib/lib{}.dylib".format(base_path, name),
        tags = ["manual"],
        visibility = ["//visibility:public"],
    )

    copy_file(
        name = name + ".linux_copy_lib",
        src = library,
        out = "{}lib/lib{}.so".format(base_path, name),
        tags = ["manual"],
        visibility = ["//visibility:public"],
    )

    native.alias(
        name = "{}.copy_lib".format(name),
        actual = select({
            "@bazel_tools//src/conditions:darwin": name + ".osx_copy_lib",
            "@bazel_tools//src/conditions:windows": name + ".win_copy_lib",
            "//conditions:default": name + ".linux_copy_lib",
        }),
        visibility = ["//visibility:public"],
    )

def _folder_prefix(name):
    if "/" in name:
        last_slash = name.rfind("/")
        return (name[0:last_slash], name[last_slash + 1:])
    else:
        return ("", name)

def native_wrappery_library(
        name,
        pyproject_toml,
        libinit_file,
        pc_file,
        pc_deps,
        native_shared_library,
        install_path,
        headers,
        strip_path_prefixes = [],
        python_tag = "py3",  # TODO
        abi = "none",
        summary = None,
        project_urls = None,
        author_email = None,
        entry_points = None,
        requires = None,
        deps = []):
    cmd = "$(locations //shared/bazel/rules/robotpy/hatchlib_native_port:generate_native_lib_files) "
    cmd += "  $(location " + pyproject_toml + ")"
    cmd += " $(OUTS) "
    for pc_dep in pc_deps:
        cmd += " $(location " + pc_dep + ")"

    native.genrule(
        name = name + ".gen",
        srcs = [pyproject_toml],
        outs = [libinit_file, pc_file],
        cmd = cmd,
        tools = ["//shared/bazel/rules/robotpy/hatchlib_native_port:generate_native_lib_files"] + pc_deps,
        visibility = ["//visibility:public"],
    )

    prefix, libname = _folder_prefix(native_shared_library)

    copy_native_file(
        name = libname,
        library = native_shared_library,
        base_path = install_path,
    )

    native.filegroup(
        name = name + ".pc_wrapper",
        srcs = [pc_file],
    )

    py_library(
        name = name,
        srcs = [libinit_file],
        data = [pc_file, ":{}.copy_lib".format(libname), headers],
        deps = deps,
        imports = ["."],
        visibility = ["//visibility:public"],
    )

    py_wheel(
        name = "{}-wheel".format(name),
        distribution = name,
        platform = select({
            "@bazel_tools//src/conditions:darwin": "macosx_11_0_x86_64",
            "@bazel_tools//src/conditions:windows": "win_amd64",
            "//conditions:default": "manylinux_2_35_x86_64",
        }),
        abi = abi,
        python_tag = python_tag,
        stamp = 1,
        version = "2027.0.0a1.dev0",  # TODO
        summary = summary,
        requires = requires,
        project_urls = project_urls,
        author_email = author_email,
        deps = [name, ":{}.copy_lib".format(libname), headers, name + ".pc_wrapper"],
        strip_path_prefixes = strip_path_prefixes,
        entry_points = entry_points,
    )
