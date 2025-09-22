import dataclasses
import json
import os
import pathlib
import re
import shutil
import subprocess
from typing import Dict


class RawConfig:

    PROJECT_RENAMES = [
        ("wpilibNewCommands/", "command/"),
        ("fieldImages/", "fields/"),
        ("datalogtool/", "tools/datalogtool/"),
        ("outlineviewer/", "tools/outlineviewer/"),
        ("processstarter/", "tools/processstarter/"),
        ("sysid/", "tools/sysid/"),
        ("wpical/", "tools/wpical/"),
        # TODO glass, wpilib[j/c]
    ]

    CC_FOLDER_RENAMES = [
        ("wpiutil/src/main/native/include", "wpi", "wpi/util"),
        ("wpiutil/src/main/native/thirdparty/argparse/include", "wpi", "wpi/util"),
        # Leave debugging alone
        ("wpiutil/src/main/native/thirdparty/expected/include", "wpi", "wpi/util"),
        # Leave fmt alone
        ("wpiutil/src/main/native/thirdparty/json/include", "wpi", "wpi/util"),
        ("wpiutil/src/main/native/thirdparty/llvm/include", "wpi", "wpi/util"),
        ("wpiutil/src/main/native/thirdparty/mpack/include", "wpi", "wpi/util"),
        # Leave nanopb alone
        ("wpiutil/src/main/native/thirdparty/sigslot/include", "wpi", "wpi/util"),
        # Leave upb alone
        ("wpinet/src/main/native/include", "wpinet", "wpi/net"),
        ("wpinet/src/main/native/thirdparty/tcpsockets/include", "wpinet", "wpi/net"),
        # No datalog
        ("ntcore/src/main/native/include", "networktables", "wpi/ntcore"),
        ("ntcore/src/generated/main/native/include", "networktables", "wpi/ntcore"),
        ("hal/src/main/native/include", "hal", "wpi/hal"),
        ("wpimath/src/main/native/include", "frc", "wpi/math"),
        ("wpimath/src/main/native/include", "units", "wpi/units"),
        ("wpilibc/src/main/native/include", "frc", "wpi"),
        ("wpilibc/src/generated/main/native/include", "frc", "wpi"),
        ("apriltag/src/main/native/include", "frc", "wpi"),
        ("command/src/main/native/include", "frc2", "wpi"),
        ("command/src/generated/main/native/include", "frc2", "wpi"),
        ("fields/src/main/native/include", "fields", "wpi/fields"),
        ("cameraserver/src/main/native/include", "cameraserver", "wpi/cameraserver"),
        ("cameraserver/src/main/native/include", "vision", "wpi/vision"),
        ("glass/src/lib/native/include", "glass", "wpi/glass"),
        ("glass/src/libnt/native/include", "glass", "wpi/glass"),
        # wpigui root handled with CC_FILE_RENAMES
        # cscore root handled with CC_FILE_RENAMES
        ("romiVendordep/src/main/native/include", "frc/romi", "wpi/romi"),
        ("xrpVendordep/src/main/native/include", "frc/xrp", "wpi/xrp"),
    ]

    CC_FILE_RENAMES = [
        (
            pathlib.Path("ntcore/src/main/native/include"),
            [
                ("ntcore_test.h", "wpi/ntcore/ntcore_test.hpp"),
                ("ntcore.h", "wpi/ntcore/ntcore.hpp"),
                ("ntcore_c.h", "wpi/ntcore/ntcore_c.h"),
                ("ntcore_cpp.h", "wpi/ntcore/ntcore_cpp.hpp"),
                ("ntcore_c.h", "wpi/ntcore/ntcore_c.h"),
            ],
        ),
        (
            pathlib.Path("ntcore/src/generated/main/native/include"),
            [
                ("ntcore_c_types.h", "wpi/ntcore/ntcore_c_types.h"),
                ("ntcore_cpp_types.h", "wpi/ntcore/ntcore_cpp_types.hpp"),
            ],
        ),
        (
            pathlib.Path("wpimath/src/main/native/include"),
            [
                ("wpimath/MathShared.h", "wpi/math/util/MathShared.hpp"),
                ("frc/DARE.h", "wpi/math/linalg/DARE.hpp"),
                ("frc/ct_matrix.h", "wpi/math/linalg/ct_matrix.hpp"),
                ("frc/EigenCore.h", "wpi/math/linalg/EigenCore.hpp"),
                ("frc/ComputerVisionUtil.h", "wpi/math/util/ComputerVisionUtil.hpp"),
                ("frc/MathUtil.h", "wpi/math/util/MathUtil.hpp"),
                ("frc/StateSpaceUtil.h", "wpi/math/util/StateSpaceUtil.hpp"),
            ],
        ),
        (
            pathlib.Path("cscore/src/main/native/include"),
            [
                ("cscore_cv.h", "wpi/cscore/cscore_cv.hpp"),
                ("cscore_cpp.h", "wpi/cscore/cscore_cpp.hpp"),
                ("cscore.h", "wpi/cscore/cscore.hpp"),
                ("cscore_raw.h", "wpi/cscore/cscore_raw.hpp"),
                ("cscore_c.h", "wpi/cscore/cscore_c.hpp"),
                ("cscore_oo.h", "wpi/cscore/cscore_oo.hpp"),
                ("cscore_runloop.h", "wpi/cscore/cscore_runloop.hpp"),
            ],
        ),
        (
            pathlib.Path("wpigui/src/main/native/include"),
            [
                ("wpigui_openurl.h", "wpi/gui/wpigui_openurl.hpp"),
                ("portable-file-dialogs.h", "wpi/gui/portable-file-dialogs.hpp"),
                ("wpigui_internal.h", "wpi/gui/wpigui_internal.hpp"),
                ("wpigui.h", "wpi/gui/wpigui.hpp"),
            ],
        ),
        (
            pathlib.Path("wpilibc/src/main/native/include"),
            [
                ("WPILibVersion.h", "wpi/system/WPILibVersion.hpp"),
                ("frc/DriverStation.h", "wpi/driverstation/DriverStation.hpp"),
                ("frc/GenericHID.h", "wpi/driverstation/GenericHID.hpp"),
                ("frc/Joystick.h", "wpi/driverstation/Joystick.hpp"),
                ("frc/ADXL345_I2C.h", "wpi/hardware/accelerometer/ADXL345_I2C.hpp"),
                (
                    "frc/AnalogAccelerometer.h",
                    "wpi/hardware/accelerometer/AnalogAccelerometer.hpp",
                ),
                ("frc/CAN.h", "wpi/hardware/bus/CAN.hpp"),
                ("frc/I2C.h", "wpi/hardware/bus/I2C.hpp"),
                ("frc/SerialPort.h", "wpi/hardware/bus/SerialPort.hpp"),
                ("frc/AnalogInput.h", "wpi/hardware/discrete/AnalogInput.hpp"),
                ("frc/CounterBase.h", "wpi/hardware/discrete/CounterBase.hpp"),
                ("frc/DigitalInput.h", "wpi/hardware/discrete/DigitalInput.hpp"),
                ("frc/DigitalOutput.h", "wpi/hardware/discrete/DigitalOutput.hpp"),
                ("frc/PWM.h", "wpi/hardware/discrete/PWM.hpp"),
                ("frc/AddressableLED.h", "wpi/hardware/led/AddressableLED.hpp"),
                ("frc/LEDPattern.h", "wpi/hardware/led/LEDPattern.hpp"),
                (
                    "frc/motorcontrol/MotorController.h",
                    "wpi/hardware/motor/MotorController.hpp",
                ),
                (
                    "frc/motorcontrol/MotorControllerGroup.h",
                    "wpi/hardware/motor/MotorControllerGroup.hpp",
                ),
                ("frc/MotorSafety.h", "wpi/hardware/motor/MotorSafety.hpp"),
                (
                    "frc/motorcontrol/PWMMotorController.h",
                    "wpi/hardware/motor/PWMMotorController.hpp",
                ),
                ("frc/Compressor.h", "wpi/hardware/pneumatic/Compressor.hpp"),
                (
                    "frc/CompressorConfigType.h",
                    "wpi/hardware/pneumatic/CompressorConfigType.hpp",
                ),
                ("frc/DoubleSolenoid.h", "wpi/hardware/pneumatic/DoubleSolenoid.hpp"),
                ("frc/PneumaticHub.h", "wpi/hardware/pneumatic/PneumaticHub.hpp"),
                ("frc/PneumaticsBase.h", "wpi/hardware/pneumatic/PneumaticsBase.hpp"),
                (
                    "frc/PneumaticsControlModule.h",
                    "wpi/hardware/pneumatic/PneumaticsControlModule.hpp",
                ),
                (
                    "frc/PneumaticsModuleType.h",
                    "wpi/hardware/pneumatic/PneumaticsModuleType.hpp",
                ),
                ("frc/Solenoid.h", "wpi/hardware/pneumatic/Solenoid.hpp"),
                (
                    "frc/PowerDistribution.h",
                    "wpi/hardware/power/PowerDistribution.hpp",
                ),
                ("frc/AnalogEncoder.h", "wpi/hardware/rotation/AnalogEncoder.hpp"),
                (
                    "frc/AnalogPotentiometer.h",
                    "wpi/hardware/rotation/AnalogPotentiometer.hpp",
                ),
                ("frc/DutyCycle.h", "wpi/hardware/rotation/DutyCycle.hpp"),
                (
                    "frc/DutyCycleEncoder.h",
                    "wpi/hardware/rotation/DutyCycleEncoder.hpp",
                ),
                ("frc/Encoder.h", "wpi/hardware/rotation/Encoder.hpp"),
                ("frc/Servo.h", "wpi/hardware/servo/Servo.hpp"),
                ("frc/IterativeRobotBase.h", "wpi/opmode/IterativeRobotBase.hpp"),
                ("frc/RobotBase.h", "wpi/opmode/RobotBase.hpp"),
                ("frc/RobotState.h", "wpi/opmode/RobotState.hpp"),
                ("frc/TimedRobot.h", "wpi/opmode/TimedRobot.hpp"),
                ("frc/TimesliceRobot.h", "wpi/opmode/TimesliceRobot.hpp"),
                ("frc/DataLogManager.h", "wpi/system/DataLogManager.hpp"),
                ("frc/Filesystem.h", "wpi/system/Filesystem.hpp"),
                ("frc/Resource.h", "wpi/system/Resource.hpp"),
                ("frc/RobotController.h", "wpi/system/RobotController.hpp"),
                ("frc/ScopedTracer.h", "wpi/system/ScopedTracer.hpp"),
                ("frc/Threads.h", "wpi/system/Threads.hpp"),
                ("frc/Timer.h", "wpi/system/Timer.hpp"),
                ("frc/Tracer.h", "wpi/system/Tracer.hpp"),
                ("frc/WPILibVersion.h", "wpi/system/WPILibVersion.hpp"),
                ("frc/Watchdog.h", "wpi/system/Watchdog.hpp"),
            ],
        ),
        (
            pathlib.Path("wpilibc/src/generated/main/native/include"),
            [
                ("frc/StadiaController.h", "wpi/driverstation/StadiaController.hpp"),
                ("frc/PS4Controller.h", "wpi/driverstation/PS4Controller.hpp"),
                ("frc/PS5Controller.h", "wpi/driverstation/PS5Controller.hpp"),
                ("frc/XboxController.h", "wpi/driverstation/XboxController.hpp"),
                (
                    "frc/motorcontrol/PWMSparkFlex.h",
                    "wpi/hardware/motor/PWMSparkFlex.hpp",
                ),
                ("frc/motorcontrol/SparkMini.h", "wpi/hardware/motor/SparkMini.hpp"),
                (
                    "frc/motorcontrol/PWMVictorSPX.h",
                    "wpi/hardware/motor/PWMVictorSPX.hpp",
                ),
                ("frc/motorcontrol/Jaguar.h", "wpi/hardware/motor/Jaguar.hpp"),
                ("frc/motorcontrol/Victor.h", "wpi/hardware/motor/Victor.hpp"),
                ("frc/motorcontrol/DMC60.h", "wpi/hardware/motor/DMC60.hpp"),
                ("frc/motorcontrol/VictorSP.h", "wpi/hardware/motor/VictorSP.hpp"),
                ("frc/motorcontrol/PWMVenom.h", "wpi/hardware/motor/PWMVenom.hpp"),
                ("frc/motorcontrol/Koors40.h", "wpi/hardware/motor/Koors40.hpp"),
                ("frc/motorcontrol/SD540.h", "wpi/hardware/motor/SD540.hpp"),
                ("frc/motorcontrol/Talon.h", "wpi/hardware/motor/Talon.hpp"),
                ("frc/motorcontrol/Spark.h", "wpi/hardware/motor/Spark.hpp"),
                (
                    "frc/motorcontrol/PWMTalonSRX.h",
                    "wpi/hardware/motor/PWMTalonSRX.hpp",
                ),
                ("frc/motorcontrol/PWMTalonFX.h", "wpi/hardware/motor/PWMTalonFX.hpp"),
                (
                    "frc/motorcontrol/PWMSparkMax.h",
                    "wpi/hardware/motor/PWMSparkMax.hpp",
                ),
            ],
        ),
    ]

    JAVA_PROJECT_REPLACMENTS = [
        ("wpiutil", "edu.wpi.first.util", "org.wpilib.util"),
        ("wpimath", "edu.wpi.first.math", "org.wpilib.math"),
        ("wpinet", "edu.wpi.first.net", "org.wpilib.net"),
        ("datalog", "edu.wpi.first.datalog", "org.wpilib.datalog"),
        ("command", "edu.wpi.first.wpilibj2.command", "org.wpilib.command"),
        ("ntcore", "edu.wpi.first.networktables", "org.wpilib.networktables"),
        ("fields", "edu.wpi.first.fields", "org.wpilib.fields"),
        ("hal", "edu.wpi.first.hal", "org.wpilib.hardware.hal"),
        ("wpiunits", "edu.wpi.first.units", "org.wpilib.units"),
        ("apriltag", "edu.wpi.first.apriltag", "org.wpilib.vision.apriltag"),
        (
            "epilogue-processor",
            "edu.wpi.first.epilogue.processor",
            "org.wpilib.epilogue.processor",
        ),
        ("epilogue-runtime", "edu.wpi.first.epilogue", "org.wpilib.epilogue"),
        (
            "epilogue-runtime",
            "edu.wpi.first.epilogue.logging",
            "org.wpilib.epilogue.logging",
        ),
        ("cscore", "edu.wpi.first.cscore", "org.wpilib.vision.camera"),
        ("cameraserver", "edu.wpi.first.vision", "org.wpilib.vision.process"),
        ("cameraserver", "edu.wpi.first.cameraserver", "org.wpilib.vision.stream"),
        ("xrpVendordep", "edu.wpi.first.wpilibj.xrp", "org.wpilib.xrp"),
        ("romiVendordep", "edu.wpi.first.wpilibj.romi", "org.wpilib.romi"),
        ("wpilibjExamples", "edu.wpi.first.wpilibj.commands", "org.wpilib.commands"),
        ("wpilibjExamples", "edu.wpi.first.wpilibj.examples", "org.wpilib.examples"),
        ("wpilibjExamples", "edu.wpi.first.wpilibj.snippets", "org.wpilib.snippets"),
        ("wpilibjExamples", "edu.wpi.first.wpilibj.templates", "org.wpilib.templates"),
        ("wpilibj", "edu.wpi.first.wpilibj", "org.wpilib"),
    ]
    """
    TODO
"wpimath/src/test/java/edu/wpi/first/wpilibj/StructTestBase.java": "wpimath/src/test/java/edu/wpi/first/wpilibj/StructTestBase.java",
"wpimath/src/test/java/edu/wpi/first/wpilibj/ProtoTestBase.java": "wpimath/src/test/java/edu/wpi/first/wpilibj/ProtoTestBase.java",
"wpimath/src/test/java/edu/wpi/first/wpilibj/UtilityClassTest.java": "wpimath/src/test/java/edu/wpi/first/wpilibj/UtilityClassTest.java",
"command/src/test/java/edu/wpi/first/wpilibj2/MockHardwareExtension.java": "command/src/test/java/edu/wpi/first/wpilibj2/MockHardwareExtension.java",
"ntcore/src/dev/java/edu/wpi/first/ntcore/DevMain.java": "ntcore/src/dev/java/edu/wpi/first/ntcore/DevMain.java",
"wpilibj/src/test/java/edu/wpi/first/math/util/ColorTest.java": "wpilibj/src/test/java/edu/wpi/first/math/util/ColorTest.java",

        """

    JAVA_FILE_RENAMES = [
        (
            pathlib.Path("wpiutil"),
            [
                ("edu/wpi/first/util", "org/wpilib/util/runtime", "ClassPreloader"),
                (
                    "edu/wpi/first/util",
                    "org/wpilib/util/runtime",
                    "CombinedRuntimeLoader",
                ),
                (
                    "edu/wpi/first/util",
                    "org/wpilib/util/runtime",
                    "MsvcRuntimeException",
                ),
                ("edu/wpi/first/util", "org/wpilib/util/runtime", "RuntimeDetector"),
                ("edu/wpi/first/util", "org/wpilib/util/runtime", "RuntimeLoader"),
                (
                    "edu/wpi/first/util",
                    "org/wpilib/util/container",
                    "DoubleCircularBuffer",
                ),
                ("edu/wpi/first/util", "org/wpilib/util/container", "CircularBuffer"),
                ("edu/wpi/first/util", "org/wpilib/util/cleanup", "WPICleaner"),
                ("edu/wpi/first/util", "org/wpilib/util/concurrent", "EventVector"),
            ],
        ),
        (
            pathlib.Path("command"),
            [
                ("edu/wpi/first/wpilibj2", "org/wpilib", "MockHardwareExtension"),
            ],
        ),
        (
            pathlib.Path("wpimath"),
            [
                ("edu/wpi/first/math", "org/wpilib/math/linalg", "DARE"),
                ("edu/wpi/first/math", "org/wpilib/math/linalg", "VecBuilder"),
                ("edu/wpi/first/math", "org/wpilib/math/linalg", "Vector"),
                ("edu/wpi/first/math", "org/wpilib/math/linalg", "Matrix"),
                ("edu/wpi/first/math", "org/wpilib/math/linalg", "MatBuilder"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "MathUtil"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "StateSpaceUtil"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "ComputerVisionUtil"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "MathShared"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "MathSharedStore"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "Pair"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "Num"),
                ("edu/wpi/first/math", "org/wpilib/math/util", "Nat"),
                (
                    "edu/wpi/first/math",
                    "org/wpilib/math/interpolation",
                    "InterpolatingMatrixTreeMap",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib", "ProtoTestBase"),
                ("edu/wpi/first/wpilibj", "org/wpilib", "StructTestBase"),
                ("edu/wpi/first/wpilibj", "org/wpilib", "UtilityClassTest"),
            ],
        ),
        (
            pathlib.Path("wpilibj"),
            [
                ("edu/wpi/first/wpilibj", "org/wpilib/driverstation", "DriverStation"),
                ("edu/wpi/first/wpilibj", "org/wpilib/driverstation", "GenericHID"),
                ("edu/wpi/first/wpilibj", "org/wpilib/driverstation", "Joystick"),
                ("edu/wpi/first/wpilibj", "org/wpilib/driverstation", "PS4Controller"),
                ("edu/wpi/first/wpilibj", "org/wpilib/driverstation", "PS5Controller"),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/driverstation",
                    "StadiaController",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/driverstation", "XboxController"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/bus", "CAN"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/bus", "I2C"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/bus", "SerialPort"),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/accelerometer",
                    "ADXL345_I2C",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/accelerometer",
                    "AnalogAccelerometer",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/discrete",
                    "AnalogInput",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/discrete",
                    "CounterBase",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/discrete",
                    "DigitalInput",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/discrete",
                    "DigitalOutput",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/discrete", "PWM"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/led", "AddressableLED"),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/led",
                    "AddressableLEDBuffer",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/led",
                    "AddressableLEDBufferView",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/led", "LEDPattern"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/led", "LEDReader"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/led", "LEDWriter"),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "MotorController",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "MotorControllerGroup",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/motor", "MotorSafety"),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMMotorController",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/motor", "MotorSafety"),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "DMC60",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "Jaguar",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "Koors40",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMSparkFlex",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMSparkMax",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMTalonFX",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMTalonSRX",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMVenom",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "PWMVictorSPX",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "SD540",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "Spark",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "SparkMini",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "Talon",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "Victor",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "VictorSP",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "MockPWMMotorController",
                ),
                (
                    "edu/wpi/first/wpilibj/motorcontrol",
                    "org/wpilib/hardware/motor",
                    "MockMotorController",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "Compressor",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "CompressorConfigType",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "DoubleSolenoid",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "PneumaticHub",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "PneumaticsBase",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "PneumaticsControlModule",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "PneumaticsModuleType",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/pneumatic", "Solenoid"),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "DoubleSolenoidTestCTRE",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "DoubleSolenoidTestREV",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "SolenoidTestCTRE",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/pneumatic",
                    "SolenoidTestREV",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/power",
                    "PowerDistribution",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/rotation",
                    "AnalogEncoder",
                ),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/rotation",
                    "AnalogPotentiometer",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/rotation", "DutyCycle"),
                (
                    "edu/wpi/first/wpilibj",
                    "org/wpilib/hardware/rotation",
                    "DutyCycleEncoder",
                ),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/rotation", "Encoder"),
                ("edu/wpi/first/wpilibj", "org/wpilib/hardware/servo", "Servo"),
                ("edu/wpi/first/wpilibj", "org/wpilib/opmode", "IterativeRobotBase"),
                ("edu/wpi/first/wpilibj", "org/wpilib/opmode", "RobotBase"),
                ("edu/wpi/first/wpilibj", "org/wpilib/opmode", "RobotState"),
                ("edu/wpi/first/wpilibj", "org/wpilib/opmode", "TimedRobot"),
                ("edu/wpi/first/wpilibj", "org/wpilib/opmode", "TimesliceRobot"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "DataLogManager"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "Filesystem"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "Resource"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "RobotController"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "Threads"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "Timer"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "Tracer"),
                ("edu/wpi/first/wpilibj", "org/wpilib/system", "Watchdog"),
            ],
        ),
    ]

    GENERIC_RENAMES = [
        (
            "apriltag/src/main/native/resources/edu/wpi/first",
            "apriltag/src/main/native/resources/org/wpilib/vision",
        ),
        (
            "apriltag/src/test/resources/edu/wpi/first",
            "apriltag/src/test/resources/org/wpilib/vision",
        ),
        (
            "command/src/generate/main/native/cpp/frc2/",
            "command/src/generate/main/native/cpp/wpi/",
        ),
        (
            "command/src/generate/main/native/include/frc2/",
            "command/src/generate/main/native/include/wpi/",
        ),
        (
            "command/wpilibnewcommands-config.cmake.in",
            "command/command-config.cmake.in",
        ),
        (
            "command/src/generate/main/native/include/wpi/command/button/commandhid.h.jinja",
            "command/src/generate/main/native/include/wpi/command/button/commandhid.hpp.jinja",
        ),
        (
            "command/src/generated/main/native/cpp/frc2/",
            "command/src/generated/main/native/cpp/wpi/",
        ),
        ("command/src/test/native/cpp/frc2/", "command/src/test/native/cpp/wpi/"),
        ("fields/fieldimages-config.cmake.in", "fields/fields-config.cmake.in"),
        (
            "fields/src/main/native/resources/edu/wpi/first",
            "fields/src/main/native/resources/org/wpilib",
        ),
        (
            "fields/src/test/native/resources/edu/wpi/first",
            "fields/src/test/native/resources/org/wpilib",
        ),
        (
            "ntcore/src/generate/main/native/include/networktables/Topic.h.jinja",
            "ntcore/src/generate/main/native/include/wpi/ntcore/Topic.hpp.jinja",
        ),
        (
            "wpilibc/src/generate/main/native/include/frc/",
            "wpilibc/src/generate/main/native/include/wpi/",
        ),
        (
            "wpilibc/src/generate/main/native/include/wpi/hid.h.jinja",
            "wpilibc/src/generate/main/native/include/wpi/driverstation/hid.hpp.jinja",
        ),
        (
            "wpilibc/src/generate/main/native/include/wpi/motorcontroller/pwm_motor_controller.h.jinja",
            "wpilibc/src/generate/main/native/include/wpi/hardware/motor/pwm_motor_controller.hpp.jinja",
        ),
        (
            "wpilibc/src/generate/main/native/include/wpi/simulation/hidsim.h.jinja",
            "wpilibc/src/generate/main/native/include/wpi/simulation/hidsim.hpp.jinja",
        ),
    ]

    STR_REPLACEMENTS = [
        (
            "frc2/command/button/Command{{ ConsoleName }}Controller.h",
            "wpi/command/button/Command{{ ConsoleName }}Controller.h",
        ),
        ("frc/motorcontrol/{{ name }}.h", "wpi/motorcontrol/{{ name }}.hpp"),
        ("frc/{{ ConsoleName }}Controller.h", "wpi/{{ ConsoleName }}Controller.hpp"),
        (
            "frc/simulation/{{ ConsoleName }}ControllerSim.h",
            "wpi/simulation/{{ ConsoleName }}ControllerSim.hpp",
        ),
    ]


