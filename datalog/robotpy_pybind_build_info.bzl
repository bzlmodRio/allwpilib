load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "create_pybind_library", "robotpy_library")
load("//shared/bazel/rules/robotpy:semiwrap_helpers.bzl", "gen_libinit", "gen_modinit_hpp", "gen_pkgconf", "resolve_casters", "run_header_gen")

def wpilog_extension(srcs = [], header_to_dat_deps = [], extra_hdrs = [], includes = [], extra_pyi_deps = []):
    WPILOG_HEADER_GEN = [
        struct(
            class_name = "DataLog",
            yml_file = "semiwrap/DataLog.yml",
            header_root = "$(execpath :robotpy-native-datalog.copy_headers)",
            header_file = "$(execpath :robotpy-native-datalog.copy_headers)/wpi/datalog/DataLog.h",
            tmpl_class_names = [
                ("DataLog_tmpl1", "StructLogEntry"),
                ("DataLog_tmpl2", "StructArrayLogEntry"),
                ("DataLog_tmpl3", "_RawLogEntryImpl"),
                ("DataLog_tmpl4", "_BooleanLogEntryImpl"),
                ("DataLog_tmpl5", "_IntegerLogEntryImpl"),
                ("DataLog_tmpl6", "_FloatLogEntryImpl"),
                ("DataLog_tmpl7", "_DoubleLogEntryImpl"),
                ("DataLog_tmpl8", "_StringLogEntryImpl"),
                ("DataLog_tmpl9", "_BooleanArrayLogEntryImpl"),
                ("DataLog_tmpl10", "_IntegerArrayLogEntryImpl"),
                ("DataLog_tmpl11", "_FloatArrayLogEntryImpl"),
                ("DataLog_tmpl12", "_DoubleArrayLogEntryImpl"),
                ("DataLog_tmpl13", "_StringArrayLogEntryImpl"),
            ],
            trampolines = [
                ("wpi::log::DataLog", "wpi__log__DataLog.hpp"),
                ("wpi::log::DataLogEntry", "wpi__log__DataLogEntry.hpp"),
                ("wpi::log::DataLogValueEntryImpl", "wpi__log__DataLogValueEntryImpl.hpp"),
                ("wpi::log::RawLogEntry", "wpi__log__RawLogEntry.hpp"),
                ("wpi::log::BooleanLogEntry", "wpi__log__BooleanLogEntry.hpp"),
                ("wpi::log::IntegerLogEntry", "wpi__log__IntegerLogEntry.hpp"),
                ("wpi::log::FloatLogEntry", "wpi__log__FloatLogEntry.hpp"),
                ("wpi::log::DoubleLogEntry", "wpi__log__DoubleLogEntry.hpp"),
                ("wpi::log::StringLogEntry", "wpi__log__StringLogEntry.hpp"),
                ("wpi::log::BooleanArrayLogEntry", "wpi__log__BooleanArrayLogEntry.hpp"),
                ("wpi::log::IntegerArrayLogEntry", "wpi__log__IntegerArrayLogEntry.hpp"),
                ("wpi::log::FloatArrayLogEntry", "wpi__log__FloatArrayLogEntry.hpp"),
                ("wpi::log::DoubleArrayLogEntry", "wpi__log__DoubleArrayLogEntry.hpp"),
                ("wpi::log::StringArrayLogEntry", "wpi__log__StringArrayLogEntry.hpp"),
                ("wpi::log::StructLogEntry", "wpi__log__StructLogEntry.hpp"),
                ("wpi::log::StructArrayLogEntry", "wpi__log__StructArrayLogEntry.hpp"),
            ],
        ),
        struct(
            class_name = "DataLogBackgroundWriter",
            yml_file = "semiwrap/DataLogBackgroundWriter.yml",
            header_root = "$(execpath :robotpy-native-datalog.copy_headers)",
            header_file = "$(execpath :robotpy-native-datalog.copy_headers)/wpi/datalog/DataLogBackgroundWriter.h",
            tmpl_class_names = [],
            trampolines = [
                ("wpi::log::DataLogBackgroundWriter", "wpi__log__DataLogBackgroundWriter.hpp"),
            ],
        ),
        struct(
            class_name = "DataLogReader",
            yml_file = "semiwrap/DataLogReader.yml",
            header_root = "$(execpath :robotpy-native-datalog.copy_headers)",
            header_file = "$(execpath :robotpy-native-datalog.copy_headers)/wpi/datalog/DataLogReader.h",
            tmpl_class_names = [],
            trampolines = [
                ("wpi::log::StartRecordData", "wpi__log__StartRecordData.hpp"),
                ("wpi::log::MetadataRecordData", "wpi__log__MetadataRecordData.hpp"),
                ("wpi::log::DataLogRecord", "wpi__log__DataLogRecord.hpp"),
                ("wpi::log::DataLogReader", "wpi__log__DataLogReader.hpp"),
            ],
        ),
        struct(
            class_name = "DataLogWriter",
            yml_file = "semiwrap/DataLogWriter.yml",
            header_root = "$(execpath :robotpy-native-datalog.copy_headers)",
            header_file = "$(execpath :robotpy-native-datalog.copy_headers)/wpi/datalog/DataLogWriter.h",
            tmpl_class_names = [],
            trampolines = [
                ("wpi::log::DataLogWriter", "wpi__log__DataLogWriter.hpp"),
            ],
        ),
    ]

    resolve_casters(
        name = "wpilog.resolve_casters",
        caster_deps = ["//wpiutil:src/main/python/wpiutil/wpiutil-casters.pybind11.json"],
        casters_pkl_file = "wpilog.casters.pkl",
        dep_file = "wpilog.casters.d",
    )

    gen_libinit(
        name = "wpilog.gen_lib_init",
        output_file = "src/main/python/wpilog/_init__wpilog.py",
        modules = ["native.datalog._init_robotpy_native_datalog", "wpiutil._init__wpiutil"],
    )

    gen_pkgconf(
        name = "wpilog.gen_pkgconf",
        libinit_py = "wpilog._init__wpilog",
        module_pkg_name = "wpilog._wpilog",
        output_file = "wpilog.pc",
        pkg_name = "wpilog",
        install_path = "src/main/python/wpilog",
        project_file = "src/main/python/pyproject.toml",
        package_root = "src/main/python/wpilog/__init__.py",
    )

    gen_modinit_hpp(
        name = "wpilog.gen_modinit_hpp",
        input_dats = [x.class_name for x in WPILOG_HEADER_GEN],
        libname = "_wpilog",
        output_file = "semiwrap_init.wpilog._wpilog.hpp",
    )

    run_header_gen(
        name = "wpilog",
        casters_pickle = "wpilog.casters.pkl",
        header_gen_config = WPILOG_HEADER_GEN,
        trampoline_subpath = "src/main/python/wpilog",
        deps = header_to_dat_deps,
        local_native_libraries = [
            "//datalog:robotpy-native-datalog.copy_headers",
            "//wpiutil:robotpy-native-wpiutil.copy_headers",
        ],
    )

    create_pybind_library(
        name = "wpilog",
        install_path = "src/main/python/wpilog/",
        extension_name = "_wpilog",
        generated_srcs = [":wpilog.generated_srcs"],
        semiwrap_header = [":wpilog.gen_modinit_hpp"],
        deps = [
            ":wpilog.tmpl_hdrs",
            ":wpilog.trampoline_hdrs",
            "//datalog:datalog",
            "//wpiutil:wpiutil",
            "//wpiutil:wpiutil_pybind_library",
        ],
        dynamic_deps = [
            "//datalog:shared/datalog",
            "//wpiutil:shared/wpiutil",
        ],
        extra_hdrs = extra_hdrs,
        extra_srcs = srcs,
        includes = includes,
    )

    native.filegroup(
        name = "wpilog.generated_files",
        srcs = [
            "wpilog.gen_modinit_hpp.gen",
            "wpilog.header_gen_files",
            "wpilog.gen_pkgconf",
            "wpilog.gen_lib_init",
        ],
        tags = ["manual"],
    )

