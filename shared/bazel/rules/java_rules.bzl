load("@rules_java//java:defs.bzl", "java_binary", "java_library")

def wpilib_java_library(
        name,
        maven_group_id = None,
        maven_artifact_name = None,
        tags = [],
        **kwargs):
    tags = list(tags) if tags else []

    if maven_artifact_name and maven_group_id:
        maven_coordinates = "{}:{}:$(WPILIB_VERSION)".format(maven_group_id, maven_artifact_name)
    else:
        maven_coordinates = ""
        fail()
    tags.append("maven_coordinates=" + maven_coordinates)

    java_library(
        name = name,
        tags = tags,
        **kwargs
    )

    # wpilib_maven_export(
    #     name = "{}_publish".format(name),
    #     classifier_artifacts = {"sources": ":lib{}-sources.jar".format(name)},
    #     lib_name = name,
    #     maven_coordinates = maven_coordinates,
    #     visibility = ["//visibility:public"],
    # )

def wpilib_java_junit5_test(
        name,
        deps = [],
        runtime_deps = [],
        args = [],
        tags = [],
        package = "edu",
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

    # TODO - replace with java_test once shared libraries are hooked up.
    java_binary(
        name = name,
        deps = deps + junit_deps,
        runtime_deps = runtime_deps + junit_runtime_deps,
        args = args + ["--select-package", package],
        main_class = "org.junit.platform.console.ConsoleLauncher",
        use_testrunner = False,
        testonly = True,
        tags = tags + ["allwpilib-build-java", "no-asan", "no-tsan", "no-ubsan"],
        **kwargs
    )
