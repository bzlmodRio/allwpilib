load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("//imgui/bazel:fonts_deps.bzl", "load_font_dependencies")

def load_imgui_deps():
    GLFW_COMMITISH = "6b57e08bb0078c9834889eab871bac2368198c15"
    IMGUI_COMMITISH = "3ea0fad204e994d669f79ed29dcaf61cd5cb571d"
    IMPLOT_COMMITISH = "e80e42e8b4136ddb84ccfe04fa28d0c745828952"
    STB_COMMITISH = "c9064e317699d2e495f36ba4f9ac037e88ee371a"
    GL3W_COMMITISH = "5f8d7fd191ba22ff2b60c1106d7135bb9a335533"

    http_archive(
        name = "gl3w",
        url = "https://github.com/skaslev/gl3w/archive/{}.zip".format(GL3W_COMMITISH),
        sha256 = "e96a650a5fb9530b69a19d36ef931801762ce9cf5b51cb607ee116b908a380a6",
        strip_prefix = "gl3w-{}".format(GL3W_COMMITISH),
        build_file = "//imgui/bazel/subproject_build_files:gl3w.BUILD.bazel",
    )

    http_archive(
        name = "glfw",
        url = "https://github.com/glfw/glfw/archive/{}.zip".format(GLFW_COMMITISH),
        sha256 = "9da97be33d64247ee91ce57ab6a4910c4a3de2ab92fca7c7445937ba73833d21",
        strip_prefix = "glfw-{}".format(GLFW_COMMITISH),
        build_file = "//imgui/bazel/subproject_build_files:glfw.BUILD.bazel",
    )

    http_archive(
        name = "imgui",
        url = "https://github.com/ocornut/imgui/archive/{}.zip".format(IMGUI_COMMITISH),
        sha256 = "3e36f6030eb09237ac6afa60196795e4e029c946ce9fcba819cfecb77755acac",
        strip_prefix = "imgui-{}".format(IMGUI_COMMITISH),
        build_file = "//imgui/bazel/subproject_build_files:imgui.BUILD.bazel",
    )

    http_archive(
        name = "implot",
        url = "https://github.com/epezent/implot/archive/{}.zip".format(IMPLOT_COMMITISH),
        sha256 = "278fa337df61883b36dabc6fe8f62243d7764a6c26fc00aedadadae87e2b00b9",
        strip_prefix = "implot-{}".format(IMPLOT_COMMITISH),
        build_file = "//imgui/bazel/subproject_build_files:implot.BUILD.bazel",
    )

    http_archive(
        name = "stb",
        url = "https://github.com/nothings/stb/archive/{}.zip".format(STB_COMMITISH),
        sha256 = "59527e3ffca9f5a27b8d9bcbe7993182b2005217fc041ad5723e668b50269c76",
        strip_prefix = "stb-{}".format(STB_COMMITISH),
        build_file = "//imgui/bazel/subproject_build_files:stb.BUILD.bazel",
    )

    load_font_dependencies()