@dataclasses.dataclass
class PreprocessedConfig:
    cc_file_renames: int
    cc_incude_replacements: int
    java_pkg_renames: int
    java_file_renames: Dict[str, str]
    java_class_package_overrides: Dict[str, str]

    def write_json(self, f):
        return json.dump(
            dict(
                cc_file_renames=self.cc_file_renames,
                cc_incude_replacements=self.cc_incude_replacements,
                java_file_renames=self.java_file_renames,
                java_pkg_renames=self.java_pkg_renames,
                java_class_package_overrides=self.java_class_package_overrides,
            ),
            f,
            indent=4,
        )


def crawl_and_replace(dir_to_crawl, file_filter, replacement_callback):

    excluded_dirs = [".venv", ".git", "build", ".gradle"]

    for root, dirs, files in os.walk(dir_to_crawl):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and "bazel-" not in d]

        for f in files:

            full_file = os.path.join(root, f)
            if full_file == "./refactor_layout.py":
                continue
            if not file_filter(full_file):
                continue

            with open(full_file) as fs:
                contents = fs.read()

            contents = replacement_callback(contents)

            with open(full_file, "w") as of:
                of.write(contents)


def hal_namespace_replacements():
    return [
        (" hal::", r" wpi::hal::"),
    ]


def namespace_type_helper(original_namespace, new_namespace, class_types):
    output = []
    for class_type in class_types:
        output.extend(
            [
                ("([ !<\({])" + class_type, r"\1" + new_namespace + "::" + class_type),
                (
                    "([ !<\({])" + original_namespace + "::" + class_type,
                    r"\1" + new_namespace + "::" + class_type,
                ),
                ("^" + class_type, new_namespace + "::" + class_type),
                (
                    "^" + original_namespace + "::" + class_type,
                    new_namespace + "::" + class_type,
                ),
            ]
        )
    return output


