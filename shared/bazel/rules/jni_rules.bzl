load("@bazel_tools//tools/cpp:toolchain_utils.bzl", "find_cpp_toolchain")
load("@rules_cc//cc:defs.bzl", "cc_library")
load("@rules_cc//cc/common:cc_common.bzl", "cc_common")
load("@rules_cc//cc/common:cc_info.bzl", "CcInfo")
load("@rules_java//java/common:java_info.bzl", "JavaInfo")
load("@rules_pkg//:mappings.bzl", "filter_directory")
load("//shared/bazel/rules:java_rules.bzl", "wpilib_java_library")
load("//shared/bazel/rules:packaging.bzl", "zip_java_srcs")
load("//shared/bazel/rules:publishing.bzl", "wpilib_maven_export")

def _jni_headers_impl(ctx):
    include_dir = ctx.actions.declare_directory(ctx.attr.name + ".h")
    native_headers_jar = ctx.attr.lib[JavaInfo].outputs.native_headers
    args = ["xf", native_headers_jar.path, "-d", include_dir.path]

    ctx.actions.run(
        inputs = [native_headers_jar],
        tools = [ctx.executable._zipper],
        outputs = [include_dir],
        executable = ctx.executable._zipper.path,
        arguments = args,
    )

    cc_toolchain = find_cpp_toolchain(ctx)
    feature_configuration = cc_common.configure_features(
        ctx = ctx,
        cc_toolchain = cc_toolchain,
        requested_features = ctx.features,
        unsupported_features = ctx.disabled_features,
    )
    compilation_context, _ = cc_common.compile(
        name = ctx.attr.name,
        actions = ctx.actions,
        feature_configuration = feature_configuration,
        cc_toolchain = cc_toolchain,
        public_hdrs = [include_dir],
        quote_includes = [include_dir.path],
    )
    cc_info_with_jni = cc_common.merge_cc_infos(
        direct_cc_infos = [
            CcInfo(compilation_context = compilation_context),
            ctx.attr.jni[CcInfo],
        ],
    )

    return [
        DefaultInfo(files = depset([include_dir])),
        cc_info_with_jni,
    ]

_jni_headers = rule(
    implementation = _jni_headers_impl,
    attrs = {
        "jni": attr.label(mandatory = True),
        "lib": attr.label(
            mandatory = True,
            providers = [JavaInfo],
        ),
        "_cc_toolchain": attr.label(default = Label("@bazel_tools//tools/cpp:current_cc_toolchain")),
        "_zipper": attr.label(
            executable = True,
            cfg = "exec",
            default = Label("@bazel_tools//tools/zip:zipper"),
        ),
    },
    fragments = ["cpp"],
    incompatible_use_toolchain_transition = True,
    provides = [CcInfo],
    toolchains = ["@bazel_tools//tools/cpp:toolchain_type"],
)


def _merge_default_infos(ctx, infos):
    return DefaultInfo(
        files = depset(transitive = [info.files for info in infos]),
        runfiles = ctx.runfiles(
            transitive_files = depset(
                transitive = [info.default_runfiles.files for info in infos] + [info.data_runfiles.files for info in infos],
            ),
        ),
    )

def _merge_java_infos_impl(ctx):
    return [
        _merge_default_infos(ctx, [lib[DefaultInfo] for lib in ctx.attr.libs + ctx.attr.native_libs]),
        java_common.merge([lib[JavaInfo] for lib in ctx.attr.libs]),
        cc_common.merge_cc_infos(direct_cc_infos = [lib[CcInfo] for lib in ctx.attr.native_libs]),
        coverage_common.instrumented_files_info(
            ctx,
            dependency_attributes = ["libs"],
        ),
    ]

merge_java_infos = rule(
    implementation = _merge_java_infos_impl,
    attrs = {
        "libs": attr.label_list(
            providers = [JavaInfo],
        ),
        "native_libs": attr.label_list(
            providers = [CcInfo],
        ),
    },
    provides = [JavaInfo],
)

def wpilib_jni_java_library(
        name,
        maven_group_id,
        maven_artifact_name,
        native_libs = [],
        tags = [],
        extra_source_pkgs = [],
        **java_library_args):
        
    tags = list(tags) if tags else []

    maven_coordinates = "{}:{}:$(WPILIB_VERSION)".format(maven_group_id, maven_artifact_name)
    tags.append("maven_coordinates=" + maven_coordinates)

    visibility = java_library_args.pop("visibility", default = None)
    testonly = java_library_args.pop("testonly", default = None)
    headers_name = name + ".hdrs"

    intermediate_name = name + ".intermediate"

    native.java_library(
        name = intermediate_name,
        visibility = ["//visibility:private"],
        testonly = testonly,
        tags = tags,
        **java_library_args
    )

    jni = "@rules_bzlmodrio_toolchains//jni"
    _jni_headers(
        name = headers_name,
        jni = jni,
        lib = ":" + intermediate_name,
        testonly = testonly,
        visibility = visibility,
    )

    # Expose a pkg_files with the JNI generated header in it.
    filter_directory(
        name = name + "-jni-hdrs-pkg",
        src = headers_name,
        excludes = ["MANIFEST.MF"],
        outdir_name = "jni/",
    )

    merge_java_infos(
        name = name,
        libs = [":" + intermediate_name],
        native_libs = [x for x in native_libs],
        tags = tags,
        testonly = testonly,
        visibility = visibility,
    )

    zip_java_srcs(name = name, extra_pkgs = extra_source_pkgs)

    wpilib_maven_export(
        name = "{}_publish".format(name),
        classifier_artifacts = {"sources": ":lib{}-sources.jar".format(name)},
        lib_name = name,
        maven_coordinates = maven_coordinates,
        visibility = ["//visibility:public"],
    )

def wpilib_jni_cc_library(
        name,
        deps = [],
        java_dep = None,
        **kwargs):
    jni = "@rules_bzlmodrio_toolchains//jni"

    if java_dep[0] != ":":
        fail("java_dep", java_dep, "should start with a :")

    cc_library(
        name = name,
        deps = [jni, java_dep + ".hdrs"] + deps,
        **kwargs
    )
