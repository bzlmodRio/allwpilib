# THIS FILE IS AUTO GENERATED

load("@rules_cc//cc:cc_library.bzl", "cc_library")
load("//shared/bazel/rules/gen:gen-version-file.bzl", "generate_version_file")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "create_pybind_library", "robotpy_library")
load("//shared/bazel/rules/robotpy:semiwrap_helpers.bzl", "gen_libinit", "gen_modinit_hpp", "gen_pkgconf", "make_pyi", "publish_casters", "resolve_casters", "run_header_gen")

def cscore_extension(srcs = [], header_to_dat_deps = [], extra_hdrs = [], includes = []):
    CSCORE_HEADER_GEN = [
        # struct(
        #     class_name = "CameraServer",
        #     yml_file = "semiwrap/CameraServer.yml",
        #     header_root = "src/main/native/include/wpi/cs",
        #     header_file = "src/main/native/include/cameraserver/CameraServer.h",
        #     tmpl_class_names = [],
        #     trampolines = [
        #         ("frc::CameraServer", "frc__CameraServer.hpp"),
        #     ],
        # ),
        struct(
            class_name = "cscore_cpp",
            yml_file = "semiwrap/cscore_cpp.yml",
            header_root = "cscore/src/main/native/include",
            header_file = "cscore/src/main/native/include/wpi/cs/cscore_cpp.hpp",
            tmpl_class_names = [],
            trampolines = [
                ("wpi::cs::UsbCameraInfo", "wpi__cs__UsbCameraInfo.hpp"),
                ("wpi::cs::VideoMode", "wpi__cs__VideoMode.hpp"),
                ("wpi::cs::RawEvent", "wpi__cs__RawEvent.hpp"),
            ],
        ),
        struct(
            class_name = "cscore_oo",
            yml_file = "semiwrap/cscore_oo.yml",
            header_root = "cscore/src/main/native/include",
            header_file = "cscore/src/main/native/include/wpi/cs/cscore_oo.hpp",
            tmpl_class_names = [],
            trampolines = [
                ("wpi::cs::VideoProperty", "wpi__cs__VideoProperty.hpp"),
                ("wpi::cs::VideoSource", "wpi__cs__VideoSource.hpp"),
                ("wpi::cs::VideoCamera", "wpi__cs__VideoCamera.hpp"),
                ("wpi::cs::UsbCamera", "wpi__cs__UsbCamera.hpp"),
                ("wpi::cs::HttpCamera", "wpi__cs__HttpCamera.hpp"),
                ("wpi::cs::AxisCamera", "wpi__cs__AxisCamera.hpp"),
                ("wpi::cs::ImageSource", "wpi__cs__ImageSource.hpp"),
                ("wpi::cs::VideoSink", "wpi__cs__VideoSink.hpp"),
                ("wpi::cs::MjpegServer", "wpi__cs__MjpegServer.hpp"),
                ("wpi::cs::ImageSink", "wpi__cs__ImageSink.hpp"),
                ("wpi::cs::VideoEvent", "wpi__cs__VideoEvent.hpp"),
                ("wpi::cs::VideoListener", "wpi__cs__VideoListener.hpp"),
            ],
        ),
        struct(
            class_name = "cscore_cv",
            yml_file = "semiwrap/cscore_cv.yml",
            header_root = "cscore/src/main/native/include",
            header_file = "cscore/src/main/native/include/wpi/cs/cscore_cv.hpp",
            tmpl_class_names = [],
            trampolines = [
                ("wpi::cs::CvSource", "wpi__cs__CvSource.hpp"),
                ("wpi::cs::CvSink", "wpi__cs__CvSink.hpp"),
            ],
        ),
        struct(
            class_name = "cscore_runloop",
            yml_file = "semiwrap/cscore_runloop.yml",
            header_root = "cscore/src/main/native/include",
            header_file = "cscore/src/main/native/include/wpi/cs/cscore_runloop.hpp",
            tmpl_class_names = [],
            trampolines = [],
        ),
    ]

    resolve_casters(
        name = "cscore.resolve_casters",
        caster_deps = ["//wpiutil:src/main/python/wpiutil/wpiutil-casters.pybind11.json", ":src/main/python/cscore/cscore-casters.pybind11.json"],
        casters_pkl_file = "cscore.casters.pkl",
        dep_file = "cscore.casters.d",
    )

    gen_libinit(
        name = "cscore.gen_lib_init",
        output_file = "src/main/python/cscore/_init__cscore.py",
        modules = ["wpiutil._init__wpiutil", "wpinet._init__wpinet", "ntcore._init__ntcore"],
    )

    gen_pkgconf(
        name = "cscore.gen_pkgconf",
        libinit_py = "cscore._init__cscore",
        module_pkg_name = "cscore._cscore",
        output_file = "cscore.pc",
        pkg_name = "cscore",
        install_path = "src/main/python/cscore",
        project_file = "src/main/python/pyproject.toml",
        package_root = "src/main/python/cscore/__init__.py",
    )

    gen_modinit_hpp(
        name = "cscore.gen_modinit_hpp",
        input_dats = [x.class_name for x in CSCORE_HEADER_GEN],
        libname = "_cscore",
        output_file = "semiwrap_init.cscore._cscore.hpp",
    )

    run_header_gen(
        name = "cscore",
        casters_pickle = "cscore.casters.pkl",
        header_gen_config = CSCORE_HEADER_GEN,
        trampoline_subpath = "src/main/python/cscore",
        deps = header_to_dat_deps,
        local_native_libraries = [
        ],
    )

    create_pybind_library(
        name = "cscore",
        install_path = "src/main/python/cscore/",
        extension_name = "_cscore",
        generated_srcs = [":cscore.generated_srcs"],
        semiwrap_header = [":cscore.gen_modinit_hpp"],
        deps = [
            ":cscore.tmpl_hdrs",
            ":cscore.trampoline_hdrs",
            "//cameraserver:cameraserver",
            "//cscore:cscore",
            "//cscore:cscore-casters",
            "//ntcore:ntcore",
            "//ntcore:ntcore_pybind_library",
            "//wpinet:wpinet",
            "//wpinet:wpinet_pybind_library",
            "//wpiutil:wpiutil",
            "//wpiutil:wpiutil_pybind_library",
        ],
        dynamic_deps = [
            # "//cscore:shared/cscore",
            "//ntcore:shared/ntcore",
            "//wpinet:shared/wpinet",
            "//wpiutil:shared/wpiutil",
        ],
        extra_hdrs = extra_hdrs,
        extra_srcs = srcs,
        includes = includes,
    )

    native.filegroup(
        name = "cscore.generated_files",
        srcs = [
            "cscore.gen_modinit_hpp.gen",
            "cscore.header_gen_files",
            "cscore.gen_pkgconf",
            "cscore.gen_lib_init",
        ],
        tags = ["manual", "robotpy"],
    )

