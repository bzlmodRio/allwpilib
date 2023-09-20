load("//shared/bazel/rules:java_rules.bzl", "wpilib_java_binary", "wpilib_java_junit5_test", "wpilib_java_library")

EXAMPLES_FOLDERS = [
    "addressableled",
    "arcadedrive",
    "arcadedrivexboxcontroller",
    "armbot",
    "armbotoffboard",
    "armsimulation",
    "axiscamera",
    "canpdp",
    "differentialdrivebot",
    "differentialdriveposeestimator",
    "digitalcommunication",
    "dma",
    "drivedistanceoffboard",
    "dutycycleencoder",
    "dutycycleinput",
    "elevatorprofiledpid",
    "elevatorsimulation",
    "elevatortrapezoidprofile",
    "encoder",
    "eventloop",
    "frisbeebot",
    "gearsbot",
    "gettingstarted",
    "gyro",
    "gyrodrivecommands",
    "gyromecanum",
    "hatchbotinlined",
    "hatchbottraditional",
    "hidrumble",
    "i2ccommunication",
    "intermediatevision",
    "mecanumbot",
    "mecanumcontrollercommand",
    "mecanumdrive",
    "mecanumdriveposeestimator",
    "mechanism2d",
    "motorcontrol",
    "potentiometerpid",
    "quickvision",
    "ramsetecommand",
    "ramsetecontroller",
    "rapidreactcommandbot",
    "relay",
    "romireference",
    "selectcommand",
    "shuffleboard",
    "simpledifferentialdrivesimulation",
    "solenoid",
    "statespacearm",
    "statespacedifferentialdrivesimulation",
    "statespaceelevator",
    "statespaceflywheel",
    "statespaceflywheelsysid",
    "swervebot",
    "swervecontrollercommand",
    "swervedriveposeestimator",
    "tankdrive",
    "tankdrivexboxcontroller",
    "ultrasonic",
    "ultrasonicpid",
    "unittest",
]

COMMANDS_V2_FOLDERS = [
    "command2",
    "emptyclass",
    "instantcommand",
    "parallelcommandgroup",
    "paralleldeadlinegroup",
    "parallelracegroup",
    "pidcommand",
    "pidsubsystem2",
    "profiledpidcommand",
    "profiledpidsubsystem",
    "sequentialcommandgroup",
    "subsystem2",
    "trapezoidprofilecommand",
    "trapezoidprofilesubsystem",
]

TEMPLATES_FOLDERS = [
    "commandbased",
    "commandbasedskeleton",
    "educational",
    "robotbaseskeleton",
    "romicommandbased",
    "romieducational",
    "romitimed",
    "timed",
    "timedskeleton",
    "timeslice",
    "timesliceskeleton",
]

TEST_FOLDERS = [
    "addressableled",
    "unittest",
]

def build_examples(halsim_deps):
    for folder in EXAMPLES_FOLDERS:
        wpilib_java_binary(
            name = folder + "-example",
            srcs = native.glob(["src/main/java/edu/wpi/first/wpilibj/examples/" + folder + "/**/*.java"]),
            main_class = "edu/wpi/first/wpilibj/examples/" + folder + "/Main",
            deps = [
                "//apriltag/src/main/java/edu/wpi/first/apriltag",
                "//cameraserver/src/main/java/edu/wpi/first:cameraserver",
                "//cscore/src/main/java/edu/wpi/first/cscore",
                "//hal/src/main/java/edu/wpi/first/hal",
                "//ntcore/src/main/java/edu/wpi/first/networktables",
                "//wpimath/src/main/java/edu/wpi/first/math:wpimath",
                "//wpilibj/src/main/java/edu/wpi/first/wpilibj",
                "//wpilibNewCommands/src/main/java/edu/wpi/first/wpilibj2/command:wpilibNewCommands",
                "//wpiutil/src/main/java/edu/wpi/first/util:wpiutil",
                "//romiVendordep/src/main/java/edu/wpi/first/wpilibj/romi",
                "@bzlmodrio-opencv//libraries/java/opencv",
            ],
            tags = ["wpi-example"],
        )

def build_commands():
    for folder in COMMANDS_V2_FOLDERS:
        wpilib_java_library(
            name = folder + "-command",
            srcs = native.glob(["src/main/java/edu/wpi/first/wpilibj/commands/" + folder + "/**/*.java"]),
            deps = [
                "//hal/src/main/java/edu/wpi/first/hal",
                "//wpilibj/src/main/java/edu/wpi/first/wpilibj",
                "//wpilibNewCommands/src/main/java/edu/wpi/first/wpilibj2/command:wpilibNewCommands",
                "//wpimath/src/main/java/edu/wpi/first/math:wpimath",
            ],
            tags = ["wpi-example"],
        )

def build_templates():
    for folder in TEMPLATES_FOLDERS:
        wpilib_java_library(
            name = folder + "-template",
            srcs = native.glob(["src/main/java/edu/wpi/first/wpilibj/templates/" + folder + "/**/*.java"]),
            deps = [
                "//hal/src/main/java/edu/wpi/first/hal",
                "//wpilibj/src/main/java/edu/wpi/first/wpilibj",
                "//wpilibNewCommands/src/main/java/edu/wpi/first/wpilibj2/command:wpilibNewCommands",
                "//wpimath/src/main/java/edu/wpi/first/math:wpimath",
                "//wpiutil/src/main/java/edu/wpi/first/util:wpiutil",
            ],
            tags = ["wpi-example"],
        )

def build_tests():
    for folder in TEST_FOLDERS:
        wpilib_java_junit5_test(
            name = folder + "-test",
            srcs = native.glob(["src/test/java/edu/wpi/first/wpilibj/examples/" + folder + "/**/*.java"]),
            deps = [
                ":" + folder + "-example",
                "//hal/src/main/java/edu/wpi/first/hal",
                "//ntcore/src/main/java/edu/wpi/first/networktables",
                "//wpilibj/src/main/java/edu/wpi/first/wpilibj",
                "//wpilibNewCommands/src/main/java/edu/wpi/first/wpilibj2/command:wpilibNewCommands",
                "//wpimath/src/main/java/edu/wpi/first/math:wpimath",
                "//wpiutil/src/main/java/edu/wpi/first/util:wpiutil",
            ],
            tags = ["wpi-example"],
        )
