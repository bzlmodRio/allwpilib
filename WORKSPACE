load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

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

http_archive(
    name = "rules_proto",
    sha256 = "dc3fb206a2cb3441b485eb1e423165b231235a1ea9b031b4433cf7bc1fa460dd",
    strip_prefix = "rules_proto-5.3.0-21.7",
    urls = [
        "https://github.com/bazelbuild/rules_proto/archive/refs/tags/5.3.0-21.7.tar.gz",
    ],
)

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")

rules_proto_dependencies()

rules_proto_toolchains()

# Rules Python
http_archive(
    name = "rules_python",
    sha256 = "94750828b18044533e98a129003b6a68001204038dc4749f40b195b24c38f49f",
    strip_prefix = "rules_python-0.21.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.21.0/rules_python-0.21.0.tar.gz",
)

# Download Extra java rules
http_archive(
    name = "rules_jvm_external",
    sha256 = "f86fd42a809e1871ca0aabe89db0d440451219c3ce46c58da240c7dcdc00125f",
    strip_prefix = "rules_jvm_external-5.2",
    url = "https://github.com/bazelbuild/rules_jvm_external/releases/download/5.2/rules_jvm_external-5.2.tar.gz",
)

load("@rules_jvm_external//:repositories.bzl", "rules_jvm_external_deps")

rules_jvm_external_deps()

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
    sha256 = "4d6010ca5e3bb4d7045b071205afa8db06ec11eb24de3f023d74d77cca765f66",
    strip_prefix = "bazel-lib-1.39.0",
    url = "https://github.com/aspect-build/bazel-lib/releases/download/v1.39.0/bazel-lib-v1.39.0.tar.gz",
)

load("@aspect_bazel_lib//lib:repositories.bzl", "aspect_bazel_lib_dependencies")

aspect_bazel_lib_dependencies()
