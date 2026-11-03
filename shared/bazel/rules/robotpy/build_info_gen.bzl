load("@bazel_lib//lib:write_source_files.bzl", "write_source_files")
load("//shared/bazel/rules/robotpy:compatibility_select.bzl", "robotpy_compatibility_select")

def _generate_build_info(name, pyproject_toml, args, srcs, generated_file_name, suggested_update_target):
    """
    Runs the build file generator on a pyproject.toml file, and creates the targets to write the result back into the source tree.
    The generator chooses between a native library wrapper and a pybind / pure python library based on the contents of the toml file.
    """
    cmd = "$(location //shared/bazel/rules/robotpy:generate_pybind_build_file) --project_file=$(location " + pyproject_toml + ") --output_file=$(OUTS)"
    cmd += " --package_name=" + native.package_name()
    if args:
        cmd += " " + " ".join(args)

    native.genrule(
        name = "{}.gen_build_info".format(name),
        tools = ["//shared/bazel/rules/robotpy:generate_pybind_build_file"],
        srcs = [pyproject_toml] + srcs + ["//shared/bazel/rules/robotpy:jinja_templates"],
        outs = ["{}-generated_build_info.bzl".format(name)],
        cmd = cmd,
        tags = ["robotpy"],
        target_compatible_with = robotpy_compatibility_select(),
    )

    write_source_files(
        name = "{}.generate_build_info".format(name),
        files = {
            generated_file_name: "{}-generated_build_info.bzl".format(name),
        },
        visibility = ["//visibility:public"],
        suggested_update_target = suggested_update_target,
        tags = ["robotpy"],
        target_compatible_with = robotpy_compatibility_select(),
        diff_args = ["-u"],
    )

def generate_robotpy_native_wrapper_build_info(
        name,
        pyproject_toml,
        third_party_dirs = [],
        module_include_targets = {},
        native_srcs_root = "src/main/native/",
        generated_include_target = None,
        generated_include_root = "src/generated/main/native/include",
        include_license_file = True,
        include_third_party_notices = False):
    """
    This function will generate the bazel file necessary to declare a library that wraps a standard allwpilib library.

    Params:
        pyproject_toml - Path to the native library wrappers definition file
        third_party_dirs - Any directories under <native_srcs_root>thirdparty that should be used by semiwrap
        module_include_targets - Headers that live in a Bazel module rather than under
            <native_srcs_root>thirdparty (a vendored tree with its own MODULE.bazel is its own
            package, so globs cannot reach it). Maps a filegroup label exporting the header tree
            to the prefix to strip from its paths, e.g. {"@libuv//:include_files": "include"}
        native_srcs_root - Package-relative prefix under which the native cpp/include/thirdparty
            directories live, relative to wherever this macro is invoked from
        generated_include_target - Optional label pointing at a public filegroup exposing that project's
            generated headers
        generated_include_root - Package-relative prefix to strip from generated_include_target's sources
            so they land correctly under the wheel's include root. Defaults to the standard generated
            include directory; override when generated_include_target's sources live elsewhere (e.g.
            wpimath's generated protobuf headers live under src/generated/main/native/cpp).
    """
    extra_include_root_files = []
    if include_license_file:
        extra_include_root_files.append("//:LICENSE.md")
    if include_third_party_notices:
        extra_include_root_files.append("//:ThirdPartyNotices.txt")

    args = []
    if native_srcs_root:
        args.append("--native_srcs_root=" + native_srcs_root)
    if generated_include_target:
        args.append("--generated_include_target=" + generated_include_target)
        args.append("--generated_include_root=" + generated_include_root)
    if extra_include_root_files:
        args.append("--extra_include_root_files " + " ".join(extra_include_root_files))
    if third_party_dirs:
        args.append("--third_party_dirs " + " ".join(third_party_dirs))
    if module_include_targets:
        args.append("--module_include_targets " + " ".join([label + "=" + strip for label, strip in module_include_targets.items()]))

    _generate_build_info(
        name = name,
        pyproject_toml = pyproject_toml,
        args = args,
        srcs = [],
        generated_file_name = "robotpy_build_info.bzl",
        suggested_update_target = "//:write_robotpy_generated_native_files",
    )

def generate_robotpy_pybind_build_info(
        name,
        package_root_file,
        yaml_files = [],
        pkgcfgs = [],
        additional_srcs = [],
        generated_file_name = "robotpy_build_info.bzl",
        pyproject_toml = "pyproject.toml",
        stripped_include_prefix = None,
        yml_prefix = None):
    """
    This function will generate the bazel file necessary to build a pybind library with all of its extensions.

    Params:
        package_root_file - An __init__.py file used to key the semiwrap wrappers on the project root.
        yaml_files - All of the yaml files used by semi wrap to run library wrapping
        pkgcfgs - Local files used to trick semiwrap into thinking a library is installed
        additional_srcs - Any additional sources needed by the semiwrap process
        generated_file_name - Indicates the path of the auto-generated file
        pyproject_toml - Location of the pyproject.toml file that defines this project
        yml_prefix - Optional. Used in the event that the yml files are in a non-standard location
    """

    args = ["--package_root_file=" + package_root_file]
    if stripped_include_prefix:
        args.append("--stripped_include_prefix=" + stripped_include_prefix)
    if yml_prefix:
        args.append("--yml_prefix=" + yml_prefix)
    if pkgcfgs:
        args.append("--pkgcfgs " + " ".join(["$(locations " + x + ")" for x in pkgcfgs]))

    _generate_build_info(
        name = name,
        pyproject_toml = pyproject_toml,
        args = args,
        srcs = [package_root_file] + yaml_files + pkgcfgs + additional_srcs,
        generated_file_name = generated_file_name,
        suggested_update_target = "//:write_robotpy_generated_pybind_files",
    )