def wpinet_namespace_replacements():

    return namespace_type_helper(
        "wpi",
        "wpi::net",
        [
            "raw_uv_ostream",
            "GetHostname",
            "HttpConnection",
            "EventLoopRunner",
            "EventLoopRunner",
            "NetworkAcceptor",
            "WebSocket",
            "UrlParser",
            "MimeTypeFromPath",
            "http_method_str",
        ],
    ) + [
        ("wpi::uv", "wpi::net::uv"),
        ("wpi::HTTP_GET", "wpi::net::HTTP_GET"),
        ("wpi::HTTP_CONNECT", "wpi::net::HTTP_CONNECT"),
    ]


def wpiutil_namespace_replacements():

    return namespace_type_helper(
        "wpi",
        "wpi::util",
        [
            "SmallString",
            "SmallVector",
            "SmallVectorImpl",
            "StringMap",
            "SmallSet",
            "DenseMap",
            "SmallDenseMap",
            "SHA1",
            "Logger",
            "EventVector",
            "MemoryBuffer",
            "FastQueue",
            "raw_ostream",
            "raw_istream",
            "raw_string_ostream",
            "raw_svector_ostream",
            "raw_uvector_ostream",
            "raw_fd_ostream",
            "raw_fd_istream",
            "unique_function",
            "safe_malloc",
            "promise",
            # "future",
            "function_ref",
            "SafeThreadOwner",
            "SafeThread",
            "sig::Signal",
            "sig::ScopedConnection",
            # "substr",
            # "slice",
            "parse_integer",
            "equals_lower",
            "starts_with",
            "ends_with",
            "circular_buffer",
            "rsplit",
            "ends_with",
            "drop_back",
            "drop_front",
            "remove_prefix",
            "remove_suffix",
            "to_string_view",
            "make_string",
            "format_to_n_c_str",
            # "contains",
            "hexDigitValue",
            # "print",
            "WPI_LOG_INFO",
            "WPI_LOG_CRITICAL",
            "WPI_LOG_ERROR",
            "WPI_LOG_WARNING",
            "WPI_LOG_DEBUG",
            "WPI_LOG_DEBUG1",
            "WPI_LOG_DEBUG2",
            "WPI_LOG_DEBUG3",
            "WPI_LOG_DEBUG4",
            "RawFrame",
            "WaitForObject",
            "SendableRegistry",
            "SetFrameData",
            "kHandleTypeCSBase",
            "kHandleTypeHALBase",
            "CallbackListenerData",
            "DynamicStruct",
            "Protobuf",
            "ProtoInputStream",
            "ProtoOutputStream",
            "ForEachStructSchema",
            "PackCallback",
            "StdVectorUnpackCallback",
            "StructSerializable",
            "GetStructTypeString",
            "UnescapeCString",
            "NullDeleter",
            "GetStackTrace",
            "UnpackCallback",
            "UidVector",
        ],
    ) + [
        ("::wpi::WPI_LOG_ERROR", "::wpi::util::WPI_LOG_ERROR"),
        ("::wpi::WPI_LOG_WARNING", "::wpi::util::WPI_LOG_WARNING"),
        ("::wpi::WPI_LOG_INFO", "::wpi::util::WPI_LOG_INFO"),
        ("::wpi::WPI_LOG_DEBUG", "::wpi::util::WPI_LOG_DEBUG"),
        ("::wpi::WPI_LOG_DEBUG1", "::wpi::util::WPI_LOG_DEBUG1"),
        ("::wpi::WPI_LOG_DEBUG2", "::wpi::util::WPI_LOG_DEBUG2"),
        ("::wpi::WPI_LOG_DEBUG3", "::wpi::util::WPI_LOG_DEBUG3"),
        ("::wpi::WPI_LOG_DEBUG4", "::wpi::util::WPI_LOG_DEBUG4"),
        ("wpi::Event(\W)", r"wpi::util::Event\1"),
        ("wpi::SendableBuilder(\W)", r"wpi::util::SendableBuilder\1"),
        ("wpi::SendableHelper(\W)", r"wpi::util::SendableHelper\1"),
        ("wpi::Sendable(\W)", r"wpi::util::Sendable\1"),
        ("wpi::Lerp", "wpi::util::Lerp"),
        ("wpi::Struct", "wpi::util::Struct"),
        ("wpi::array", "wpi::util::array"),
        ("wpi::empty_array", "wpi::util::empty_array"),
        ("wpi::UnpackStruct", "wpi::util::UnpackStruct"),
        ("wpi::PackStruct", "wpi::util::PackStruct"),
        ("wpi::StructSerializable", "wpi::util::StructSerializable"),
        ("wpi::is_constexpr", "wpi::util::is_constexpr"),
        ("wpi::contains", "wpi::util::contains"),
        ("wpi::print", "wpi::util::print"),
        ("wpi::substr", "wpi::util::substr"),
        ("wpi::rtrim", "wpi::util::rtrim"),
        ("wpi::trim", "wpi::util::trim"),
        ("wpi::split", "wpi::util::split"),
        ("wpi::mutex", "wpi::util::mutex"),
        ("wpi::sgn", "wpi::util::sgn"),
        ("wpi::condition_variable", "wpi::util::condition_variable"),
        ("wpi::recursive_mutex", "wpi::util::recursive_mutex"),
        ("wpi::recursive_spinlock", "wpi::util::recursive_spinlock"),
        ("wpi::Now", "wpi::util::Now"),
        ("wpi::SetNowImpl", "wpi::util::SetNowImpl"),
        ("wpi::spinlock", "wpi::util::spinlock"),
        ("wpi::future", "wpi::util::future"),
        ("wpi::support", "wpi::util::support"),
        ("namespace wpi::java", "namespace wpi::util::java"),
        ("wpi::java", "wpi::util::java"),
    ]


