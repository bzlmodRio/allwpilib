"""Rule that renames built wheels to the platform tag they actually satisfy."""

def _robotpy_wheel_platform_tag_impl(ctx):
    out_dir = ctx.actions.declare_directory(ctx.label.name)

    args = ctx.actions.args()
    args.add("--output_dir", out_dir.path)
    args.add_all(ctx.files.wheels, before_each = "--wheel")

    ctx.actions.run(
        executable = ctx.executable._tool,
        arguments = [args],
        inputs = ctx.files.wheels,
        outputs = [out_dir],
        mnemonic = "FixWheelPlatformTag",
        progress_message = "Computing platform tags for %s" % ctx.label.name,
    )

    return [DefaultInfo(files = depset([out_dir]))]

robotpy_wheel_platform_tag = rule(
    implementation = _robotpy_wheel_platform_tag_impl,
    attrs = {
        "wheels": attr.label_list(
            allow_files = [".whl"],
            mandatory = True,
            doc = "py_wheel targets whose outputs should be re-tagged.",
        ),
        "_tool": attr.label(
            default = Label("//shared/bazel/rules/robotpy/wheel_platform_tag:fix_wheel_platform_tag"),
            executable = True,
            cfg = "exec",
        ),
    },
    doc = """
    Wraps a set of py_wheel outputs, renaming each (via auditwheel on Linux) to
    the manylinux/macOS platform tag it actually satisfies, based on the
    compiled extensions it contains. Produces a single directory containing
    all of the renamed .whl files, since the final tags aren't known until
    each wheel's contents are inspected at execution time. All wheels are
    combined into one directory (rather than one directory per wheel) so
    downstream packaging (pkg_files with REMOVE_BASE_DIRECTORY) can flatten
    them into a single destination without a rename collision.
    """,
)
