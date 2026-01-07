load("@allwpilib_pip_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_test", "py_binary")

PROJECTS = [
    "AddressableLED",
    "AprilTagsVision",
    "ArcadeDrive",
    "ArcadeDriveXboxController",
    "ArmSimulation",
    "CANPDP",
    "DifferentialDriveBot",
    "DigitalCommunication",
    "DriveDistanceOffboard",
    "DutyCycleEncoder",
    "DutyCycleInput",
    "ElevatorProfiledPID",
    "ElevatorSimulation",
    "ElevatorTrapezoidProfile",
    "Encoder",
    # "EventLoop",
    "FlywheelBangBangController",
    "GettingStarted",
    "Gyro",
    "GyroMecanum",
    "HatchbotInlined",
    "HatchbotTraditional",
    "HidRumble",
    "HttpCamera",
    "I2CCommunication",
    "IntermediateVision",
    "MecanumBot",
    "MecanumDrive",
    "Mechanism2d",
    "MotorControl",
    "PotentiometerPID",
    "QuickVision",
    "RomiReference",
    "SelectCommand",
    "SimpleDifferentialDriveSimulation",
    "Solenoid",
    "StateSpaceFlywheel",
    "StateSpaceFlywheelSysId",
    "SwerveBot",
    "SysId",
    "TankDrive",
    "TankDriveXboxController",
]


def define_examples():
    for example_folder in PROJECTS:
        base_name = example_folder.replace("/", "_")
        common_kwargs = dict(
            srcs = [":robotpy_entry_point.py",],
            main = "robotpy_entry_point.py",
            data = native.glob([example_folder + "/**"]),
            imports = [example_folder],
        )
        common_deps = [
            ":robotpy", 
            "//commandsv2:commandsv2-import",
            "//wpilibc:robotpy-wpilib", 
            "//romiVendordep:robotpy-romi",
            requirement("numpy"),
        ]

        py_test(
            name = base_name + "-test",
            args = ["--main", "$(location " + example_folder + "/robot.py)", "test", "--builtin"],
            deps = common_deps,
            size="small",
            **common_kwargs,
        )
        
        py_binary(
            name = base_name + "-run",
            args = ["--main", "$(location " + example_folder + "/robot.py)", "run"],
            deps = common_deps,
            **common_kwargs,
        )
        
        py_binary(
            name = base_name + "-sim",
            args = ["--main", "$(location " + example_folder + "/robot.py)", "sim"],
            deps = common_deps + ["//simulation/halsim_gui:robotpy-halsim-gui"],
            **common_kwargs,
        )
