load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "create_pybind_library", "robotpy_library")
load("//shared/bazel/rules/robotpy:semiwrap_helpers.bzl", "gen_libinit", "gen_modinit_hpp", "gen_pkgconf", "resolve_casters", "run_header_gen")

def hal_simulation_extension(srcs = [], header_to_dat_deps = [], extra_hdrs = [], includes = [], extra_pyi_deps = []):
    HAL_SIMULATION_HEADER_GEN = [
        struct(
            class_name = "AddressableLEDData",
            yml_file = "semiwrap/simulation/AddressableLEDData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/AddressableLEDData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "AnalogInData",
            yml_file = "semiwrap/simulation/AnalogInData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/AnalogInData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "CTREPCMData",
            yml_file = "semiwrap/simulation/CTREPCMData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/CTREPCMData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DIOData",
            yml_file = "semiwrap/simulation/DIOData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/DIOData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DigitalPWMData",
            yml_file = "semiwrap/simulation/DigitalPWMData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/DigitalPWMData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DriverStationData",
            yml_file = "semiwrap/simulation/DriverStationData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/DriverStationData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DutyCycleData",
            yml_file = "semiwrap/simulation/DutyCycleData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/DutyCycleData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "EncoderData",
            yml_file = "semiwrap/simulation/EncoderData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/EncoderData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "MockHooks",
            yml_file = "semiwrap/simulation/MockHooks.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/MockHooks.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "NotifierData",
            yml_file = "semiwrap/simulation/NotifierData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/NotifierData.h",
            tmpl_class_names = [],
            trampolines = [
                ("HALSIM_NotifierInfo", "__HALSIM_NotifierInfo.hpp"),
            ],
        ),
        struct(
            class_name = "PWMData",
            yml_file = "semiwrap/simulation/PWMData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/PWMData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "PowerDistributionData",
            yml_file = "semiwrap/simulation/PowerDistributionData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/PowerDistributionData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "REVPHData",
            yml_file = "semiwrap/simulation/REVPHData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/REVPHData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Reset",
            yml_file = "semiwrap/simulation/Reset.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/Reset.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "RoboRioData",
            yml_file = "semiwrap/simulation/RoboRioData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/RoboRioData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "SimDeviceData",
            yml_file = "semiwrap/simulation/SimDeviceData.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/simulation/SimDeviceData.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
    ]

    resolve_casters(
        name = "hal_simulation.resolve_casters",
        caster_deps = ["//wpiutil:src/main/python/wpiutil/wpiutil-casters.pybind11.json"],
        casters_pkl_file = "hal_simulation.casters.pkl",
        dep_file = "hal_simulation.casters.d",
    )

    gen_libinit(
        name = "hal_simulation.gen_lib_init",
        output_file = "src/main/python/hal/simulation/_init__simulation.py",
        modules = ["native.wpihal._init_robotpy_native_wpihal", "wpiutil._init__wpiutil", "ntcore._init__ntcore"],
    )

    gen_pkgconf(
        name = "hal_simulation.gen_pkgconf",
        libinit_py = "hal.simulation._init__simulation",
        module_pkg_name = "hal.simulation._simulation",
        output_file = "hal_simulation.pc",
        pkg_name = "hal_simulation",
        install_path = "src/main/python/hal/simulation",
        project_file = "src/main/python/pyproject.toml",
        package_root = "src/main/python/hal/__init__.py",
    )

    gen_modinit_hpp(
        name = "hal_simulation.gen_modinit_hpp",
        input_dats = [x.class_name for x in HAL_SIMULATION_HEADER_GEN],
        libname = "_simulation",
        output_file = "semiwrap_init.hal.simulation._simulation.hpp",
    )

    run_header_gen(
        name = "hal_simulation",
        casters_pickle = "hal_simulation.casters.pkl",
        header_gen_config = HAL_SIMULATION_HEADER_GEN,
        trampoline_subpath = "src/main/python/hal/simulation",
        deps = header_to_dat_deps,
        local_native_libraries = [
            "//datalog:robotpy-native-datalog.copy_headers",
            "//hal:robotpy-native-wpihal.copy_headers",
            "//ntcore:robotpy-native-ntcore.copy_headers",
            "//wpinet:robotpy-native-wpinet.copy_headers",
            "//wpiutil:robotpy-native-wpiutil.copy_headers",
        ],
    )

    create_pybind_library(
        name = "hal_simulation",
        install_path = "src/main/python/hal/simulation/",
        extension_name = "_simulation",
        generated_srcs = [":hal_simulation.generated_srcs"],
        semiwrap_header = [":hal_simulation.gen_modinit_hpp"],
        deps = [
            ":hal_simulation.tmpl_hdrs",
            ":hal_simulation.trampoline_hdrs",
            "//hal:wpiHal",
            "//ntcore:ntcore",
            "//ntcore:ntcore_pybind_library",
            "//wpiutil:wpiutil",
            "//wpiutil:wpiutil_pybind_library",
        ],
        dynamic_deps = [
            "//hal:shared/wpiHal",
            "//ntcore:shared/ntcore",
            "//wpiutil:shared/wpiutil",
        ],
        extra_hdrs = extra_hdrs,
        extra_srcs = srcs,
        includes = includes,
    )

    native.filegroup(
        name = "hal_simulation.generated_files",
        srcs = [
            "hal_simulation.gen_modinit_hpp.gen",
            "hal_simulation.header_gen_files",
            "hal_simulation.gen_pkgconf",
            "hal_simulation.gen_lib_init",
        ],
        tags = ["manual"],
    )

def wpihal_extension(srcs = [], header_to_dat_deps = [], extra_hdrs = [], includes = [], extra_pyi_deps = []):
    WPIHAL_HEADER_GEN = [
        struct(
            class_name = "AddressableLED",
            yml_file = "semiwrap/AddressableLED.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/AddressableLED.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "AddressableLEDTypes",
            yml_file = "semiwrap/AddressableLEDTypes.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/AddressableLEDTypes.h",
            tmpl_class_names = [],
            trampolines = [
                ("HAL_AddressableLEDData", "__HAL_AddressableLEDData.hpp"),
            ],
        ),
        struct(
            class_name = "AnalogInput",
            yml_file = "semiwrap/AnalogInput.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/AnalogInput.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "CAN",
            yml_file = "semiwrap/CAN.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/CAN.h",
            tmpl_class_names = [],
            trampolines = [
                ("HAL_CANStreamMessage", "__HAL_CANStreamMessage.hpp"),
            ],
        ),
        struct(
            class_name = "CANAPI",
            yml_file = "semiwrap/CANAPI.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/CANAPI.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "CANAPITypes",
            yml_file = "semiwrap/CANAPITypes.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/CANAPITypes.h",
            tmpl_class_names = [],
            trampolines = [
                ("HAL_CANMessage", "__HAL_CANMessage.hpp"),
                ("HAL_CANReceiveMessage", "__HAL_CANReceiveMessage.hpp"),
            ],
        ),
        struct(
            class_name = "CTREPCM",
            yml_file = "semiwrap/CTREPCM.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/CTREPCM.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Constants",
            yml_file = "semiwrap/Constants.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Constants.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Counter",
            yml_file = "semiwrap/Counter.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Counter.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DIO",
            yml_file = "semiwrap/DIO.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/DIO.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DriverStation",
            yml_file = "semiwrap/DriverStation.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/DriverStation.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "DriverStationTypes",
            yml_file = "semiwrap/DriverStationTypes.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/DriverStationTypes.h",
            tmpl_class_names = [],
            trampolines = [
                ("HAL_ControlWord", "__HAL_ControlWord.hpp"),
                ("HAL_JoystickAxes", "__HAL_JoystickAxes.hpp"),
                ("HAL_JoystickPOVs", "__HAL_JoystickPOVs.hpp"),
                ("HAL_JoystickButtons", "__HAL_JoystickButtons.hpp"),
                ("HAL_JoystickDescriptor", "__HAL_JoystickDescriptor.hpp"),
                ("HAL_MatchInfo", "__HAL_MatchInfo.hpp"),
            ],
        ),
        struct(
            class_name = "DutyCycle",
            yml_file = "semiwrap/DutyCycle.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/DutyCycle.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Encoder",
            yml_file = "semiwrap/Encoder.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Encoder.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Extensions",
            yml_file = "semiwrap/Extensions.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Extensions.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "HALBase",
            yml_file = "semiwrap/HALBase.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/HALBase.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "I2C",
            yml_file = "semiwrap/I2C.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/I2C.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "I2CTypes",
            yml_file = "semiwrap/I2CTypes.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/I2CTypes.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Main",
            yml_file = "semiwrap/Main.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Main.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Notifier",
            yml_file = "semiwrap/Notifier.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Notifier.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "PWM",
            yml_file = "semiwrap/PWM.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/PWM.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Ports",
            yml_file = "semiwrap/Ports.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Ports.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "Power",
            yml_file = "semiwrap/Power.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Power.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "PowerDistribution",
            yml_file = "semiwrap/PowerDistribution.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/PowerDistribution.h",
            tmpl_class_names = [],
            trampolines = [
                ("HAL_PowerDistributionVersion", "__HAL_PowerDistributionVersion.hpp"),
                ("HAL_PowerDistributionFaults", "__HAL_PowerDistributionFaults.hpp"),
                ("HAL_PowerDistributionStickyFaults", "__HAL_PowerDistributionStickyFaults.hpp"),
            ],
        ),
        struct(
            class_name = "REVPH",
            yml_file = "semiwrap/REVPH.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/REVPH.h",
            tmpl_class_names = [],
            trampolines = [
                ("HAL_REVPHVersion", "__HAL_REVPHVersion.hpp"),
                ("HAL_REVPHCompressorConfig", "__HAL_REVPHCompressorConfig.hpp"),
                ("HAL_REVPHFaults", "__HAL_REVPHFaults.hpp"),
                ("HAL_REVPHStickyFaults", "__HAL_REVPHStickyFaults.hpp"),
            ],
        ),
        struct(
            class_name = "SerialPort",
            yml_file = "semiwrap/SerialPort.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/SerialPort.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "SimDevice",
            yml_file = "semiwrap/SimDevice.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/SimDevice.h",
            tmpl_class_names = [],
            trampolines = [
                ("hal::SimValue", "hal__SimValue.hpp"),
                ("hal::SimInt", "hal__SimInt.hpp"),
                ("hal::SimLong", "hal__SimLong.hpp"),
                ("hal::SimDouble", "hal__SimDouble.hpp"),
                ("hal::SimEnum", "hal__SimEnum.hpp"),
                ("hal::SimBoolean", "hal__SimBoolean.hpp"),
                ("hal::SimDevice", "hal__SimDevice.hpp"),
            ],
        ),
        struct(
            class_name = "Threads",
            yml_file = "semiwrap/Threads.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/Threads.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
        struct(
            class_name = "HandlesInternal",
            yml_file = "semiwrap/HandlesInternal.yml",
            header_root = "$(execpath :robotpy-native-wpihal.copy_headers)",
            header_file = "$(execpath :robotpy-native-wpihal.copy_headers)/hal/handles/HandlesInternal.h",
            tmpl_class_names = [],
            trampolines = [],
        ),
    ]

    resolve_casters(
        name = "wpihal.resolve_casters",
        caster_deps = ["//wpiutil:src/main/python/wpiutil/wpiutil-casters.pybind11.json"],
        casters_pkl_file = "wpihal.casters.pkl",
        dep_file = "wpihal.casters.d",
    )

    gen_libinit(
        name = "wpihal.gen_lib_init",
        output_file = "src/main/python/hal/_init__wpiHal.py",
        modules = ["native.wpihal._init_robotpy_native_wpihal", "wpiutil._init__wpiutil", "ntcore._init__ntcore"],
    )

    gen_pkgconf(
        name = "wpihal.gen_pkgconf",
        libinit_py = "hal._init__wpiHal",
        module_pkg_name = "hal._wpiHal",
        output_file = "wpihal.pc",
        pkg_name = "wpihal",
        install_path = "src/main/python/hal",
        project_file = "src/main/python/pyproject.toml",
        package_root = "src/main/python/hal/__init__.py",
    )

    gen_modinit_hpp(
        name = "wpihal.gen_modinit_hpp",
        input_dats = [x.class_name for x in WPIHAL_HEADER_GEN],
        libname = "_wpiHal",
        output_file = "semiwrap_init.hal._wpiHal.hpp",
    )

    run_header_gen(
        name = "wpihal",
        casters_pickle = "wpihal.casters.pkl",
        header_gen_config = WPIHAL_HEADER_GEN,
        trampoline_subpath = "src/main/python/hal",
        deps = header_to_dat_deps,
        local_native_libraries = [
            "//datalog:robotpy-native-datalog.copy_headers",
            "//hal:robotpy-native-wpihal.copy_headers",
            "//ntcore:robotpy-native-ntcore.copy_headers",
            "//wpinet:robotpy-native-wpinet.copy_headers",
            "//wpiutil:robotpy-native-wpiutil.copy_headers",
        ],
    )

    create_pybind_library(
        name = "wpihal",
        install_path = "src/main/python/hal/",
        extension_name = "_wpiHal",
        generated_srcs = [":wpihal.generated_srcs"],
        semiwrap_header = [":wpihal.gen_modinit_hpp"],
        deps = [
            ":wpihal.tmpl_hdrs",
            ":wpihal.trampoline_hdrs",
            "//hal:wpiHal",
            "//ntcore:ntcore",
            "//ntcore:ntcore_pybind_library",
            "//wpiutil:wpiutil",
            "//wpiutil:wpiutil_pybind_library",
        ],
        dynamic_deps = [
            "//hal:shared/wpiHal",
            "//ntcore:shared/ntcore",
            "//wpiutil:shared/wpiutil",
        ],
        extra_hdrs = extra_hdrs,
        extra_srcs = srcs,
        includes = includes,
    )

    native.filegroup(
        name = "wpihal.generated_files",
        srcs = [
            "wpihal.gen_modinit_hpp.gen",
            "wpihal.header_gen_files",
            "wpihal.gen_pkgconf",
            "wpihal.gen_lib_init",
        ],
        tags = ["manual"],
    )

def define_pybind_library(name):
    native.filegroup(
        name = "{}.generated_files".format(name),
        srcs = [
            "hal_simulation.generated_files",
            "wpihal.generated_files",
        ],
        tags = ["manual"],
        visibility = ["//visibility:public"],
    )

    native.filegroup(
        name = "{}.generated_data_files".format(name),
        srcs = [
            "src/main/python/hal/simulation/hal_simulation.pc",
            "src/main/python/hal/wpihal.pc",
        ],
        tags = ["manual"],
    )

    native.filegroup(
        name = "{}.extra_files".format(name),
        srcs = native.glob(["src/main/python/hal/**"], exclude = ["src/main/python/hal/**/*.py"], allow_empty = True),
        tags = ["manual"],
    )

    robotpy_library(
        name = name,
        srcs = native.glob(["src/main/python/hal/**/*.py"]) + [
            "src/main/python/hal/simulation/_init__simulation.py",
            "src/main/python/hal/_init__wpiHal.py",
        ],
        data = [
            "{}.generated_data_files".format(name),
            "{}.extra_files".format(name),
            ":src/main/python/hal/simulation/_simulation",
            ":src/main/python/hal/_wpiHal",
            ":hal_simulation.trampoline_hdr_files",
            ":wpihal.trampoline_hdr_files",
        ],
        imports = ["src/main/python"],
        deps = [
            "//hal:robotpy-native-wpihal",
            "//ntcore:pyntcore",
            "//wpiutil:robotpy-wpiutil",
        ],
        strip_path_prefixes = ["hal/src/main/python/"],
        summary = "Binary wrapper for FRC HAL",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-native-wpihal==2027.0.0a1.dev0", "robotpy-ntcore==2027.0.0a1.dev0", "robotpy-wpiutil==2027.0.0a1.dev0"],
        entry_points = {
            "pkg_config": ["hal_simulation = hal.simulation", "wpihal = hal"],
        },
        visibility = ["//visibility:public"],
    )
