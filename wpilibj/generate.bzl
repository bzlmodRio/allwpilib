def __generate_wpilibj_impl(ctx):
    output_dir = ctx.actions.declare_directory("_gendir")

    args = ctx.actions.args()
    args.add("--output_directory", output_dir.path)
    args.add("--template_root", "wpilibj/src/generate")

    ctx.actions.run(
        inputs = ctx.attr._templates.files,
        outputs = [output_dir],
        executable = ctx.executable._tool,
        arguments = [args],
    )

    return [DefaultInfo(files = depset([output_dir]))]

generate_wpilibj = rule(
    implementation = __generate_wpilibj_impl,
    attrs = {
        "_templates": attr.label(
            default = Label("//wpilibj/src/generate:templates"),
        ),
        "_tool": attr.label(
            default = Label("//wpilibj:generate_wpilibj_py"),
            cfg = "exec",
            executable = True,
        ),
    },
)
