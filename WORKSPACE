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
    apriltaglib_version = None,
    imgui_version = None,
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

load("@aspect_bazel_lib//lib:repositories.bzl", "aspect_bazel_lib_dependencies")

aspect_bazel_lib_dependencies()

python_register_toolchains(
    name = "python_3_11",
    ignore_root_user_error = True,
    python_version = "3.11",
)

http_archive(
    name = "rules_bzlmodrio_jdk",
    sha256 = "43a475e46852305ffc87f7499e772a42dc5343d7bfcc7631dbca83568712f44f",
    strip_prefix = "rules_bzlmodrio_jdk-d5f0db20a611e4ec4b26f95d9c772e2436b69b55",
    urls = ["https://github.com/wpilibsuite/rules_bzlmodRio_jdk/archive/d5f0db20a611e4ec4b26f95d9c772e2436b69b55.tar.gz"],
)

load("@rules_bzlmodrio_jdk//:maven_deps.bzl", "setup_legacy_setup_jdk_dependencies")

setup_legacy_setup_jdk_dependencies()
