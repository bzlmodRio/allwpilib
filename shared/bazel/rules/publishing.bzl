load("@rules_pkg//:mappings.bzl", "pkg_files")
load("@rules_pkg//:pkg.bzl", "pkg_zip")
load("@rules_python//python:defs.bzl", "py_binary")

def assemble_headers(
        name,
        maven_coordinates,
        src_directories,
        extra_pkg_files = [],
        package_file_name = None,
        include_license_files = False,
        remapped_dirs = []):
    extra_pkg_files = list(extra_pkg_files)
    for i, x in enumerate(src_directories):
        extra_name = name + ".extra_pkg" + str(i)

        pkg_files(
            name = extra_name,
            srcs = native.glob([x + "/**"]),
            strip_prefix = x,
        )
        extra_pkg_files.append(extra_name)

    for i, (include_dir, remapped_dir) in enumerate(remapped_dirs):
        extra_name = name + ".remapped_pkg" + str(i)

        pkg_files(
            name = extra_name,
            srcs = native.glob([include_dir + "/**"]),
            strip_prefix = include_dir,
            prefix = remapped_dir,
        )
        extra_pkg_files.append(extra_name)

    pkg_zip(
        name = name,
        srcs = extra_pkg_files + (["//:liscense_pkg_files"] if include_license_files else []),
        # package_dir = "wpi",
        tags = ["no-remote"],
        package_file_name = package_file_name,
    )

def bundle_artifacts(
        name,
        artifacts):
    output_file = name + "-maven-info.json"
    cmd = "$(locations //shared/bazel/rules:combine_artifacts) $(OUTS) "
    srcs = []
    for coordinate, artifact in artifacts:
        cmd += coordinate + " $(locations " + artifact + ") "
        srcs.append(artifact)

    native.genrule(
        name = name,
        srcs = srcs,
        outs = [output_file],
        cmd = cmd,
        tools = ["//shared/bazel/rules:combine_artifacts"],
        visibility = ["//visibility:public"],
    )

def publish_artifacts(
        name,
        artifact_bundles):
    # print(artifact_bundles)
    # cmd = "$(location //shared/bazel/rules:publish) output " + " ".join(["$(location " + x + ") " for x in artifact_bundles])
    # print(cmd)
    # native.genrule(
    #     name = name,
    #     srcs = artifact_bundles,
    #     outs = ["dummy.txt"],
    #     cmd = cmd,
    #     tools = ["//shared/bazel/rules:publish"]
    # )

    py_binary(
        name = name,
        srcs = ["//shared/bazel/rules:publish.py"],
        args = ["$(location " + x + ") " for x in artifact_bundles],
        data = artifact_bundles,
        deps = [
            # requirement("somerequirement"),
        ],
    )

    # print(artifact_bundles)
    # native.py_binary(
    #     name = "publish",
    #     srcs = ["//shared/bazel/rules:publish.py"],
    #     args = [Label(artifact_bundles[0]).]
    # )

def assemble_java_library(
        base_name,
        src_directories = []):
    assemble_headers(
        name = base_name + ".java_srcs_pkg",
        maven_coordinates = None,
        src_directories = src_directories,
        # package_file_name = "wpiutil-sources.jar"
    )

def assemble_cpp_library(
        base_name,
        static_library_pkg_files,
        shared_library_pkg_files,
        hdr_directories = [],
        src_directories = [],
        extra_src_pkg_files = [],
        remapped_cpp_src_dirs = [],
        include_license_files_in_srcs=False):
    assemble_headers(
        name = base_name + ".hdrs_pkg",
        maven_coordinates = None,
        src_directories = hdr_directories,
        include_license_files = include_license_files_in_srcs,
    )

    assemble_headers(
        name = base_name + ".srcs_pkg",
        maven_coordinates = None,
        src_directories = src_directories,
        extra_pkg_files = extra_src_pkg_files,
        remapped_dirs = remapped_cpp_src_dirs,
        include_license_files = include_license_files_in_srcs,
    )

    if static_library_pkg_files:
        pkg_zip(
            name = base_name + ".static_pkg",
            srcs = [static_library_pkg_files, "//:liscense_pkg_files"],
            tags = ["no-remote"],
        )

    if shared_library_pkg_files:
        pkg_zip(
            name = base_name + ".shared_pkg",
            srcs = [
                shared_library_pkg_files,
                "//:liscense_pkg_files",
                # base_name + "jni.pkg_files"
            ],
            tags = ["no-remote"],
        )

def publish_default_jni_libraries(base_name, group_id, extra_cpp_hdr_dirs = [], extra_cpp_src_dirs = [], extra_java_src_dirs = [], remapped_cpp_src_dirs = []):
    if "hal" in base_name:
        HACK = "wpiHal"
    else:
        HACK = base_name

    assemble_cpp_library(
        base_name = base_name,
        static_library_pkg_files = HACK + ".static_pkg_files",
        shared_library_pkg_files = HACK + ".shared_pkg_files",
        hdr_directories = ["src/main/native/include"] + extra_cpp_hdr_dirs,
        src_directories = ["src/main/native/cpp"] + extra_cpp_src_dirs,
        extra_src_pkg_files = [base_name + "-java.jni_header_pkg_files"],
        remapped_cpp_src_dirs = remapped_cpp_src_dirs,
    )

    assemble_java_library(
        base_name = base_name,
        src_directories = ["src/main/java"] + extra_java_src_dirs,
    )

    pkg_files(
        name = base_name + ".jni_jar_pkg_files",
        srcs = [":" + HACK + "jni"],
        prefix = "linux/x86-64",
    )
    pkg_zip(
        name = base_name + ".jni_jar_pkg",
        srcs = [base_name + ".jni_jar_pkg_files", "//:liscense_pkg_files"],
        tags = ["no-remote"],
    )

    bundle_artifacts(
        name = base_name + "-publishing",
        artifacts = [
            (group_id + ":" + base_name + "-cpp:-headers", base_name + ".hdrs_pkg"),
            (group_id + ":" + base_name + "-cpp:-sources", base_name + ".srcs_pkg"),
            (group_id + ":" + base_name + "-cpp:-{platform}", base_name + ".shared_pkg"),
            (group_id + ":" + base_name + "-cpp:-{platform}static", base_name + ".static_pkg"),
            (group_id + ":" + base_name + "-jni:-{platform}", base_name + ".jni_jar_pkg"),
            (group_id + ":" + base_name + "-java:-sources", base_name + ".java_srcs_pkg"),
        ],
    )
