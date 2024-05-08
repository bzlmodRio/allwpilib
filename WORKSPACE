load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "build_bazel_apple_support",
    sha256 = "c4bb2b7367c484382300aee75be598b92f847896fb31bbd22f3a2346adf66a80",
    url = "https://github.com/bazelbuild/apple_support/releases/download/1.15.1/apple_support.1.15.1.tar.gz",
)

load(
    "@build_bazel_apple_support//lib:repositories.bzl",
    "apple_support_dependencies",
)

apple_support_dependencies()

http_archive(
    name = "rules_proto",
    sha256 = "303e86e722a520f6f326a50b41cfc16b98fe6d1955ce46642a5b7a67c11c0f5d",
    strip_prefix = "rules_proto-6.0.0",
    url = "https://github.com/bazelbuild/rules_proto/releases/download/6.0.0/rules_proto-6.0.0.tar.gz",
)

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies")

rules_proto_dependencies()

load("@rules_proto//proto:toolchains.bzl", "rules_proto_toolchains")

rules_proto_toolchains()

# Rules Python
http_archive(
    name = "rules_python",
    sha256 = "c68bdc4fbec25de5b5493b8819cfc877c4ea299c0dcb15c244c5a00208cde311",
    strip_prefix = "rules_python-0.31.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.31.0/rules_python-0.31.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

py_repositories()

# Download Extra java rules
http_archive(
    name = "rules_jvm_external",
    sha256 = "08ea921df02ffe9924123b0686dc04fd0ff875710bfadb7ad42badb931b0fd50",
    strip_prefix = "rules_jvm_external-6.1",
    url = "https://github.com/bazelbuild/rules_jvm_external/releases/download/6.1/rules_jvm_external-6.1.tar.gz",
)

load("@rules_jvm_external//:repositories.bzl", "rules_jvm_external_deps")

rules_jvm_external_deps()

# -------------------------
# bzlmodRio
# -------------------------
# local_repository(
#     name = "bzlmodRio",
#     path = "../bzlmodRio/monorepo/bzlmodRio",
# )
http_archive(
    name = "bzlmodRio",
    sha256 = "d976f4a7fa45b44929eee349f9d2923bf4d7ad1954ab6f6dbd4f211942ace4e2",
    strip_prefix = "bzlmodRio-311bfd2a4584eb1e26bff7367f1016f631fee4fc",
    url = "https://github.com/bzlmodRio/bzlmodRio/archive/311bfd2a4584eb1e26bff7367f1016f631fee4fc.tar.gz",
)
# -------------------------

load("@bzlmodRio//private/non_bzlmod:download_dependencies.bzl", "download_dependencies")

download_dependencies(
    allwpilib_version = None,
    apriltaglib_version = "3.3.0-1",
    imgui_version = "2024.1.89.9-1",
    libssh_version = "2024.0.105-1",
    local_monorepo_base = "../bzlmodRio/monorepo",
    navx_version = None,
    ni_version = "2024.2.0",
    opencv_version = "2024.4.8.0-2",
    phoenix_version = None,
    revlib_version = None,
    rules_bazelrio_version = "0.0.13",
    rules_checkstyle_version = None,
    rules_pmd_version = None,
    rules_spotless_version = None,
    rules_toolchains_version = "2024-1",
    rules_wpi_styleguide_version = None,
    rules_wpiformat_version = None,
)

load("@bzlmodRio//private/non_bzlmod:setup_dependencies.bzl", "setup_dependencies")

setup_dependencies()

load("//shared/bazel/deps:repo.bzl", "load_third_party")

load_third_party()

# Initialize repositories for all packages in requirements_lock.txt.
load("@allwpilib_pip_deps//:requirements.bzl", "install_deps")

install_deps()

load("@maven//:defs.bzl", "pinned_maven_install")

pinned_maven_install()

http_archive(
    name = "aspect_bazel_lib",
    sha256 = "a8a92645e7298bbf538aa880131c6adb4cf6239bbd27230f077a00414d58e4ce",
    strip_prefix = "bazel-lib-2.7.2",
    url = "https://github.com/aspect-build/bazel-lib/releases/download/v2.7.2/bazel-lib-v2.7.2.tar.gz",
)

load("@aspect_bazel_lib//lib:repositories.bzl", "aspect_bazel_lib_dependencies", "aspect_bazel_lib_register_toolchains")

# Required bazel-lib dependencies

aspect_bazel_lib_dependencies()

# Register bazel-lib toolchains

aspect_bazel_lib_register_toolchains()

http_archive(
    name = "com_google_protobuf",
    patch_args = ["-p1"],
    patches = [
        "//upstream_utils/protobuf_patches:0001-Fix-sign-compare-warnings.patch",
        "//upstream_utils/protobuf_patches:0002-Remove-redundant-move.patch",
        "//upstream_utils/protobuf_patches:0003-Fix-maybe-uninitialized-warnings.patch",
        "//upstream_utils/protobuf_patches:0004-Fix-coded_stream-WriteRaw.patch",
        "//upstream_utils/protobuf_patches:0005-Suppress-enum-enum-conversion-warning.patch",
        "//upstream_utils/protobuf_patches:0006-Fix-noreturn-function-returning.patch",
        "//upstream_utils/protobuf_patches:0007-Work-around-GCC-12-restrict-warning-compiler-bug.patch",
        "//upstream_utils/protobuf_patches:0008-Disable-MSVC-switch-warning.patch",
        "//upstream_utils/protobuf_patches:0009-Disable-unused-function-warning.patch",
        "//upstream_utils/protobuf_patches:0010-Disable-pedantic-warning.patch",
        "//upstream_utils/protobuf_patches:0011-Avoid-use-of-sprintf.patch",
    ],
    sha256 = "f7042d540c969b00db92e8e1066a9b8099c8379c33f40f360eb9e1d98a36ca26",
    strip_prefix = "protobuf-3.21.12",
    urls = [
        "https://github.com/protocolbuffers/protobuf/archive/refs/tags/v3.21.12.zip",
    ],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

load("@bazel_features//:deps.bzl", "bazel_features_deps")

bazel_features_deps()

# -------------------------
# rules_robotpy_utils
# -------------------------
http_archive(
    name = "rules_robotpy_utils",
    integrity = "sha256-7QlvRqZBYzie3+zzR8o8wJx30jjEucUzDlDRXW7UmjE=",
    strip_prefix = "rules_robotpy_utils-2af8aa27400759465b3dfe593869dcdb3c15e766",
    url = "https://github.com/bzlmodRio/rules_robotpy_utils/archive/2af8aa27400759465b3dfe593869dcdb3c15e766.tar.gz",
)

# local_repository(
#     name = "rules_robotpy_utils",
#     path = "/home/pjreiniger/git/bzlmodRio/monorepo/rules/rules_robotpy_utils",
#     # path = "C:/Users/PJ/git/bzlmodrio/monorepo/rules/rules_robotpy_utils",
# )

# -------------------------
# TO DELETE
# -------------------------
# http_archive(
#   name = "pybind11_bazel",
#   strip_prefix = "pybind11_bazel-2.12.0",
#   urls = ["https://github.com/pybind/pybind11_bazel/archive/v2.12.0.zip"],
# )
#
# http_archive(
#   name = "pybind11",
#   build_file = "@pybind11_bazel//:pybind11-BUILD.bazel",
#   strip_prefix = "pybind11-a5b0cdcb937b2853e012489633d692099dab7078",
#   integrity = "sha256-ONA//pxfMap4Hs1OtYk/Yk4UMBZ3B0PmIBsVoYIjdFE=",
#   urls = ["https://github.com/pybind/pybind11/archive/a5b0cdcb937b2853e012489633d692099dab7078.zip"],
# )

load("@rules_robotpy_utils//:download_dependencies.bzl", "download_rules_robotpy_utils_dependencies")

download_rules_robotpy_utils_dependencies()

load("@rules_robotpy_utils//:setup_dependencies.bzl", "setup_rules_robotpy_utils_dependencies")

setup_rules_robotpy_utils_dependencies()

load("@rules_robotpy_utils_pip_deps//:requirements.bzl", install_rules_robotpy_utils_pip_deps = "install_deps")

install_rules_robotpy_utils_pip_deps()

python_register_toolchains(
    name = "python_3_11",
    ignore_root_user_error = True,
    python_version = "3.11",
)

http_archive(
    name = "rules_bzlmodrio_jdk",
    integrity = "sha256-lomuqGaQPqVLzlGyfDb/mlEyAGPFAV6dF+pr0GINGxg=",
    strip_prefix = "rules_bzlmodrio_jdk-32d4c03e8343a17dbc0b4bdf1a482e77a3d37058",
    urls = [
        "https://github.com/bzlmodRio/rules_bzlmodrio_jdk/archive/32d4c03e8343a17dbc0b4bdf1a482e77a3d37058.zip",
    ],
)

load("@rules_bzlmodrio_jdk//:maven_deps.bzl", "setup_legacy_setup_jdk_dependencies")

setup_legacy_setup_jdk_dependencies()

http_archive(
    name = "rules_python_pytest",
    sha256 = "8b82935e16f7b28e3711a68ae5f88f44d8685ccd906b869f7721fdd4c32f2369",
    strip_prefix = "rules_python_pytest-1.1.0",
    url = "https://github.com/caseyduquettesc/rules_python_pytest/releases/download/v1.1.0/rules_python_pytest-v1.1.0.tar.gz",
)

load("@rules_python_pytest//python_pytest:repositories.bzl", "rules_python_pytest_dependencies")

rules_python_pytest_dependencies()