def wpimath_namespace_replacements():

    return namespace_type_helper(
        "frc",
        "wpi::math",
        [
            "Pose2d",
            "Pose3d",
            "Rotation2d",
            "Rotation3d",
            "Translation2d",
            "Translation3d",
            "Transform2d",
            "Transform3d",
            "Quaternion",
            "Matrixd",
            "Vectord",
            "LinearSystemId",
            "Trajectory",
            "TrapezoidProfile",
            "DifferentialDriveWheelSpeeds",
            "DifferentialDrivePoseEstimator",
            "DifferentialDriveOdometry",
            "MecanumDriveWheelSpeeds",
            "MecanumDriveWheelPositions",
            "MecanumDriveOdometry",
            "MecanumDriveKinematics",
            "MecanumDrivePoseEstimator",
            "SwerveDriveKinematics",
            "SwerveDriveOdometry",
            "SwerveDrivePoseEstimator",
            "SwerveModuleState",
            "SwerveModulePosition",
            "ExponentialProfile",
            "ElevatorFeedforward",
            # "ProfiledPIDController",
            # "ObjectToRobotPose",
            "SlewRateLimiter",
            "BangBangController",
            "ChassisSpeeds",
            "KalmanFilter",
            "LinearSystemLoop",
        ],
    ) + [
        (" DCMotor(\W)", r" wpi::math::DCMotor\1"),
        ("([ \(])frc::DCMotor(\W)", r"\1wpi::math::DCMotor\2"),
        ("frc::Debouncer", r"wpi::math::Debouncer"),
        ("frc::ApplyDeadband", r"wpi::math::ApplyDeadband"),
        ("frc::PIDController", r"wpi::math::PIDController"),
        (" ApplyDeadband", r" wpi::math::ApplyDeadband"),
        ("frc::RKDP", r"wpi::math::RKDP"),
        (" RKDP", r" wpi::math::RKDP"),
        ("frc::DesaturateInputVector", r"wpi::math::DesaturateInputVector"),
        ("frc::MakeWhiteNoiseVector", r"wpi::math::MakeWhiteNoiseVector"),
        ("frc::InputModulus", r"wpi::math::InputModulus"),
        ("frc::FloorMod", r"wpi::math::FloorMod"),
        (" InputModulus", r" wpi::math::InputModulus"),
        (" CopySignPow", r" wpi::math::CopySignPow"),
        ("frc::LinearSystemId", r"wpi::math::LinearSystemId"),
        ("frc::DifferentialDriveKinematics", r"wpi::math::DifferentialDriveKinematics"),
        (
            "frc::LinearPlantInversionFeedforward",
            r"wpi::math::LinearPlantInversionFeedforward",
        ),
        ("frc::LTVUnicycleController", r"wpi::math::LTVUnicycleController"),
        (" LinearSystem(\W)", r" wpi::math::LinearSystem\1"),
        ("frc::LinearSystem<", r"wpi::math::LinearSystem<"),
        ("frc::SimpleMotorFeedforward<", r"wpi::math::SimpleMotorFeedforward<"),
        ("frc::DiscretizeAB", "wpi::math::DiscretizeAB"),
        ("frc::LinearQuadraticRegulator", "wpi::math::LinearQuadraticRegulator"),
        ("frc::LinearFilter", "wpi::math::LinearFilter"),
        ("frc::MedianFilter", "wpi::math::MedianFilter"),
    ]


