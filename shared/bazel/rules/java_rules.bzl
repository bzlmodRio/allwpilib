load("@rules_java//java:defs.bzl", "java_library", "java_test")
load("@rules_shell//shell:sh_test.bzl", "sh_test")
load("//shared/bazel/rules:packaging.bzl", "zip_java_srcs")
load("//shared/bazel/rules:publishing.bzl", "wpilib_maven_export")
load("//shared/bazel/rules/gen:native_libs.bzl", "wpilib_flatten_native_libs")

def _native_companion_label(label):
    if ":" not in label:
        # Shorthand label (e.g. "//wpiannotations") where the target name is
        # implicitly the last path segment.
        target = label.split("/")[-1]
        return label + ":" + target + ".native"
    return label + ".native"

def _has_native_companion(label):
    if not label.startswith(":"):
        # Cross-package reference: by repo convention every internal "-java"
        # target is built via wpilib_java_library, which always declares a
        # `.native` sibling.
        return True

    # Same-package reference: not every same-package target goes through
    # wpilib_java_library (e.g. plain java_binary/java_library targets like
    # the wpilibjExamples example/snippet/command/template binaries), so only
    # rely on the sibling if it was actually declared so far in this package.
    return native.existing_rule(label[1:] + ".native") != None

def _internal_native_companions(labels):
    """Maps a list of dep labels to their sibling `.native` filegroup labels.

    External (`@...`) labels are skipped: they either carry no native code, or
    (like the prebuilt OpenCV Java artifact) already attach their native
    library through a plain, non-self-referential attribute, so they
    propagate through ordinary dep merging without needing a `.native`
    sibling. Same-package labels without a declared `.native` sibling (e.g.
    plain java_binary/java_library targets) are skipped too: they carry no
    native code of their own, and whatever real native libraries they depend
    on are already reachable through the caller's other, wpilib_java_library-
    backed deps.
    """
    return [
        _native_companion_label(label)
        for label in labels
        if not label.startswith("@") and _has_native_companion(label)
    ]

def wpilib_java_library(
        name,
        maven_group_id,
        maven_artifact_name,
        tags = [],
        extra_source_pkgs = [],
        native_libs = [],
        deps = [],
        runtime_deps = [],
        **kwargs):
    tags = list(tags) if tags else []

    maven_coordinates = "{}:{}:$(WPILIB_VERSION)".format(maven_group_id, maven_artifact_name)
    tags.append("maven_coordinates=" + maven_coordinates)

    java_library(
        name = name,
        tags = tags,
        deps = deps,
        runtime_deps = runtime_deps,
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

    # A sibling target carrying this library's own native/JNI shared libraries
    # (if any) plus those of its dependencies, transitively. This must be a
    # separate target from `name`: a JNI library's own shared object is
    # compiled using headers generated from `name` itself (see
    # wpilib_jni_java_library/_jni_headers in jni_rules.bzl), so attaching it
    # directly to `name`'s own data/deps would create a dependency cycle.
    native.filegroup(
        name = name + ".native",
        testonly = kwargs.get("testonly"),
        visibility = kwargs.get("visibility"),
        srcs = native_libs + _internal_native_companions(deps) + _internal_native_companions(runtime_deps),
    )

def wpilib_java_junit5_test(
        name,
        deps = [],
        runtime_deps = [],
        args = [],
        tags = [],
        package = "org.wpilib",
        jvm_flags = [],
        data = [],
        size = None,
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

    # Collects every transitively-linked native/JNI shared library into one
    # flat directory, so the JVM/OS loader can resolve them uniformly
    # regardless of which Bazel package they were built in. Two channels feed
    # this: each dependency's `.native` sibling filegroup (see
    # wpilib_java_library above, for in-repo JNI modules whose own shared
    # library can't be reached through the ordinary dep graph without a
    # cycle), and the ordinary deps themselves (for things like the prebuilt
    # OpenCV Java artifact, which carries its native libraries through a
    # plain, non-self-referential attribute and so is already reachable via
    # normal transitive runfiles merging).
    native_libs_name = name + ".native-libs"
    wpilib_flatten_native_libs(
        name = native_libs_name,
        deps = deps + runtime_deps + _internal_native_companions(deps) + _internal_native_companions(runtime_deps),
        testonly = True,
        tags = ["manual"],
    )

    _inner_tags = ["allwpilib-build-java", "no-asan", "no-tsan", "no-ubsan"]
    java_impl_name = name + "_java_impl"

    # Core java_test: never bakes in -Djava.library.path itself, on any OS.
    # The sh_test wrapper below resolves the native-libs directory from the
    # runfiles manifest at test runtime and injects it via
    # --wrapper_script_flag (which the launcher applies after the params-file
    # jvm_flags, so it always wins). This avoids relying on
    # ${CLASSLOADER_PREFIX_PATH} substitution, which is only correct when
    # this java_test is invoked as the top-level test process; nested inside
    # the sh_test wrapper it is not reliable.
    # Tagged manual so //... wildcard expansion skips it; the sh_test below is
    # the only entry point users interact with.
    java_test(
        name = java_impl_name,
        deps = deps + junit_deps,
        runtime_deps = runtime_deps + junit_runtime_deps,
        data = data + [":" + native_libs_name],
        # Gradle's Test task enables assertions by default (unlike JavaExec,
        # where it defaults to false); match that here since some tests (e.g.
        # HAL.initialize) rely on `assert` for setup, and use_testrunner =
        # False below means Bazel's own -ea injection never kicks in.
        # --enable-native-access=ALL-UNNAMED matches javacommon.gradle's test
        # task, silencing the JEP 472 restricted-method warning that
        # System.loadLibrary triggers via RuntimeLoader.
        # junit.jupiter.extensions.autodetection.enabled=true also matches
        # javacommon.gradle: it's required for ServiceLoader-registered
        # extensions (e.g. wpilibj/commandsv2/commandsv3's
        # MockHardwareExtension, declared only via
        # META-INF/services/org.junit.jupiter.api.extension.Extension) to
        # actually run, since Jupiter ignores that file by default.
        jvm_flags = jvm_flags + [
            "-ea",
            "--enable-native-access=ALL-UNNAMED",
        ],
        args = args + ["--select-package", package],
        main_class = "org.junit.platform.console.ConsoleLauncher",
        use_testrunner = False,
        testonly = True,
        tags = tags + ["manual"] + _inner_tags,
        **kwargs
    )

    # Primary test target (all platforms). The wrapper reads
    # RUNFILES_MANIFEST_FILE to obtain the absolute native-libs path and
    # injects it via --wrapper_script_flag before invoking the java_impl
    # binary, on every OS.  On Windows the wrapper additionally prepends the
    # native-libs directory to PATH so the DLL loader can resolve transitive
    # dependencies.
    sh_test(
        name = name,
        srcs = ["//shared/bazel/rules/gen:java_test_wrapper.sh"],
        args = args + ["--select-package", package],
        deps = ["@bazel_tools//tools/bash/runfiles"],
        env = {
            "JAVA_TEST_RLOCATION": "_main/" + native.package_name() + "/" + java_impl_name,
            "NATIVE_LIBS_RLOCATION": "_main/" + native.package_name() + "/" + native_libs_name,
        },
        size = size or "small",
        data = [":" + java_impl_name, ":" + native_libs_name],
        testonly = True,
        visibility = kwargs.get("visibility"),
        tags = tags + _inner_tags,
    )
