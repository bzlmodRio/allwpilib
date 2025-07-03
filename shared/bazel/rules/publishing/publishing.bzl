load("@rules_pkg//pkg:zip.bzl", "pkg_zip")
load("@rules_python//python:defs.bzl", "py_binary")

def generate_maven_info_cmd(
        artifact,
        group_id,
        artifact_name,
        suffix = ""):
    """
    Helper function used to format the maven info into a CSV that can be parsed by the python tool.
    """
    return "$(locations {}),{},{},{} ".format(artifact, group_id, artifact_name, suffix)

def get_platform_suffix_cmd():
    return " --platform=" + select({
        "@bazel_tools//src/conditions:darwin": "osxuniversal",
        "@bazel_tools//src/conditions:linux_x86_64": "linuxx86-64",
        "@rules_bzlmodrio_toolchains//conditions:windows": "windowsx86-64",
        "@rules_bzlmodrio_toolchains//conditions:windows_arm64": "windowsarm64",
        "@rules_bzlmodrio_toolchains//conditions:windows_arm64_debug": "windowsarm64",
        "@rules_bzlmodrio_toolchains//conditions:windows_debug": "windowsx86-64",
        "@rules_bzlmodrio_toolchains//constraints/is_bookworm64:bookworm64": "linuxarm64",
        "@rules_bzlmodrio_toolchains//constraints/is_raspibookworm32:raspibookworm32": "linuxarm32",
        "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore": "linuxsystemcore",
    })

def get_debug_suffix_cmd():
    return " --debug_suffix=" + select({
        "@rules_bzlmodrio_toolchains//conditions:linux_x86_64_debug": "debug",
        "@rules_bzlmodrio_toolchains//conditions:osx_debug": "debug",
        "@rules_bzlmodrio_toolchains//conditions:windows_arm64_debug": "debug",
        "@rules_bzlmodrio_toolchains//conditions:windows_debug": "debug",
        "@rules_bzlmodrio_toolchains//constraints/is_bookworm64:bookworm64_debug": "debug",
        "@rules_bzlmodrio_toolchains//constraints/is_raspibookworm32:raspibookworm32_debug": "debug",
        "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore_debug": "debug",
        "//conditions:default": " ",
    })

def bundle_library_artifacts(
        name,
        group_id,
        library_base_name = "",
        cc_hdr_pkg = None,
        cc_src_pkg = None,
        cc_static_library_pkg = None,
        cc_shared_library_pkg = None,
        java_pkg = None,
        jni_pkg = None,
        add_cc_suffix = True):
    """
    Helper function for creating a file containing the info used to later publish maven libraries

    This generates a json file (name + "-maven-info.json") containing the relevant information to laster publish this library
    to maven coordinates. These can be gathered together to be published en masse with the wpilib_publish rule

    Params
        group_id: The groupd id used for determining the publihsing location
        library_base_name: The root name for all of the artifacts. Will be appended based on the artifact being published
        cc_hdr_pkg: Optional. A pkg_files target used to indcate there is are C++ headers to be published
        cc_src_pkg: Optional. A pkg_files target used to indicate there are C++ sources to be published
        cc_static_library_pkg: Optional. A pkg_files target used to indicate there is a compiled C++ library to be published
        jni_pkg: Optional. A pkg_files target used to indicate there is a compiled C++ JNI library to be published
    """
    srcs = []

    cmd = "$(locations //shared/bazel/rules/publishing:generate_maven_bundle) --output_file=$(OUTS) --maven_infos "
    maybe_cc_suffix = "-cpp" if add_cc_suffix else ""

    dbg_suffix = "##DEBUG##"
    platform = "##PLATFORM##"

    if cc_hdr_pkg:
        srcs.append(cc_hdr_pkg)
        cmd += generate_maven_info_cmd(cc_hdr_pkg, group_id, library_base_name + maybe_cc_suffix, "-headers")

    if cc_src_pkg:
        srcs.append(cc_src_pkg)
        cmd += generate_maven_info_cmd(cc_src_pkg, group_id, library_base_name + maybe_cc_suffix, "-sources")

    if cc_static_library_pkg:
        srcs.append(cc_static_library_pkg)
        cmd += generate_maven_info_cmd(cc_static_library_pkg, group_id, library_base_name + maybe_cc_suffix, "-" + platform + "static" + dbg_suffix)

    if cc_shared_library_pkg:
        srcs.append(cc_shared_library_pkg)
        cmd += generate_maven_info_cmd(cc_shared_library_pkg, group_id, library_base_name + maybe_cc_suffix, "-" + platform + dbg_suffix)

    if jni_pkg:
        fail()
        # srcs.append(jni_pkg)
        # cmd += "$(locations {}),{},{},{} ".format(jni_pkg, group_id, library_base_name + "-cpp", "jni-" + platform) # generate_maven_info_cmd()

    if java_pkg:
        srcs.append(java_pkg)
        cmd += generate_maven_info_cmd(java_pkg, group_id, library_base_name + "-java", suffix = "-sources")

    output_file = name + "-maven-info.json"

    cmd += get_platform_suffix_cmd()
    cmd += get_debug_suffix_cmd()

    native.genrule(
        name = name,
        srcs = srcs,
        outs = [output_file],
        cmd = cmd,
        tools = ["//shared/bazel/rules/publishing:generate_maven_bundle"],
        visibility = ["//visibility:public"],
        tags = ["manual"],
    )

def bundle_default_jni_library(
        name,
        library_base_name,
        group_id,
        library_name = None):
    """
    Helper function to help bundle files for a standard allwpilib JNI library.

    Due to the standard layout and naming convention of the JNI libraries, this function provides
    syntactic sugar to bundle all of the pieces relevant to a C++ / Java / JNI library to maven.
    """
    if library_name == None:
        library_name = library_base_name

    pkg_zip(
        name = "{}-shared-with-jni-zip".format(library_name),
        srcs = [
            "//:license_pkg_files",
            "//:third_party_notices_pkg_files",
            ":shared/{}-shared.pkg".format(library_name),
            ":shared/{}jni-shared.pkg".format(library_name),
        ],
        out = "{}-shared-with-jni.zip".format(library_name),
        tags = ["no-remote", "manual"],
    )

    bundle_library_artifacts(
        name = "publishing_bundle",
        group_id = group_id,
        library_base_name = library_base_name,
        cc_hdr_pkg = ":{}-hdrs-zip".format(library_name),
        cc_src_pkg = ":{}-srcs-zip".format(library_name),
        cc_static_library_pkg = ":static/{}-static-zip".format(library_name),
        cc_shared_library_pkg = ":{}-shared-with-jni-zip".format(library_name),
        java_pkg = ":lib{}-java-sources".format(library_name),
    )

def wpilib_publish(
        name,
        bundles):
    """
    Helper function that takes a list of bundled maven information and publishes it to an external location.

    This will take a list of json files containing maven publishing infomration, created by the
    //shared/bazel/rules/publishing:generate_maven_bundle target, and publish to a directory.

    See the "publish.py" library for a description of the available options

    Params
        bundles: A list of json files

    """
    py_binary(
        name = name,
        srcs = ["//shared/bazel/rules/publishing:publish.py"],
        args = ["--bundles "] + ["$(location " + x + ") " for x in bundles],
        data = bundles,
        deps = ["@rules_python//python/runfiles"],
        tags = ["no-remote", "manual"],
    )