def wpilib_namespace_replacements():

    return (
        namespace_type_helper(
            "frc",
            "wpi",
            [
                "AnalogInput",
                "DigitalInput",
                "DigitalOutput",
                "MotorController",
                "MotorSafety",
                "AddressableLED",
                "LEDPattern",
                # "Encoder",
                "PWMSparkMax",
                "PWMSparkMax",
                "MechanismLigament2d",
            ],
        )
        + namespace_type_helper(
            "frc::sim",
            "wpi::sim",
            [
                "SingleJointedArmSim",
                # "Mechanism2d",
                # "MechanismRoot2d",
            ],
        )
        + [
            ("frc::err", "wpi::err"),
            ("frc::StartRobot", "wpi::StartRobot"),
            ("frc::TimedRobot", "wpi::TimedRobot"),
        ]
    )


NAMESPACE_PROJECT_REPLACEMENTS = [
    (
        "apriltag",
        "frc",
        "wpi::apriltag",
        wpiutil_namespace_replacements() + wpimath_namespace_replacements(),
    ),
    (
        "cameraserver/src/main/native/include/wpi/cameraserver",
        "frc",
        "wpi",
        [
            (r"\(cs::", "(wpi::cs::"),
            (r" cs::", " wpi::cs::"),
        ],
    ),
    (
        "cameraserver/src/main/native/include/wpi/vision",
        "frc",
        "wpi::vision",
        wpiutil_namespace_replacements()
        + [
            (r"\(cs::", "(wpi::cs::"),
            (r" cs::", " wpi::cs::"),
        ],
    ),
    (
        "cameraserver/src/main/native/cpp/cameraserver",
        "frc",
        "wpi",
        wpiutil_namespace_replacements()
        + [
            # (r"\(cs::", "(wpi::cs::"),
            # (r" cs::", " wpi::cs::"),
        ],
    ),
    (
        "cameraserver/src/main/native/cpp/vision",
        "frc",
        "wpi::vision",
        wpiutil_namespace_replacements()
        + [
            ("frc::GetCameraServerShared", "wpi::GetCameraServerShared"),
            # (r"\(cs::", "(wpi::cs::"),
            # (r" cs::", " wpi::cs::"),
        ],
    ),
    (
        "command",
        "frc2",
        "wpi::cmd",
        wpiutil_namespace_replacements()
        + hal_namespace_replacements()
        + wpimath_namespace_replacements()
        + wpilib_namespace_replacements()
        + [
            ("frc::", "wpi::"),
        ],
    ),
    (
        "cscore",
        "cs",
        "wpi::cs",
        wpiutil_namespace_replacements()
        + wpinet_namespace_replacements()
        + [
            ("([\(< ])cs::", r"\1wpi::cs::"),
            (" ::cs::", " ::wpi::cs::"),
            (r"\(::cs::", "(::wpi::cs::"),
        ],
    ),
    ("datalog", None, None, wpiutil_namespace_replacements()),
    (
        "hal",
        "hal",
        "wpi::hal",
        wpiutil_namespace_replacements()
        + [
            ("^hal::", "wpi::hal::"),
            (" hal::", " wpi::hal::"),
            (" ::hal::", " ::wpi::hal::"),
            ("frc::", "wpi::"),
        ],
    ),
    ("fields", "fields", "wpi::fields", []),
    (
        "hal",
        "hal",
        "wpi::hal",
        wpiutil_namespace_replacements()
        + wpinet_namespace_replacements()
        + [
            ("^hal::", "wpi::hal::"),
            (" hal::", " wpi::hal::"),
            (" ::hal::", " ::wpi::hal::"),
            ("frc::", "wpi::"),
        ],
    ),
    (
        "glass",
        "glass",
        "wpi::glass",
        wpiutil_namespace_replacements()
        + wpimath_namespace_replacements()
        + [
            ("([&\( <])glass::", r"\1wpi::glass::"),
            (" fields::", " wpi::fields::"),
        ],
    ),
    ("ntcore", "nt", "wpi::nt", wpiutil_namespace_replacements()),
    # wpigui namespace good
    (
        "wpilibc",
        "frc",
        "wpi",
        wpiutil_namespace_replacements()
        + hal_namespace_replacements()
        + wpimath_namespace_replacements(),
    ),
    (
        "wpimath",
        "frc",
        "wpi::math",
        wpiutil_namespace_replacements()
        + [
            ("frc::Timer", "wpi::Timer"),
        ],
    ),
    # # # TODO wpinet
    # (
    #     "wpinet",
    #     "wpi",
    #     "wpi::net",
    #     # "wpi::uv",
    #     # "wpi::net::uv",
    #     wpiutil_namespace_replacements()
    #     + [
    #         ("wpi::uv", "wpi::net::uv"),
    #         # ("wpi::", "wpi::util::"),
    #         # ("namespace wpi {", "namespace wpi::util {"),
    #         # ("}  // namespace wpi", "}  // namespace wpi::util"),
    #         # ("} // namespace wpi", "} // namespace wpi::util"),
    #         # ("using namespace wpi;", "using namespace wpi::util;"),
    #         # ("}    // end namespace wpi", "}    // end namespace wpi::util"),
    #         # ("} // end namespace wpi", "} // end namespace wpi::util"),
    #     ],
    #     # wpiutil_namespace_replacements(),
    # ),
    # (
    #     "wpinet",
    #     "wpi",
    #     "wpi::net",
    #     [
    #         # ("wpi::", "wpi::util::"),
    #         # ("namespace wpi {", "namespace wpi::util {"),
    #         # ("}  // namespace wpi", "}  // namespace wpi::util"),
    #         # ("} // namespace wpi", "} // namespace wpi::util"),
    #         # ("using namespace wpi;", "using namespace wpi::util;"),
    #         # ("}    // end namespace wpi", "}    // end namespace wpi::util"),
    #         # ("} // end namespace wpi", "} // end namespace wpi::util"),
    #     ]
    #     # wpiutil_namespace_replacements(),
    # ),
    # # # TODO wpiutil
    # (
    #     "wpiutil",
    #     None,
    #     None,
    #     [
    #         ("wpi::", "wpi::util::"),
    #         ("namespace wpi {", "namespace wpi::util {"),
    #         ("}  // namespace wpi", "}  // namespace wpi::util"),
    #         ("} // namespace wpi", "} // namespace wpi::util"),
    #         ("using namespace wpi;", "using namespace wpi::util;"),
    #         ("}    // end namespace wpi", "}    // end namespace wpi::util"),
    #         ("} // end namespace wpi", "} // end namespace wpi::util"),
    #     ]
    #     # wpiutil_namespace_replacements(),
    # ),
    (
        "xrpVendordep",
        "frc",
        "wpi::xrp",
        wpinet_namespace_replacements()
        + wpimath_namespace_replacements()
        + wpilib_namespace_replacements(),
    ),
    (
        "romiVendordep",
        "frc",
        "wpi::romi",
        wpinet_namespace_replacements()
        + wpimath_namespace_replacements()
        + wpilib_namespace_replacements()
        + [
            ("frc::Timer", "wpi::Timer"),
        ],
    ),
    (
        "developerRobot",
        None,
        None,
        wpimath_namespace_replacements() + wpilib_namespace_replacements() + [],
    ),
    (
        "benchmark",
        None,
        None,
        wpimath_namespace_replacements() + wpilib_namespace_replacements() + [],
    ),
    (
        "tools",
        None,
        None,
        wpiutil_namespace_replacements()
        + wpimath_namespace_replacements()
        + wpilib_namespace_replacements()
        + [
            ("([&\( <])glass::", r"\1wpi::glass::"),
            ("namespace glass {", "namespace wpi::glass {"),
            ("^glass::", "wpi::glass::"),
        ],
    ),
    (
        "simulation",
        None,
        None,
        wpiutil_namespace_replacements() + wpinet_namespace_replacements()
        # + wpimath_namespace_replacements()
        # + wpilib_namespace_replacements()
        + [
            ("([&\( <])glass::", r"\1wpi::glass::"),
            # ("namespace glass {", "namespace wpi::glass {"),
            ("^glass::", "wpi::glass::"),
        ],
    ),
    (
        "wpilibcExamples",
        None,
        None,
        wpiutil_namespace_replacements()
        + wpimath_namespace_replacements()
        + wpilib_namespace_replacements()
        + [
            ("frc2::", "wpi::cmd::"),
            ("frc::AprilTagDetector", "wpi::apriltag::AprilTagDetector"),
            ("frc::AprilTagDetection", "wpi::apriltag::AprilTagDetection"),
            ("frc::AprilTagPoseEstimator", "wpi::apriltag::AprilTagPoseEstimator"),
            ("frc::AprilTagField", "wpi::apriltag::AprilTagField"),
            # ("([&\( <])glass::", r"\1wpi::glass::"),
            # ("namespace glass {", "namespace wpi::glass {"),
            # ("^glass::", "wpi::glass::"),
            ("frc::OnBoardIO", "wpi::romi::OnBoardIO"),
            ("frc::RomiGyro", "wpi::romi::RomiGyro"),
            ("frc::XRPOnBoardIO", "wpi::xrp::XRPOnBoardIO"),
            ("frc::XRPServo", "wpi::xrp::XRPServo"),
            ("frc::XRPMotor", "wpi::xrp::XRPMotor"),
            ("frc::XRPGyro", "wpi::xrp::XRPGyro"),
            (" cs::", " wpi::cs::"),
            ("frc::", "wpi::"),
        ],
    ),
]