def define_pybind_library(name):
    native.filegroup(
        name = "{}.generated_files".format(name),
        srcs = [
            "wpilog.generated_files",
        ],
        tags = ["manual"],
    )

    native.filegroup(
        name = "{}.generated_data_files".format(name),
        srcs = [
            "src/main/python/wpilog/wpilog.pc",
        ],
        tags = ["manual"],
    )

    native.filegroup(
        name = "{}.extra_files".format(name),
        srcs = native.glob(["src/main/python/wpilog/**"], exclude = ["src/main/python/wpilog/**/*.py"], allow_empty = True),
    )

    robotpy_library(
        name = name,
        srcs = native.glob(["src/main/python/wpilog/**/*.py"]) + [
            "src/main/python/wpilog/_init__wpilog.py",
        ],
        data = [
            "{}.generated_data_files".format(name),
            "{}.extra_files".format(name),
            ":src/main/python/wpilog/_wpilog",
            ":wpilog.trampoline_hdr_files",
        ],
        imports = ["src/main/python"],
        deps = [
            "//datalog:robotpy-native-datalog",
            "//wpiutil:robotpy-wpiutil",
        ],
        strip_path_prefixes = ["wpilog/src/main/python/"],
        summary = "Binary wrapper for FRC wpilog library",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-native-datalog==2027.0.0a1.dev0", "robotpy-wpiutil==2027.0.0a1.dev0"],
        entry_points = {
            "pkg_config": ["wpilog = wpilog"],
        },
        visibility = ["//visibility:public"],
    )
