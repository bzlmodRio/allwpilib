load("@rules_pkg//:mappings.bzl", "pkg_filegroup", "pkg_files")
load("//shared/bazel/rules:cc_rules.bzl", "wpilib_cc_library", "wpilib_cc_shared_library", "wpilib_cc_static_library")
load("//shared/bazel/rules:publishing.bzl", "architectures_pkg_zip", "platform_prefix", "wpilib_maven_export")

def wpilib_halsim_extension(
        name,
        init_extension_name,
        srcs = [],
        deps = [],
        dynamic_deps = [],
        static_deps = [],
        auto_export_windows_symbols = True,
        visibility = None,
        shared_library_additional_linker_inputs = [],
        shared_library_user_link_flags = [],
        **kwargs):
    """
    Helper wrapper for creating a HALSIM extension. Provides some of the default argments for creating the library.
    """
    wpilib_cc_library(
        name = name,
        srcs = srcs,
        include_license_files = True,
        target_compatible_with = select({
            "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        visibility = visibility,
        deps = deps,
        **kwargs
    )

    wpilib_cc_library(
        name = "{}_static".format(name),
        srcs = srcs,
        copts = [
            "-DHALSIM_InitExtension=" + init_extension_name,
        ],
        include_license_files = True,
        target_compatible_with = select({
            "@rules_bzlmodrio_toolchains//constraints/is_roborio:roborio": ["@platforms//:incompatible"],
            "@rules_bzlmodrio_toolchains//constraints/is_systemcore:systemcore": ["@platforms//:incompatible"],
            "//conditions:default": [],
        }),
        visibility = visibility,
        deps = deps,
        **kwargs
    )

    wpilib_cc_shared_library(
        name = "shared/{}".format(name),
        auto_export_windows_symbols = auto_export_windows_symbols,
        dynamic_deps = dynamic_deps,
        visibility = visibility,
        deps = [":{}".format(name)],
        additional_linker_inputs = shared_library_additional_linker_inputs,
        user_link_flags = shared_library_user_link_flags,
    )

    wpilib_cc_static_library(
        name = "static/{}".format(name),
        static_deps = static_deps,
        deps = [":{}".format(name)],
        visibility = visibility,
    )

    pkg_files(
        name = "{}-static-files".format(name),
        srcs = [
            ":static/{}".format(name),
        ],
        prefix = platform_prefix("static"),
        strip_prefix = "static",
    )

    pkg_filegroup(
        name = "{}-shared-files".format(name),
        srcs = [
            ":shared/lib{}-shared-files".format(name),
        ],
        prefix = platform_prefix("shared"),
    )

    architectures_pkg_zip(
        name = "{}_static_zip".format(name),
        srcs = [
            ":{}-static-files".format(name),
            "//:license_pkg_files",
        ],
    )

    architectures_pkg_zip(
        name = "{}_shared_zip".format(name),
        srcs = [
            ":{}-shared-files".format(name),
            "//:license_pkg_files",
        ],
    )

    maven_artifact_name = name
    maven_group_id = "edu.wpi.first.halsim"

    wpilib_maven_export(
        name = "{}-cpp_publish".format(name),
        classifier_artifacts = {
            "headers": ":{}-hdrs-zip".format(name),
            "sources": ":{}-srcs-zip".format(name),
        },
        linux_artifacts = {
            "linuxx86-64": ":{}_shared_zip-opt-linux-x86-64".format(name),
            "linuxx86-64debug": ":{}_shared_zip-dbg-linux-x86-64".format(name),
            "linuxx86-64static": ":{}_static_zip-opt-linux-x86-64".format(name),
            "linuxx86-64staticdebug": ":{}_static_zip-dbg-linux-x86-64".format(name),
        },
        maven_coordinates = "{}:{}:$(WPILIB_VERSION)".format(maven_group_id, maven_artifact_name),
        osx_artifacts = {
            "osxuniversal": ":{}_shared_zip-opt-osxuniversal".format(name),
            "osxuniversaldebug": ":{}_shared_zip-dbg-osxuniversal".format(name),
            "osxuniversalstatic": ":{}_static_zip-opt-osxuniversal".format(name),
            "osxuniversalstaticdebug": ":{}_static_zip-dbg-osxuniversal".format(name),
        },
        visibility = ["//visibility:public"],
        windows_artifacts = {
            "windowsarm64": ":{}_shared_zip-opt-windows-arm64".format(name),
            "windowsarm64debug": ":{}_shared_zip-dbg-windows-arm64".format(name),
            "windowsarm64static": ":{}_static_zip-opt-windows-arm64".format(name),
            "windowsarm64staticdebug": ":{}_static_zip-dbg-windows-arm64".format(name),
            "windowsx86-64": ":{}_shared_zip-opt-windows-x86-64".format(name),
            "windowsx86-64debug": ":{}_shared_zip-dbg-windows-x86-64".format(name),
            "windowsx86-64static": ":{}_static_zip-opt-windows-x86-64".format(name),
            "windowsx86-64staticdebug": ":{}_static_zip-dbg-windows-x86-64".format(name),
        },
    )
