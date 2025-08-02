# THIS FILE IS AUTO GENERATED

load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "create_pybind_library", "robotpy_library")
load("//shared/bazel/rules/robotpy:semiwrap_helpers.bzl", "gen_libinit", "gen_modinit_hpp", "gen_pkgconf", "resolve_casters", "run_header_gen")
load("//shared/bazel/rules/robotpy:semiwrap_tool_helpers.bzl", "create_imports")

def romi_extension(srcs = [], header_to_dat_deps = [], extra_hdrs = [], includes = [], extra_pyi_deps = []):
    ROMI_HEADER_GEN = [
        struct(
            class_name = "OnBoardIO",
            yml_file = "semiwrap/OnBoardIO.yml",
            header_root = "$(execpath :robotpy-native-romi.copy_headers)",
            header_file = "$(execpath :robotpy-native-romi.copy_headers)/frc/romi/OnBoardIO.h",
            tmpl_class_names = [],
            trampolines = [
                ("frc::OnBoardIO", "frc__OnBoardIO.hpp"),
            ],
        ),
        struct(
            class_name = "RomiGyro",
            yml_file = "semiwrap/RomiGyro.yml",
            header_root = "$(execpath :robotpy-native-romi.copy_headers)",
            header_file = "$(execpath :robotpy-native-romi.copy_headers)/frc/romi/RomiGyro.h",
            tmpl_class_names = [],
            trampolines = [
                ("frc::RomiGyro", "frc__RomiGyro.hpp"),
            ],
        ),
        struct(
            class_name = "RomiMotor",
            yml_file = "semiwrap/RomiMotor.yml",
            header_root = "$(execpath :robotpy-native-romi.copy_headers)",
            header_file = "$(execpath :robotpy-native-romi.copy_headers)/frc/romi/RomiMotor.h",
            tmpl_class_names = [],
            trampolines = [
                ("frc::RomiMotor", "frc__RomiMotor.hpp"),
            ],
        ),
    ]

    resolve_casters(
        name = "romi.resolve_casters",
        caster_deps = ["//wpimath:src/main/python/wpimath/wpimath-casters.pybind11.json", "//wpiutil:src/main/python/wpiutil/wpiutil-casters.pybind11.json"],
        casters_pkl_file = "romi.casters.pkl",
        dep_file = "romi.casters.d",
    )

    gen_libinit(
        name = "romi.gen_lib_init",
        output_file = "src/main/python/romi/_init__romi.py",
        modules = ["native.romi._init_robotpy_native_romi", "wpilib._init__wpilib", "wpimath.geometry._init__geometry"],
    )

    gen_pkgconf(
        name = "romi.gen_pkgconf",
        libinit_py = "romi._init__romi",
        module_pkg_name = "romi._romi",
        output_file = "romi.pc",
        pkg_name = "romi",
        install_path = "src/main/python/romi",
        project_file = "src/main/python/pyproject.toml",
        package_root = "src/main/python/romi/__init__.py",
    )

    gen_modinit_hpp(
        name = "romi.gen_modinit_hpp",
        input_dats = [x.class_name for x in ROMI_HEADER_GEN],
        libname = "_romi",
        output_file = "semiwrap_init.romi._romi.hpp",
    )

    run_header_gen(
        name = "romi",
        casters_pickle = "romi.casters.pkl",
        header_gen_config = ROMI_HEADER_GEN,
        trampoline_subpath = "src/main/python/romi",
        deps = header_to_dat_deps,
        local_native_libraries = [
            "//datalog:robotpy-native-datalog.copy_headers",
            "//hal:robotpy-native-wpihal.copy_headers",
            "//ntcore:robotpy-native-ntcore.copy_headers",
            "//romiVendordep:robotpy-native-romi.copy_headers",
            "//wpilibc:robotpy-native-wpilib.copy_headers",
            "//wpimath:robotpy-native-wpimath.copy_headers",
            "//wpinet:robotpy-native-wpinet.copy_headers",
            "//wpiutil:robotpy-native-wpiutil.copy_headers",
        ],
    )

    create_pybind_library(
        name = "romi",
        install_path = "src/main/python/romi/",
        extension_name = "_romi",
        generated_srcs = [":romi.generated_srcs"],
        semiwrap_header = [":romi.gen_modinit_hpp"],
        deps = [
            ":romi.tmpl_hdrs",
            ":romi.trampoline_hdrs",
            "//romiVendordep:romiVendordep",
            "//wpilibc:wpilib_pybind_library",
            "//wpilibc:wpilibc",
            "//wpimath:wpimath",
            "//wpimath:wpimath_geometry_pybind_library",
        ],
        dynamic_deps = [
            "//romiVendordep:shared/romiVendordep",
            "//wpilibc:shared/wpilibc",
            "//wpimath:shared/wpimath",
        ],
        extra_hdrs = extra_hdrs,
        extra_srcs = srcs,
        includes = includes,
    )

    native.filegroup(
        name = "romi.generated_files",
        srcs = [
            "romi.gen_modinit_hpp.gen",
            "romi.header_gen_files",
            "romi.gen_pkgconf",
            "romi.gen_lib_init",
        ],
        tags = ["manual", "robotpy"],
    )

def define_pybind_library(name):
    # Helper used to generate all files with one target.
    native.filegroup(
        name = "{}.generated_files".format(name),
        srcs = [
            "romi.generated_files",
        ],
        tags = ["manual", "robotpy"],
        visibility = ["//visibility:public"],
    )

    # Files that will be included in the wheel as data deps
    native.filegroup(
        name = "{}.generated_data_files".format(name),
        srcs = [
            "src/main/python/romi/romi.pc",
        ],
        tags = ["manual", "robotpy"],
    )

    # Contains all of the non-python files that need to be included in the wheel
    native.filegroup(
        name = "{}.extra_files".format(name),
        srcs = native.glob(["src/main/python/romi/**"], exclude = ["src/main/python/romi/**/*.py"], allow_empty = True),
        tags = ["manual", "robotpy"],
    )

    robotpy_library(
        name = name,
        srcs = native.glob(["src/main/python/romi/**/*.py"]) + [
            "src/main/python/romi/_init__romi.py",
        ],
        data = [
            "{}.generated_data_files".format(name),
            "{}.extra_files".format(name),
            ":src/main/python/romi/_romi",
            ":romi.trampoline_hdr_files",
        ],
        imports = ["src/main/python"],
        deps = [
            "//romiVendordep:robotpy-native-romi",
            "//wpilibc:robotpy-wpilib",
        ],
        strip_path_prefixes = ["romi/src/main/python/"],
        summary = "Binary wrapper for WPILib Romi Vendor library",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-native-romi==2027.0.0a2", "wpilib==2027.0.0a2"],
        entry_points = {
            "pkg_config": ["romi = romi"],
        },
        visibility = ["//visibility:public"],
    )

    create_imports(
        name = "{}-create-imports".format(name),
        # project_file = "romiVendordep/src/main/python/pyproject.toml",
        library = [name],
        update_init = ["romi"],
    )
