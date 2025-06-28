load("@aspect_bazel_lib//lib:write_source_files.bzl", "write_source_files")

def generate_robotpy_native_wrapper_build_info(name, pyproject_toml, third_party_dirs = []):
    cmd = "$(location //shared/bazel/rules/robotpy:generate_native_build_file) --output_file=$(OUTS)"
    cmd += " --project_cfg=$(location " + pyproject_toml + ")"
    if third_party_dirs:
        cmd += " --third_party_dirs "
        for d in third_party_dirs:
            cmd += " " + d
    native.genrule(
        name = "{}.gen_build_info".format(name),
        tools = ["//shared/bazel/rules/robotpy:generate_native_build_file"],
        srcs = [pyproject_toml],
        outs = ["{}-generated_build_info.bzl".format(name)],
        cmd = cmd,
    )

    write_source_files(
        name = "{}.generate_build_info".format(name),
        files = {
            "robotpy_native_build_info.bzl": "{}-generated_build_info.bzl".format(name),
        },
        visibility = ["//visibility:public"],
        suggested_update_target = "//:write_robotpy_generated_native_files",
    )

def generate_robotpy_pybind_build_info(
        name,
        package_root_file,
        yaml_files = [],
        pkgcfgs = [],
        additional_srcs = [],
        generated_file_name = "robotpy_pybind_build_info.bzl",
        pyproject_toml = "src/main/python/pyproject.toml",
        stripped_include_prefix = None,
        yml_prefix = None):
    pass

    cmd = "$(location //shared/bazel/rules/robotpy:generate_pybind_build_file2) --project_file=$(location " + pyproject_toml + ") --output_file=$(OUTS)"

    cmd += " --package_root_file=" + package_root_file
    if stripped_include_prefix:
        cmd += " --stripped_include_prefix=" + stripped_include_prefix
    if stripped_include_prefix:
        cmd += " --yml_prefix=" + yml_prefix

    # TODO kwargs

    if pkgcfgs:
        cmd += " --pkgcfgs "
        for x in pkgcfgs:
            cmd += " $(location " + x + ")"

    native.genrule(
        name = "{}.gen_build_info".format(name),
        tools = ["//shared/bazel/rules/robotpy:generate_pybind_build_file2"],
        srcs = [pyproject_toml, package_root_file] + yaml_files + pkgcfgs + additional_srcs + ["//shared/bazel/rules/robotpy:jinja_templates"],
        # srcs = local_libraries + [pyproject_toml] + yaml_files + header_packages + additional_srcs,
        outs = ["{}-generated_build_info.bzl".format(name)],
        cmd = cmd,
    )

    write_source_files(
        name = "{}.generate_build_info".format(name),
        files = {
            generated_file_name: "{}-generated_build_info.bzl".format(name),
        },
        suggested_update_target = "//:write_robotpy_generated_pybind_files",
        visibility = ["//visibility:public"],
    )
