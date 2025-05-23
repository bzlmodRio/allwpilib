load("//shared/bazel/rules:cc_rules.bzl", "wpilib_cc_binary", "wpilib_cc_library", "wpilib_cc_test")
load("//wpilibcExamples:example_projects.bzl", "COMMANDS_V2_FOLDERS", "EXAMPLE_FOLDERS", "TEMPLATES_FOLDERS", "TESTS_FOLDERS")

def build_examples(halsim_deps = []):
    for folder in EXAMPLE_FOLDERS:
        wpilib_cc_library(
            name = folder + "-examples-headers",
            hdrs = native.glob(["src/main/cpp/examples/" + folder + "/include/**/*.h"], allow_empty = True),
            strip_include_prefix = "src/main/cpp/examples/" + folder + "/include",
            tags = ["wpi-example"],
        )

        wpilib_cc_binary(
            name = folder + "-example",
            srcs = native.glob(["src/main/cpp/examples/" + folder + "/cpp/**/*.cpp", "src/main/cpp/examples/" + folder + "/c/**/*.c"], allow_empty = True),
            deps = [
                "//wpilibNewCommands:wpilibNewCommands.shared",
                "//apriltag:apriltag.shared",
                "//romiVendordep:romi-cpp.shared",
                "//xrpVendordep:xrp-cpp.shared",
                ":{}-examples-headers".format(folder),
            ],
            tags = ["wpi-example"],
        )

def build_commands():
    for folder in COMMANDS_V2_FOLDERS:
        wpilib_cc_library(
            name = folder + "-command",
            srcs = native.glob(["src/main/cpp/commands/" + folder + "/**/*.cpp"]),
            hdrs = native.glob(["src/main/cpp/commands/" + folder + "/**/*.h"]),
            deps = [
                "//wpilibNewCommands:wpilibNewCommands.shared",
            ],
            strip_include_prefix = "src/main/cpp/commands/" + folder,
            tags = ["wpi-example"],
        )

def build_templates():
    for folder in TEMPLATES_FOLDERS:
        wpilib_cc_library(
            name = folder + "-template",
            srcs = native.glob(["src/main/cpp/templates/" + folder + "/**/*.cpp"]),
            hdrs = native.glob(["src/main/cpp/templates/" + folder + "/**/*.h"]),
            deps = [
                "//wpilibNewCommands:wpilibNewCommands.shared",
            ],
            strip_include_prefix = "src/main/cpp/templates/" + folder + "/include",
            tags = ["wpi-example"],
        )

def build_tests():
    for folder in TESTS_FOLDERS:
        example_src_folder = "src/main/cpp/examples/" + folder
        example_test_folder = "src/test/cpp/examples/" + folder
        wpilib_cc_test(
            name = folder + "-test",
            size = "small",
            srcs = native.glob([example_test_folder + "/**/*.cpp", example_src_folder + "/cpp/**/*.cpp", example_src_folder + "/c/**/*.c"], allow_empty = True),
            deps = [
                "//wpilibNewCommands:wpilibNewCommands.static",
                ":{}-examples-headers".format(folder),
                "//thirdparty/googletest:googletest.static",
            ],
            defines = ["RUNNING_FRC_TESTS=1"],
            tags = ["wpi-example", "no-tsan", "no-asan", "no-ubsan", "exclusive"],
        )
