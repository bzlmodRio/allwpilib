
load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@aspect_bazel_lib//lib:write_source_files.bzl", "write_source_files")

def generate_robopy_files(
    name,
    config_file,
):
    __run_on_dl(
        name = name,
        config_file = config_file,
    )

    __run_on_build_gen(
        name = name,
        config_file = config_file,
    )
    
    # write_source_files(
    #     name = "write_all",
    #     additional_update_targets = [
    #         ":write_on_build_dl_files",
    #         ":write_on_build_gen",
    #     ],
    #     visibility = ["//visibility:public"]
    # )

def __run_on_dl(
        name,
        config_file
    ):

    py_binary(
        name = name + ".pybind_on_build_dl_exe",
        main = "pybind_on_build_dl.py",
        srcs = ["//shared/bazel/rules/python/pybind_generator:pybind_on_build_dl.py"],
        deps = [
            "//shared/bazel/rules/python/pybind_generator:pybind_gen_utils",
            "//shared/bazel/rules/python/pybind_generator:load_project_config",
        ],
        data = native.glob(["gen/**"])
    )

    __generate_on_build_dl_files(
        name = "generate_on_build_dl_files",
        tool = name + ".pybind_on_build_dl_exe",
        config_file = config_file,
        gen_dir = "_gen_on_build_dl",
    )

    write_source_files(
        name = "write_on_build_dl_files",
        files = {
            "generated/on_build_dl_files": ":generate_on_build_dl_files",
        },
        suggested_update_target = "//:write_python_on_build_dl_files",
        visibility = ["//visibility:public"],
        diff_test = False,
    )

def __run_on_build_gen(
        name,
        config_file,
    ):
    py_binary(
        name = name + ".generate_pybind_exe",
        main = "pybind_on_build_gen.py",
        srcs = ["//shared/bazel/rules/python/pybind_generator:pybind_on_build_gen.py"],
        deps = [
            # name + ".pkginfo",
            "//shared/bazel/rules/python/pybind_generator:pybind_gen_utils",
            "//shared/bazel/rules/python/pybind_generator:load_project_config",
        ],
        # data = [headers] + native.glob(["gen/**"]),
    )
    

    __generate_on_build_gen_files(
        name = "generate_on_build_gen",
        tool = name + ".generate_pybind_exe",
        config_file = config_file,
        gen_dir = "_gen_on_build",
        project_name = name,
    )

    write_source_files(
        name = "write_on_build_gen",
        files = {
            "generated": ":generate_on_build_gen",
        },
        suggested_update_target = "//:write_python_on_build_gen",
        visibility = ["//visibility:public"],
        diff_test = False,
    )


def __generate_on_build_dl_files_impl(ctx):
    output_dir = ctx.actions.declare_directory(ctx.attr.gen_dir)

    args = ctx.actions.args()
    args.add("--output_directory", output_dir.path)
    args.add("--config", ctx.files.config_file[0].path)

    ctx.actions.run(
        inputs = ctx.files.config_file,
        outputs = [output_dir],
        executable = ctx.executable.tool,
        arguments = [args],
    )

    return [DefaultInfo(files = depset([output_dir]))]

__generate_on_build_dl_files = rule(
    implementation = __generate_on_build_dl_files_impl,
    attrs = {
        "tool": attr.label(
            cfg = "exec",
            executable = True,
            mandatory=True,
        ),
        "config_file": attr.label(
            mandatory=True,
            allow_single_file = True,
        ),
        "gen_dir": attr.string(
            mandatory = True,
        ),
        "gen_files": attr.label(
            allow_files = True,
        )
    },
)


def __generate_on_build_gen_files_impl(ctx):
    output_dir = ctx.actions.declare_directory(ctx.attr.gen_dir)

    args = ctx.actions.args()
    args.add("--output_directory", output_dir.path)
    args.add("--config", ctx.files.config_file[0].path)
    args.add("--project_name", ctx.attr.project_name)

    ctx.actions.run(
        inputs = ctx.files.config_file,
        outputs = [output_dir],
        executable = ctx.executable.tool,
        arguments = [args],
    )

    return [DefaultInfo(files = depset([output_dir]))]

__generate_on_build_gen_files = rule(
    implementation = __generate_on_build_gen_files_impl,
    attrs = {
        "tool": attr.label(
            cfg = "exec",
            executable = True,
            mandatory=True,
        ),
        "config_file": attr.label(
            mandatory=True,
            allow_single_file = True,
        ),
        "gen_dir": attr.string(
            mandatory = True,
        ),
        "gen_files": attr.label(
            allow_files = True,
        ),
        "project_name": attr.string(
            mandatory = True,
        )
    },
)