def _make_commit(msg):
    pass
    # subprocess.check_call(["git", "add", "."])
    # subprocess.check_call(["git", "commit", "-m", msg])


def rename_projects():
    for _, new in RawConfig.PROJECT_RENAMES:
        try:
            if os.path.exists(new):
                shutil.rmtree(new)
        except:
            pass

    for original, new in RawConfig.PROJECT_RENAMES:
        original = pathlib.Path(original)
        new = pathlib.Path(new)

        new.parent.mkdir(parents=True, exist_ok=True)
        original.rename(new)

    _make_commit("Move subprojects")


def fixup_project_renames():
    def fixup_filter(full_file):
        suffix = full_file.split(".")[-1]

        print(full_file)
        return suffix not in [
            "pyc",
            "jar",
            "gz",
            "png",
            "jpg",
            "icns",
            "ico",
            "avi",
            "mp4",
            "bat",
        ]

    def fixup_impl(contents):
        contents = contents.replace("wpilibNewCommands", "command")
        contents = contents.replace("wpilibnewcommands", "command")
        contents = contents.replace("fieldImages", "fields")

        return contents

    crawl_and_replace(".", fixup_filter, fixup_impl)


def _preprocess_cc_file(original_dir, new_dir, original_file, include_root):
    original_rel = original_file.relative_to(include_root)

    if original_file.suffix == ".h" and "thirdparty" not in str(original_file):
        destination_file = include_root / (
            str(original_rel).replace(original_dir, new_dir) + "pp"
        )
    else:
        destination_file = include_root / str(original_rel).replace(
            original_dir, new_dir
        )
    destination_rel = destination_file.relative_to(include_root)

    return original_file, destination_file, original_rel, destination_rel


