"""Macros for the per-folder wpilibjExamples BUILD files.

Each is called from wpilibjExamples/src/{main,test}/java/org/wpilib/<kind>/<name>.
"""

load("@rules_java//java:defs.bzl", "java_binary", "java_library")
load("//shared/bazel/rules:java_rules.bzl", "wpilib_java_junit5_test")

visibility(["//wpilibjExamples/..."])

def wpilib_java_example(name, deps = []):
    """
    Creates a runnable WPILib Java example, snippet, or template.

    The sources are compiled without the wpilibjExamples module-info.java, so
    each folder builds independently of the others. The Epilogue annotation
    processor also writes META-INF/services entries, which is what the
    Epilogue service loader uses outside of a named module.

    Targets:
      {name}-lib: the compiled sources
      {name}: the robot program, launched through org.wpilib.Executor

    Args:
      name: the folder name
      deps: the libraries the sources use directly
    """
    kind = native.package_name().split("/")[-2]

    native.filegroup(
        name = "sources",
        srcs = native.glob(["**/*.java"]),
        visibility = ["//wpilibjExamples/src/main/java/org/wpilib/{}:__pkg__".format(kind)],
    )

    java_library(
        name = name + "-lib",
        srcs = [":sources"],
        plugins = ["//epilogue-processor/src/main/java:plugin"],
        tags = ["wpi-example"],
        visibility = ["//wpilibjExamples/src/test/java/org/wpilib/{}/{}:__pkg__".format(kind, name)],
        deps = deps,
    )

    java_binary(
        name = name,
        args = ["org.wpilib.{}.{}.Robot".format(kind, name)],
        main_class = "org.wpilib.Executor",
        tags = ["wpi-example"],
        runtime_deps = [
            ":" + name + "-lib",
            "//wpilibjExamples/src/main/java:executor",
        ],
    )

def wpilib_java_command(name, deps = []):
    """
    Creates a library for a WPILib Java command-based class template.

    Args:
      name: the folder name
      deps: the libraries the sources use directly
    """
    native.filegroup(
        name = "sources",
        srcs = native.glob(["**/*.java"]),
        visibility = ["//wpilibjExamples/src/main/java/org/wpilib/commands:__pkg__"],
    )

    java_library(
        name = name,
        srcs = [":sources"],
        tags = ["wpi-example"],
        deps = deps,
    )

def wpilib_java_example_test(name, deps = []):
    """
    Creates the JUnit tests for the example or snippet of the same name.

    Args:
      name: the folder name
      deps: the libraries the tests use directly, besides the code under test
    """
    kind = native.package_name().split("/")[-2]

    native.filegroup(
        name = "sources",
        srcs = native.glob(["**/*.java"]),
        visibility = ["//wpilibjExamples/src/test/java/org/wpilib/{}:__pkg__".format(kind)],
    )

    wpilib_java_junit5_test(
        name = name,
        srcs = [":sources"],
        package = "org.wpilib.{}.{}".format(kind, name),
        tags = ["wpi-example"],
        deps = ["//wpilibjExamples/src/main/java/org/wpilib/{}/{}:{}-lib".format(kind, name, name)] + deps,
    )
