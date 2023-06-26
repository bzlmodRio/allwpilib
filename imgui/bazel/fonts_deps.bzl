load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def load_font_dependencies():
    PROGGYFONTS_VERSION = "1.1.5"
    FONTAWESOME_VERSION = "6.2.0"
    FIRACODE_VERSION = "6.2"
    DROID_COMMIT = "d3817c246c6e3da7531fa1fbb0b0fca271aae7fb"
    ICONFONTCPPHEADERS_COMMIT = "acd3728de3ee4e2461f8958154bb2dc46f958723"

    http_archive(
        name = "proggy_fonts",
        url = "https://github.com/bluescan/proggyfonts/archive/refs/tags/v{}.zip".format(PROGGYFONTS_VERSION),
        sha256 = "260c5311b655ef1e73bf38947a82d37f14ed51522d3bcaf1b466c2d6225b11bb",
        build_file_content = """
filegroup(
    name = "files",
    srcs = ["proggyfonts-{}/ProggyDotted/ProggyDotted Regular.ttf"],
    visibility = ["//visibility:public"]
)
""".format(PROGGYFONTS_VERSION),
    )

    http_archive(
        name = "font_awesome",
        url = "https://github.com/FortAwesome/Font-Awesome/releases/download/{FONTAWESOME_VERSION}/fontawesome-free-{FONTAWESOME_VERSION}-web.zip".format(FONTAWESOME_VERSION = FONTAWESOME_VERSION),
        sha256 = "923687e03f83b68e074d2f4c8871524cad5e1fe0952ba2d89e85b23403c1183a",
        build_file_content = """
filegroup(
    name = "regular",
    srcs = ["fontawesome-free-{FONTAWESOME_VERSION}-web/webfonts/fa-regular-400.ttf"],
    visibility = ["//visibility:public"]
)
filegroup(
    name = "solid",
    srcs = ["fontawesome-free-{FONTAWESOME_VERSION}-web/webfonts/fa-solid-900.ttf"],
    visibility = ["//visibility:public"]
)
""".format(FONTAWESOME_VERSION = FONTAWESOME_VERSION),
    )

    http_archive(
        name = "droid_fonts",
        url = "https://github.com/grays/droid-fonts/archive/{DROID_COMMIT}.zip".format(DROID_COMMIT = DROID_COMMIT),
        sha256 = "03b5f5b33d0c8a9a0a4b9fe9708eca995a0765c9fbbc423ddb0bd96e096b76c4",
        build_file_content = """
filegroup(
    name = "files",
    srcs = ["droid-fonts-{DROID_COMMIT}/droid/DroidSans.ttf"],
    visibility = ["//visibility:public"]
)
""".format(DROID_COMMIT = DROID_COMMIT),
    )

    http_archive(
        name = "fira_code_fonts",
        url = "https://github.com/tonsky/FiraCode/releases/download/{FIRACODE_VERSION}/Fira_Code_v{FIRACODE_VERSION}.zip".format(FIRACODE_VERSION = FIRACODE_VERSION),
        sha256 = "0949915ba8eb24d89fd93d10a7ff623f42830d7c5ffc3ecbf960e4ecad3e3e79",
        build_file_content = """
filegroup(
    name = "files",
    srcs = ["ttf/FiraCode-Retina.ttf"],
    visibility = ["//visibility:public"]
)
""".format(PROGGYFONTS_VERSION),
    )

    http_archive(
        name = "font_awesome_icons",
        url = "https://github.com/juliettef/IconFontCppHeaders/archive/{ICONFONTCPPHEADERS_COMMIT}.zip".format(ICONFONTCPPHEADERS_COMMIT = ICONFONTCPPHEADERS_COMMIT),
        sha256 = "7842467826a6b8d56e6927737f2f3d3a09aa56756e1628cb1181dc5a00edb2de",
        build_file_content = """
filegroup(
    name = "files",
    srcs = ["IconFontCppHeaders-acd3728de3ee4e2461f8958154bb2dc46f958723/IconsFontAwesome6.h"],
    visibility = ["//visibility:public"]
)
""".format(PROGGYFONTS_VERSION),
    )