def publish_library_casters():
    publish_casters(
        name = "publish_casters",
        caster_name = "cscore-casters",
        output_json = "src/main/python/cscore/cscore-casters.pybind11.json",
        output_pc = "src/main/python/cscore/cscore-casters.pc",
        project_config = "src/main/python/pyproject.toml",
        package_root = "src/main/python/cscore/__init__.py",
        typecasters_srcs = native.glob(["src/main/python/cscore/cvnp/**/*.h"]),
    )

    cc_library(
        name = "cscore-casters",
        hdrs = native.glob(["src/main/python/cscore/**/*.h"]),
        includes = ["src/main/python/cscore"],
        visibility = ["//visibility:public"],
        tags = ["robotpy"],
    )

def _make_pyi_stubs(name, extra_pyi_deps = []):
    make_pyi(
        name = name + ".make_pyi0",
        extension_package = "cscore._cscore",
        stub_files = [
            "cscore/_cscore.pyi",
            "$(location cscore/_cscore.pyi)",
        ],
        remapping_args = [
            "cscore",
            "cscore/src/main/python/cscore/__init__.py",
            "cscore._init__cscore",
            "$(location :src/main/python/cscore/_init__cscore.py)",
            "cscore._cscore",
            "$(location :src/main/python/cscore/_cscore)",
        ],
        outputs = [
            "cscore/_cscore.pyi",
        ],
        srcs = [
            "src/main/python/cscore/__init__.py",
            ":src/main/python/cscore/_init__cscore.py",
            ":src/main/python/cscore/_cscore",
        ],
        python_deps = [
            "//ntcore:pyntcore",
            "//wpinet:robotpy-wpinet",
            "//wpiutil:robotpy-wpiutil",
        ] + extra_pyi_deps,
    )

    native.filegroup(
        name = name + ".pyi_files",
        srcs = [
            "cscore/_cscore.pyi",
        ],
    )