def preprocess_cc_renames(preprocessor_file):
    file_renames = {}
    include_replacements = {}

    for include_root, original, new in RawConfig.CC_FOLDER_RENAMES:
        include_root = pathlib.Path(include_root)

        for root, _, files in os.walk(include_root):
            root = pathlib.Path(root)
            for f in files:
                original_file = root / f

                if original not in str(root):
                    print(f"Skipping {original_file}")
                    continue

                res = _preprocess_cc_file(original, new, original_file, include_root)
                if res:
                    original_file, destination_file, original_rel, destination_rel = res

                    file_renames[str(original_file)] = str(destination_file)
                    include_replacements[str(original_rel)] = str(destination_rel)

    for include_root, replacements in RawConfig.CC_FILE_RENAMES:
        include_root = pathlib.Path(include_root)
        for original, new in replacements:
            original_file = include_root / original
            destination_file = include_root / new
            file_renames[str(original_file)] = str(destination_file)
            include_replacements[original] = str(new)

    include_replacements["EventLoop.h"] = "EventLoop.hpp"
    include_replacements["PneumaticsBase.h"] = "PneumaticsBase.hpp"
    include_replacements["EdgeConfiguration.h"] = "EdgeConfiguration.hpp"

    include_replacements["HandlesInternal.h"] = "HandlesInternal.hpp"
    include_replacements["util/Color.h"] = "wpi/util/Color.hpp"
    include_replacements["Color.h"] = "wpi/util/Color.hpp"
    include_replacements["util/Color8Bit.h"] = "wpi/util/Color8Bit.hpp"
    include_replacements["BooleanEvent.h"] = "wpi/event/BooleanEvent.hpp"
    include_replacements["../../include/frc/controller/BangBangController.h"] = (
        "wpi/math/controller/BangBangController.hpp"
    )
    include_replacements["MechanismObject2d.h"] = (
        "wpi/smartdashboard/MechanismObject2d.hpp"
    )

    include_replacements["Odometry.h"] = "wpi/math/kinematics/Odometry.hpp"
    include_replacements["Odometry3d.h"] = "wpi/math/kinematics/Odometry3d.hpp"
    include_replacements["SwerveDriveKinematics.h"] = (
        "wpi/math/kinematics/SwerveDriveKinematics.hpp"
    )
    include_replacements["SwerveModulePosition.h"] = (
        "wpi/math/kinematics/SwerveModulePosition.hpp"
    )
    include_replacements["SwerveModuleState.h"] = (
        "wpi/math/kinematics/SwerveModuleState.hpp"
    )
    include_replacements["Trigger.h"] = "wpi/command/button/Trigger.hpp"

    return file_renames, include_replacements


def run_cc_renames(pp_config: PreprocessedConfig):

    for original, new in pp_config.cc_file_renames.items():
        new = pathlib.Path(new)
        new.parent.mkdir(parents=True, exist_ok=True)
        if pathlib.Path(original).exists():
            shutil.move(original, new)

    _make_commit("Move cc files")


def run_cc_include_fixup(pp_config):
    def cc_replacement_filter(full_file):
        if full_file.endswith("/pyproject.toml"):
            return True

        suffix = full_file.split(".")[-1]
        return suffix in ["c", "cpp", "h", "hpp", "jinja", "mm"]

    def cc_replacement_impl(contents):
        for old_pkg, new_pkg in pp_config.cc_incude_replacements.items():
            contents = contents.replace(f'"{old_pkg}"', f'"{new_pkg}"')
            contents = contents.replace(f"<{old_pkg}>", f"<{new_pkg}>")

        return contents

    crawl_and_replace(".", cc_replacement_filter, cc_replacement_impl)

    _make_commit("Run cc include replacements")


def load_pp_config(preprocessor_file):
    with open(preprocessor_file, "r") as f:
        pp = json.load(f)

    # return pp["cc_file_renames"], pp["cc_incude_replacements"]

    return PreprocessedConfig(
        cc_file_renames=pp["cc_file_renames"],
        cc_incude_replacements=pp["cc_incude_replacements"],
        java_pkg_renames=pp["java_pkg_renames"],
        java_file_renames=pp["java_file_renames"],
        java_class_package_overrides=pp["java_class_package_overrides"],
    )


def generic_renames():
    print("Generic Renames:")
    for original, new in RawConfig.GENERIC_RENAMES:
        print(f"{original} -> {new}")
        if os.path.exists(original):
            pathlib.Path(new).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(original, new)

    _make_commit("Generic Renames")


def crawl_for_renames(
    file_renames, include_root, subpath, old_pkg_as_dir, new_pkg_as_dir
):
    for root, _, files in os.walk(include_root + subpath):
        for f in files:
            original_file = pathlib.Path(root) / f
            new_file = str((pathlib.Path(root) / f)).replace(
                old_pkg_as_dir, new_pkg_as_dir
            )
            if str(original_file) != new_file:
                file_renames[str(original_file)] = new_file


def preprocess_java_renames():

    full_package_replacements = {}

    file_renames = {}

    for project, old_pkg, new_pkg in RawConfig.JAVA_PROJECT_REPLACMENTS:
        old_pkg_as_dir = old_pkg.replace(".", "/")
        new_pkg_as_dir = new_pkg.replace(".", "/")
        full_package_replacements[old_pkg] = new_pkg
        full_package_replacements[old_pkg.replace(".", "_")] = new_pkg.replace(".", "_")
        full_package_replacements[old_pkg_as_dir] = new_pkg_as_dir

        include_root = project
        crawl_for_renames(
            file_renames, include_root, "/src/main/java", old_pkg_as_dir, new_pkg_as_dir
        )
        crawl_for_renames(
            file_renames, include_root, "/src/dev/java", old_pkg_as_dir, new_pkg_as_dir
        )
        crawl_for_renames(
            file_renames,
            include_root,
            "/src/generated/main/java",
            old_pkg_as_dir,
            new_pkg_as_dir,
        )
        crawl_for_renames(
            file_renames, include_root, "/src/test/java", old_pkg_as_dir, new_pkg_as_dir
        )

    class_import_renames = {}
    class_package_overrides = {}
    for project, replacements in RawConfig.JAVA_FILE_RENAMES:
        for old_pkg, new_pkg, class_name in replacements:
            print("!!!", old_pkg, new_pkg, class_name)
            old_pkg = old_pkg.replace("/", ".")
            new_pkg = new_pkg.replace("/", ".")

            old_pkg_as_dir = old_pkg.replace(".", "/")
            new_pkg_as_dir = new_pkg.replace(".", "/")

            original_file = (
                pathlib.Path(project)
                / "src/main/java"
                / old_pkg_as_dir
                / (class_name + ".java")
            )
            new_file = (
                pathlib.Path(project)
                / "src/main/java"
                / new_pkg_as_dir
                / (class_name + ".java")
            )
            if original_file.exists():
                class_import_renames[old_pkg + "." + class_name] = (
                    new_pkg + "." + class_name
                )
                class_package_overrides[str(new_file)] = new_pkg
                file_renames[str(original_file)] = str(new_file)

            original_file = (
                pathlib.Path(project)
                / "src/test/java"
                / old_pkg_as_dir
                / (class_name + ".java")
            )
            new_file = (
                pathlib.Path(project)
                / "src/test/java"
                / new_pkg_as_dir
                / (class_name + ".java")
            )
            if original_file.exists():
                class_import_renames[old_pkg + "." + class_name] = (
                    new_pkg + "." + class_name
                )
                class_package_overrides[str(new_file)] = new_pkg
                file_renames[str(original_file)] = str(new_file)

            original_file = (
                pathlib.Path(project)
                / "src/test/java"
                / old_pkg_as_dir
                / (class_name + "Test.java")
            )
            new_file = (
                pathlib.Path(project)
                / "src/test/java"
                / new_pkg_as_dir
                / (class_name + "Test.java")
            )
            if original_file.exists():
                class_import_renames[old_pkg + "." + class_name + "Test"] = (
                    new_pkg + "." + class_name + "Test"
                )
                class_package_overrides[str(new_file)] = new_pkg
                file_renames[str(original_file)] = str(new_file)

            original_file = (
                pathlib.Path(project)
                / "src/generated/main/java"
                / old_pkg_as_dir
                / (class_name + ".java")
            )
            new_file = (
                pathlib.Path(project)
                / "src/generated/main/java"
                / new_pkg_as_dir
                / (class_name + ".java")
            )
            if "motorcontrol" in str(original_file):
                print("++++", original_file, new_file, class_name)
            if original_file.exists():
                print("----", original_file, new_file)
                class_import_renames[old_pkg + "." + class_name] = (
                    new_pkg + "." + class_name
                )
                class_package_overrides[str(new_file)] = new_pkg
                file_renames[str(original_file)] = str(new_file)

            # rename_java_file(package_replacements, project, "src/main/java", old_pkg, new_pkg, class_name)
            # rename_java_file(package_replacements, project, "src/test/java", old_pkg, new_pkg, class_name + "Test")
            # rename_java_file(package_replacements, project, "src/generated/main/java", old_pkg, new_pkg, class_name + "Test")

    #     original_file = (
    #         pathlib.Path(project)
    #         / subpath
    #         / old_pkg
    #         / (class_name + ".java")
    #     )
    #     new_file = (
    #         pathlib.Path(project)
    #         / subpath
    #         / new_pkg
    #         / (class_name + ".java")
    #     )

    #     original_full_name = old_pkg.replace("/", ".") + "." + class_name
    #     new_full_name = new_pkg.replace("/", ".") + "." + class_name

    package_replacements = {}
    package_replacements.update(class_import_renames)
    package_replacements.update(full_package_replacements)

    return package_replacements, file_renames, class_package_overrides


