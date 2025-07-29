load("@allwpilib_pip_deps//:requirements.bzl", "requirement")
load("@aspect_bazel_lib//lib:write_source_files.bzl", "write_source_files")
load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("//shared/bazel/rules/robotpy:compatibility_select.bzl", "robotpy_compatibility_select")

def __create_yaml_files_impl(ctx):
    output_dir = ctx.actions.declare_directory(ctx.attr.gen_dir)

    args = ctx.actions.args()
    args.add("--output_dir=" + output_dir.path)
    args.add("--backup_dir=" + ctx.attr.backup_dir)
    args.add("--directory=" + ctx.attr.directory)
    args.add("--pkgcfgs")
    for f in ctx.files.pkgcfgs:
        args.add(str(f.path))

    ctx.actions.run(
        inputs = ctx.files.package_root_file + ctx.files.pyproject_toml + ctx.files.pkgcfgs + ctx.files.extra_hdrs + ctx.files.yaml_files,
        outputs = [output_dir],
        executable = ctx.executable._tool,
        arguments = [args],
    )

    return [DefaultInfo(files = depset([output_dir]))]

__create_yaml_files = rule(
    implementation = __create_yaml_files_impl,
    attrs = {
        "backup_dir": attr.string(default = "_gen_create_yaml_original"),
        "directory": attr.string(mandatory = True),
        "extra_hdrs": attr.label_list(allow_files = True),
        "gen_dir": attr.string(default = "_gen_create_yaml"),
        "package_root_file": attr.label(mandatory = True, allow_files = True),
        "pkgcfgs": attr.label_list(allow_files = True),
        "pyproject_toml": attr.label(mandatory = True, allow_files = True),
        "yaml_files": attr.label_list(mandatory = True, allow_files = True),
        "_tool": attr.label(
            default = Label("//shared/bazel/rules/robotpy:create-yaml"),
            cfg = "exec",
            executable = True,
        ),
    },
)

def create_yaml_files(name, **kwargs):
    __create_yaml_files(name = name, **kwargs)

    write_source_files(
        name = "write_{}".format(name),
        files = {
            "src/main/python/semiwrap": ":" + name,
        },
        suggested_update_target = "//:write_all",
        tags = ["robotpy", "noremote"],
        visibility = ["//visibility:public"],
        diff_test = False,  # These are often hand tweaked
    )

def scan_headers(name, directory, pyproject_toml, package_root_file, extra_hdrs, pkgcfgs):
    pkgcfg_args = ["--pkgcfgs"]
    for pkgcfg in pkgcfgs:
        pkgcfg_args.append(" $(location " + pkgcfg + ")")
    py_test(
        name = name,
        srcs = [
            "//shared/bazel/rules/robotpy:scan-headers.py",
        ],
        deps = [
            requirement("semiwrap"),
        ],
        args = [
            "--directory=" + directory,
        ] + pkgcfg_args,
        data = extra_hdrs + pkgcfgs + [pyproject_toml, package_root_file],
        main = "shared/bazel/rules/robotpy/scan-headers.py",
        size = "small",
    )

def create_imports(name, library, output_file, base, compiled = None):
    py_binary(
        name = name,
        srcs = [
            "//shared/bazel/rules/robotpy:create-imports.py",
        ],
        deps = library + [
            requirement("semiwrap"),
        ],
        main = "shared/bazel/rules/robotpy/create-imports.py",
        tags = ["robotpy", "manual"],
        legacy_create_init = 0,
    )

    cmd = "$(location " + name + ") --output_file=$(OUTS) --base=" + base
    if compiled:
        cmd += " --compiled=" + compiled

    native.genrule(
        name = name + ".gen",
        tools = [name],
        outs = ["{}-create_imports.py".format(name)],
        cmd = cmd,
        tags = ["robotpy", "manual"],
        target_compatible_with = robotpy_compatibility_select(),
    )

    write_source_files(
        name = "{}.generate_build_info4".format(name),
        files = {
            output_file: "{}-create_imports.py".format(name),
        },
        visibility = ["//visibility:public"],
        target_compatible_with = robotpy_compatibility_select(),
    )