def define_pybind_library(name, pkgcfgs = [], create_pyi_extra_deps = [], create_imports_extra_deps = []):
    _make_pyi_stubs(name, extra_pyi_deps = create_pyi_extra_deps + create_imports_extra_deps)

    # Helper used to generate all files with one target.
    native.filegroup(
        name = "{}.generated_files".format(name),
        srcs = [
            "cscore.generated_files",
        ],
        tags = ["manual", "robotpy"],
        visibility = ["//visibility:public"],
    )

    # Files that will be included in the wheel as data deps
    native.filegroup(
        name = "{}.generated_pkgcfg_files".format(name),
        srcs = [
            "src/main/python/cscore/cscore.pc",
            "src/main/python/cscore/cscore-casters.pc",
            "src/main/python/cscore/cscore-casters.pybind11.json",
        ] + [name + ".pyi_files"],
        tags = ["manual", "robotpy"],
        visibility = ["//visibility:public"],
    )

    # Contains all of the non-python files that need to be included in the wheel
    native.filegroup(
        name = "{}.extra_files".format(name),
        srcs = native.glob(["src/main/python/cscore/**"], exclude = ["src/main/python/cscore/**/*.py"], allow_empty = True),
        tags = ["manual", "robotpy"],
    )

    generate_version_file(
        name = "{}.generate_version".format(name),
        output_file = "src/main/python/cscore/version.py",
        template = "//shared/bazel/rules/robotpy:version_template.in",
    )

    robotpy_library(
        name = name,
        srcs = native.glob(["src/main/python/cscore/**/*.py"]) + [
            "src/main/python/cscore/_init__cscore.py",
            "{}.generate_version".format(name),
        ],
        data = [
            "{}.generated_pkgcfg_files".format(name),
            "{}.extra_files".format(name),
            ":src/main/python/cscore/_cscore",
            ":cscore.trampoline_hdr_files",
        ],
        imports = ["src/main/python"],
        deps = [
            "//ntcore:pyntcore",
            "//wpinet:robotpy-wpinet",
            "//wpiutil:robotpy-wpiutil",
        ],
        strip_path_prefixes = ["cscore/src/main/python", "cscore"],
        summary = "RobotPy bindings for cscore image processing library",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-wpiutil==2027.0.0a3", "robotpy-wpinet==2027.0.0a3", "pyntcore==2027.0.0a3"],
        entry_points = {
            "pkg_config": ["cscore-casters = cscore", "cscore = cscore"],
        },
        visibility = ["//visibility:public"],
    )

    # create_imports(
    #     name = "{}-create-imports".format(name),
    #     library = [name],
    #     prefix = "src/main/python",
    #     update_init = ["cscore"],
    #     extra_deps = create_imports_extra_deps,
    # )

    # update_yaml_files(
    #     name = "{}-update-yaml".format(name),
    #     yaml_output_directory = "src/main/python/semiwrap",
    #     extra_hdrs = native.glob(["src/main/python/**/*.h"], allow_empty = True) + [
    #     ],
    #     package_root_file = "src/main/python/cscore/__init__.py",
    #     pkgcfgs = pkgcfgs,
    #     pyproject_toml = "src/main/python/pyproject.toml",
    #     yaml_files = native.glob(["src/main/python/semiwrap/**"]),
    # )

    # scan_headers(
    #     name = "{}-scan-headers".format(name),
    #     extra_hdrs = native.glob(["src/main/python/**/*.h"], allow_empty = True) + [

    #     ],
    #     package_root_file = "src/main/python/cscore/__init__.py",
    #     pkgcfgs = pkgcfgs,
    #     pyproject_toml = "src/main/python/pyproject.toml",
    # )