def run_java_renames(pp_config: PreprocessedConfig):

    for original_file, new_file in pp_config.java_file_renames.items():
        pathlib.Path(new_file).parent.mkdir(parents=True, exist_ok=True)
        if pathlib.Path(original_file).exists():
            shutil.move(original_file, new_file)

    _make_commit("Move java files")


def run_java_fixup_imports(pp_config: PreprocessedConfig):
    def java_replacement_filter(full_file):
        if full_file.endswith("/CMakeLists.txt"):
            return True
        if "ntcore/src/generate/types.json" in full_file:
            return True
        if "styleguide" in full_file:
            return True
        suffix = full_file.split(".")[-1]
        return suffix in ["java", "cpp", "jinja", "proto", "Extension"]

    def java_replacement_impl(contents):
        for old_pkg, new_pkg in pp_config.java_pkg_renames.items():
            contents = contents.replace(old_pkg, new_pkg)

        return contents

    crawl_and_replace(".", java_replacement_filter, java_replacement_impl)

    for filename, new_pkg in pp_config.java_class_package_overrides.items():
        with open(filename, "r") as f:
            contents = f.read()

        contents = re.sub("package .*;", f"package {new_pkg};", contents)

        with open(filename, "w") as f:
            f.write(contents)

    _make_commit("Run java package replacements")


def run_java_spotless():
    subprocess.check_call(["./gradlew", "spotlessApply"])


# def rename_java_file(package_replacements, project, subpath, old_pkg, new_pkg, class_name):
#     original_file = (
#         pathlib.Path(project)
#         / subpath
#         / old_pkg
#         / (class_name + ".java")
#     )
#     new_file = (
#         pathlib.Path(project)
#         / subpath
#         / new_pkg
#         / (class_name + ".java")
#     )

#     original_full_name = old_pkg.replace("/", ".") + "." + class_name
#     new_full_name = new_pkg.replace("/", ".") + "." + class_name

#     package_replacements.add((original_full_name, new_full_name))

#     # if "generated" in str(new_file):
#     print("---", original_file, new_file)
#     if original_file.exists():
#         new_file.parent.mkdir(parents=True, exist_ok=True)
#         shutil.move(original_file, new_file)

#     if new_file.exists():
#         with open(new_file) as f:
#             contents = f.read()

#         original_package = f"package {old_pkg.replace('/', '.')};"
#         new_package = f"package {new_pkg.replace('/', '.')};"
#         contents = contents.replace(original_package, new_package)

#         with open(new_file, "w") as f:
#             f.write(contents)

# def run_java_file_renames():
#     package_replacements = set()

#     for project, replacements in RawConfig.JAVA_FILE_RENAMES:
#         for old_pkg, new_pkg, class_name in replacements:

#             # rename_java_file(package_replacements, project, "src/main/java", old_pkg, new_pkg, class_name)
#             # rename_java_file(package_replacements, project, "src/test/java", old_pkg, new_pkg, class_name + "Test")
#             rename_java_file(package_replacements, project, "src/generated/main/java", old_pkg, new_pkg, class_name + "Test")


#     # for old, new in package_replacements:
#     #     print(f"{old} -> {new}")
#     # return

#     # excluded_dirs = [".venv", ".git", "build", ".gradle"]

#     def java_replacement_filter(full_file):
#         suffix = full_file.split(".")[-1]
#         return suffix in ["java", "cpp"]

#     def java_replacement_impl(contents):
#         for old_pkg, new_pkg in package_replacements:
#             contents = contents.replace(old_pkg, new_pkg)

#         return contents

#     crawl_and_replace(".", java_replacement_filter, java_replacement_impl)

#     _make_commit("Run java package replacements")


def run_namespace_replacements():
    def namespace_replacement_filter(full_file):
        suffix = full_file.split(".")[-1]
        return suffix in ["cpp", "h", "hpp", "mm", "jinja"]

    def namespace_replacement_impl(contents):
        for origin, new in replacements:
            contents = re.sub(origin, new, contents, flags=re.MULTILINE)

        if original_ns is not None:
            contents = contents.replace(
                f"}}  // namespace {original_ns}", f"}}  // namespace {new_ns}"
            )
            contents = contents.replace(
                f"namespace {original_ns} {{", f"namespace {new_ns} {{"
            )
            # contents = contents.replace(
            #     f"namespace {original_ns}::", f"namespace {new_ns}::"
            # )
            contents = contents.replace(
                f"using namespace {original_ns};", f"using namespace {new_ns};"
            )

            if original_ns not in new_ns:
                contents = contents.replace(f"{original_ns}::", f"{new_ns}::")
        return contents

    for project, original_ns, new_ns, replacements in NAMESPACE_PROJECT_REPLACEMENTS:
        print(f"Fixing namespaces for {project}")

        crawl_and_replace(
            project, namespace_replacement_filter, namespace_replacement_impl
        )


def main():
    preprocessor_file = "refactor_layout_pp.json"

    preprocess = True

    # rename_projects()
    fixup_project_renames()

    if preprocess:
        cc_file_renames, cc_include_replacements = preprocess_cc_renames(
            preprocessor_file
        )
        java_pkg_renames, java_file_renames, java_class_package_overrides = (
            preprocess_java_renames()
        )

        pp_config = PreprocessedConfig(
            cc_file_renames=cc_file_renames,
            cc_incude_replacements=cc_include_replacements,
            java_pkg_renames=java_pkg_renames,
            java_file_renames=java_file_renames,
            java_class_package_overrides=java_class_package_overrides,
        )
        with open(preprocessor_file, "w") as f:
            pp_config.write_json(f)
    else:
        pp_config = load_pp_config(preprocessor_file)

    # run_cc_renames(pp_config)
    # run_java_renames(pp_config)
    # generic_renames()

    # run_java_fixup_imports(pp_config)
    # run_cc_include_fixup(pp_config)


if __name__ == "__main__":
    main()
