# THIS FILE IS AUTO GENERATED

load("@rules_cc//cc:cc_library.bzl", "cc_library")
load("//shared/bazel/rules/robotpy:pybind_rules.bzl", "create_pybind_library", "robotpy_library")
load("//shared/bazel/rules/robotpy:semiwrap_helpers.bzl", "gen_libinit", "gen_modinit_hpp", "gen_pkgconf", "publish_casters", "resolve_casters", "run_header_gen")
load("//shared/bazel/rules/robotpy:semiwrap_tool_helpers.bzl", "create_imports")

def cscore_extension(srcs = [], header_to_dat_deps = [], extra_hdrs = [], includes = [], extra_pyi_deps = []):
    CSCORE_HEADER_GEN = [
        # struct(
        #     class_name = "CameraServer",
        #     yml_file = "semiwrap/CameraServer.yml",
        #     header_root = "cscore/src/main/python/../../../../cameraserver/src/main/native/include",
        #     header_file = "cscore/src/main/python/../../../../cameraserver/src/main/native/include/cameraserver/CameraServer.h",
        #     tmpl_class_names = [],
        #     trampolines = [
        #         ("frc::CameraServer", "frc__CameraServer.hpp"),
        #     ],
        # ),
        struct(
            class_name = "cscore_cpp",
            yml_file = "semiwrap/cscore_cpp.yml",
            header_root = "cscore/src/main/python/../native/include",
            header_file = "cscore/src/main/python/../native/include/cscore_cpp.h",
            tmpl_class_names = [],
            trampolines = [
                ("cs::UsbCameraInfo", "cs__UsbCameraInfo.hpp"),
                ("cs::VideoMode", "cs__VideoMode.hpp"),
                ("cs::RawEvent", "cs__RawEvent.hpp"),
            ],
        ),
        struct(
            class_name = "cscore_oo",
            yml_file = "semiwrap/cscore_oo.yml",
            header_root = "cscore/src/main/python/../native/include",
            header_file = "cscore/src/main/python/../native/include/cscore_oo.h",
            tmpl_class_names = [],
            trampolines = [
                ("cs::VideoProperty", "cs__VideoProperty.hpp"),
                ("cs::VideoSource", "cs__VideoSource.hpp"),
                ("cs::VideoCamera", "cs__VideoCamera.hpp"),
                ("cs::UsbCamera", "cs__UsbCamera.hpp"),
                ("cs::HttpCamera", "cs__HttpCamera.hpp"),
                ("cs::AxisCamera", "cs__AxisCamera.hpp"),
                ("cs::ImageSource", "cs__ImageSource.hpp"),
                ("cs::VideoSink", "cs__VideoSink.hpp"),
                ("cs::MjpegServer", "cs__MjpegServer.hpp"),
                ("cs::ImageSink", "cs__ImageSink.hpp"),
                ("cs::VideoEvent", "cs__VideoEvent.hpp"),
                ("cs::VideoListener", "cs__VideoListener.hpp"),
            ],
        ),
        struct(
            class_name = "cscore_cv",
            yml_file = "semiwrap/cscore_cv.yml",
            header_root = "cscore/src/main/python/../native/include",
            header_file = "cscore/src/main/python/../native/include/cscore_cv.h",
            tmpl_class_names = [],
            trampolines = [
                ("cs::CvSource", "cs__CvSource.hpp"),
                ("cs::CvSink", "cs__CvSink.hpp"),
            ],
        ),
        struct(
            class_name = "cscore_runloop",
            yml_file = "semiwrap/cscore_runloop.yml",
            header_root = "cscore/src/main/python/../native/include",
            header_file = "cscore/src/main/python/../native/include/cscore_runloop.h",
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
            "//cscore:shared/cscore",
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

def define_pybind_library(name):
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
        name = "{}.generated_data_files".format(name),
        srcs = [
            "src/main/python/cscore/cscore.pc",
            "src/main/python/cscore/cscore-casters.pc",
            "src/main/python/cscore/cscore-casters.pybind11.json",
        ],
        tags = ["manual", "robotpy"],
    )

    # Contains all of the non-python files that need to be included in the wheel
    native.filegroup(
        name = "{}.extra_files".format(name),
        srcs = native.glob(["src/main/python/cscore/**"], exclude = ["src/main/python/cscore/**/*.py"], allow_empty = True),
        tags = ["manual", "robotpy"],
    )

    robotpy_library(
        name = name,
        srcs = native.glob(["src/main/python/cscore/**/*.py"]) + [
            "src/main/python/cscore/_init__cscore.py",
        ],
        data = [
            "{}.generated_data_files".format(name),
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
        strip_path_prefixes = ["cscore/src/main/python/"],
        summary = "RobotPy bindings for cscore image processing library",
        project_urls = {"Source code": "https://github.com/robotpy/mostrobotpy"},
        author_email = "RobotPy Development Team <robotpy@googlegroups.com>",
        requires = ["robotpy-wpiutil==2027.0.0a2", "robotpy-wpinet==2027.0.0a2", "pyntcore==2027.0.0a2"],
        entry_points = {
            "pkg_config": ["cscore-casters = cscore", "cscore = cscore"],
        },
        visibility = ["//visibility:public"],
    )

    create_imports(
        name = "{}-create-imports".format(name),
        # project_file = "cscore/src/main/python/pyproject.toml",
        library = [name],
        update_init = ["cscore"],
    )
