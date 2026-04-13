load("@rules_java//java:defs.bzl", "java_binary", "java_library", "java_test")
load("//shared/bazel/rules:packaging.bzl", "zip_java_srcs")
load("//shared/bazel/rules:publishing.bzl", "wpilib_maven_export")

def wpilib_java_library(
        name,
        maven_group_id,
        maven_artifact_name,
        tags = [],
        extra_source_pkgs = [],
        **kwargs):
    tags = list(tags) if tags else []

    maven_coordinates = "{}:{}:$(WPILIB_VERSION)".format(maven_group_id, maven_artifact_name)
    tags.append("maven_coordinates=" + maven_coordinates)

    java_library(
        name = name,
        tags = tags,
        **kwargs
    )

    zip_java_srcs(name = name, extra_pkgs = extra_source_pkgs)

    wpilib_maven_export(
        name = "{}_publish".format(name),
        classifier_artifacts = {"sources": ":lib{}-sources.jar".format(name)},
        lib_name = name,
        maven_coordinates = maven_coordinates,
        visibility = ["//visibility:public"],
    )


def get_dynamic_deps(target):
    shared_lib_native_deps = []

    if CcInfo in target:
        for linker_input in target[CcInfo].linking_context.linker_inputs.to_list():
            for library in linker_input.libraries:
                if library.dynamic_library and not library.static_library:
                    shared_lib_native_deps.append(library.dynamic_library)
    if JavaInfo in target:
        for library in target[JavaInfo].transitive_native_libraries.to_list():
            if library.dynamic_library and not library.static_library:
                shared_lib_native_deps.append(library.dynamic_library)

    return shared_lib_native_deps

def _symlink_java_native_libraries_impl(ctx):    
    shared_libraries = []
    for dep in ctx.attr.deps:
        shared_libraries += get_dynamic_deps(dep)
        if CcSharedLibraryInfo in dep:
            for lib in dep[OutputGroupInfo].main_shared_library_output.to_list():
                shared_libraries.append(lib)

    symlinks = []
    for lib in shared_libraries:
               out = ctx.actions.declare_file(ctx.attr.output_directory + "/" + lib.basename)
               
               if out not in symlinks:
                    ctx.actions.symlink(output = out, target_file = lib)
                    symlinks.append(out)

    return [DefaultInfo(files = depset(symlinks), runfiles = ctx.runfiles(files = symlinks))]

_symlink_java_native_libraries = rule(
    attrs = {
        "deps": attr.label_list(mandatory = True),
        "output_directory": attr.string(mandatory = True),
    },
    implementation = _symlink_java_native_libraries_impl,
)


def _get_runfiles_suffix(name):
    lbl = Label(native.repository_name() + "//" + native.package_name() + ":" + name)

    runfiles_suffix = "__main__"
    if str(lbl).startswith("@@"):
        runfiles_suffix = "_main"

    return runfiles_suffix



def wpilib_java_junit5_test(
        name,
        deps = [],
        runtime_deps = [],
        args = [],
        tags = [],
        data = [],
        jvm_flags = [],
        package = "org",
        **kwargs):
    """
    Convenience helper to make a junit5 test
    """
    junit_deps = [
        "@maven//:org_junit_jupiter_junit_jupiter_api",
        "@maven//:org_junit_jupiter_junit_jupiter_params",
        "@maven//:org_junit_jupiter_junit_jupiter_engine",
    ]

    junit_runtime_deps = [
        "@maven//:org_junit_platform_junit_platform_console",
    ]
    
    native_shared_libraries_symlink = name + ".symlink_native"
    extracted_native_dir = "extracted_native"
    full_extracted_native_dir = native.package_name() + "/extracted_native"
    _symlink_java_native_libraries(
        name = native_shared_libraries_symlink,
        deps = deps + runtime_deps,
        output_directory = select({
            "@bazel_tools//src/conditions:windows": name + ".exe.runfiles/" + _get_runfiles_suffix(name),
            "//conditions:default": extracted_native_dir,
        }),
        tags = ["manual"],
        testonly = True,
    )

    # TODO - replace with java_test once shared libraries are hooked up.
    java_test(
        name = name,
        deps = deps + junit_deps,
        runtime_deps = runtime_deps + junit_runtime_deps,
        args = args + ["--select-package", package],
        main_class = "org.junit.platform.console.ConsoleLauncher",
        use_testrunner = False,
        testonly = True,
        tags = tags + ["allwpilib-build-java", "no-asan", "no-tsan", "no-ubsan"],
        data = data + [native_shared_libraries_symlink],
        jvm_flags = jvm_flags + select({
            "@bazel_tools//src/conditions:windows": ["-Djava.library.path=."],
            "@rules_bzlmodrio_toolchains//constraints/combined:is_unix": ["-Djava.library.path=" + full_extracted_native_dir],
        }),
        env = select({
            "@bazel_tools//src/conditions:darwin": {"DYLD_LIBRARY_PATH": full_extracted_native_dir, "LD_LIBRARY_PATH": full_extracted_native_dir},
            "@bazel_tools//src/conditions:windows": {},
            "@rules_bzlmodrio_toolchains//constraints/combined:is_linux": {},
        }),
        **kwargs
    )
