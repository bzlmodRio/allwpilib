load("@rules_java//java:defs.bzl", "java_binary", "java_library")
load("@rules_pkg//:mappings.bzl", "pkg_files")
load("@rules_pkg//:pkg.bzl", "pkg_zip")
load("//shared/bazel/rules:java_rules.bzl", "wpilib_java_junit5_test")

def first_level_folders(paths, prefix):
    output = {}
    for path in paths:
        rel = path[len(prefix):]
        output[rel.split("/", 1)[0]] = True
    return sorted(output.keys())

def _package_type(package_type):
    pkg_files(
        name = package_type + "-pkg",
        srcs = native.glob(["src/main/java/org/wpilib/" + package_type + "/**"]),
        strip_prefix = "src/main/java/org/wpilib",
    )

    pkgs = ["//:license_pkg_files", ":" + package_type + "-pkg"]
    if package_type == "examples":
        pkg_files(
            name = package_type + "-tests-pkg",
            srcs = native.glob(["src/test/java/org/wpilib/" + package_type + "/**"]),
            strip_prefix = "src/test/java/org/wpilib/" + package_type,
            prefix = "examples_test",
        )
        pkgs.append(package_type + "-tests-pkg")

    pkg_zip(
        name = package_type + "-zip",
        srcs = pkgs,
        tags = ["manual"],
    )

def build_examples(folders, halsim_deps):
    _package_type("examples")

    for folder in folders:
        java_binary(
            name = folder + "-example",
            srcs = native.glob(["src/main/java/org/wpilib/examples/" + folder + "/**/*.java"]),
            main_class = "org/wpilib/examples/" + folder + "/Main",
            plugins = [
                "//epilogue-processor/src/main/java:plugin",
            ],
            deps = [
                "//apriltag/src/main/java:apriltag-java",
                "//cameraserver/src/main/java:cameraserver-java",
                "//cscore/src/main/java:cscore-java",
                "//fields/src/main/java:fields-java",
                "//hal/src/main/java:hal-java",
                "//ntcore/src/main/java:ntcore-java",
                "//wpimath/src/main/java:wpimath-java",
                "//wpilibj/src/main/java:wpilibj-java",
                "//commandsv2/src/main/java:commandsv2-java",
                "//commandsv3/src/main/java:commandsv3-java",
                "//wpiutil/src/main/java:wpiutil-java",
                "//romiVendordep/src/main/java:romiVendordep-java",
                "//xrpVendordep/src/main/java:xrpVendordep-java",
                "//wpiunits/src/main/java:wpiunits-java",
                "//epilogue-runtime/src/main/java:epilogue-java",
                "@bzlmodrio-opencv//libraries/java/opencv",
            ],
            tags = ["wpi-example"],
        )

def build_commands(folders):
    _package_type("commands")

    for folder in folders:
        java_library(
            name = folder + "-command",
            srcs = native.glob(["src/main/java/org/wpilib/commands/" + folder + "/**/*.java"]),
            deps = [
                "//hal/src/main/java:hal-java",
                "//wpilibj/src/main/java:wpilibj-java",
                "//commandsv2/src/main/java:commandsv2-java",
                "//wpimath/src/main/java:wpimath-java",
            ],
            tags = ["wpi-example"],
        )

def build_snippets(folders):
    _package_type("snippets")

    for folder in folders:
        java_library(
            name = folder + "-snippet",
            srcs = native.glob(["src/main/java/org/wpilib/snippets/" + folder + "/**/*.java"]),
            plugins = [
                "//epilogue-processor/src/main/java:plugin",
            ],
            deps = [
                "//apriltag/src/main/java:apriltag-java",
                "//cameraserver/src/main/java:cameraserver-java",
                "//cscore/src/main/java:cscore-java",
                "//fields/src/main/java:fields-java",
                "//hal/src/main/java:hal-java",
                "//ntcore/src/main/java:ntcore-java",
                "//wpimath/src/main/java:wpimath-java",
                "//wpilibj/src/main/java:wpilibj-java",
                "//commandsv2/src/main/java:commandsv2-java",
                "//commandsv3/src/main/java:commandsv3-java",
                "//wpiutil/src/main/java:wpiutil-java",
                "//romiVendordep/src/main/java:romiVendordep-java",
                "//xrpVendordep/src/main/java:xrpVendordep-java",
                "//wpiunits/src/main/java:wpiunits-java",
                "//epilogue-runtime/src/main/java:epilogue-java",
                "@bzlmodrio-opencv//libraries/java/opencv",
            ],
            tags = ["wpi-example"],
        )

def build_templates(folders):
    _package_type("templates")

    for folder in folders:
        java_library(
            name = folder + "-template",
            srcs = native.glob(["src/main/java/org/wpilib/templates/" + folder + "/**/*.java"]),
            plugins = [
                "//epilogue-processor/src/main/java:plugin",
            ],
            deps = [
                "//hal/src/main/java:hal-java",
                "//wpilibj/src/main/java:wpilibj-java",
                "//commandsv2/src/main/java:commandsv2-java",
                "//commandsv3/src/main/java:commandsv3-java",
                "//wpimath/src/main/java:wpimath-java",
                "//wpiutil/src/main/java:wpiutil-java",
                "//epilogue-runtime/src/main/java:epilogue-java",
                "//xrpVendordep/src/main/java:xrpVendordep-java",
                "//wpiunits/src/main/java:wpiunits-java",
            ],
            tags = ["wpi-example"],
        )

def build_tests(example_test_folders, snippet_test_folders):
    for folder in example_test_folders:
        wpilib_java_junit5_test(
            name = folder + "-test",
            srcs = native.glob(["src/test/java/org/wpilib/examples/" + folder + "/**/*.java"]),
            plugins = [
                "//epilogue-processor/src/main/java:plugin",
            ],
            deps = [
                ":" + folder + "-example",
                "//hal/src/main/java:hal-java",
                "//ntcore/src/main/java:ntcore-java",
                "//wpilibj/src/main/java:wpilibj-java",
                "//commandsv2/src/main/java:commandsv2-java",
                "//commandsv3/src/main/java:commandsv3-java",
                "//wpimath/src/main/java:wpimath-java",
                "//wpiutil/src/main/java:wpiutil-java",
                "//epilogue-runtime/src/main/java:epilogue-java",
                "//wpiunits/src/main/java:wpiunits-java",
            ],
            tags = ["wpi-example"],
        )

    for folder in snippet_test_folders:
        wpilib_java_junit5_test(
            name = folder + "-test",
            srcs = native.glob(["src/test/java/org/wpilib/snippets/" + folder + "/**/*.java"]),
            plugins = [
                "//epilogue-processor/src/main/java:plugin",
            ],
            deps = [
                ":" + folder + "-snippet",
                "//hal/src/main/java:hal-java",
                "//ntcore/src/main/java:ntcore-java",
                "//wpilibj/src/main/java:wpilibj-java",
                "//commandsv2/src/main/java:commandsv2-java",
                "//commandsv3/src/main/java:commandsv3-java",
                "//wpimath/src/main/java:wpimath-java",
                "//wpiutil/src/main/java:wpiutil-java",
                "//epilogue-runtime/src/main/java:epilogue-java",
                "//wpiunits/src/main/java:wpiunits-java",
            ],
            tags = ["wpi-example"],
        )
