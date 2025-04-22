load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")


http_archive(
    name = "rules_cc",
    urls = ["https://github.com/bazelbuild/rules_cc/releases/download/0.0.17/rules_cc-0.0.17.tar.gz"],
    sha256 = "abc605dd850f813bb37004b77db20106a19311a96b2da1c92b789da529d28fe1",
    strip_prefix = "rules_cc-0.0.17",
)

http_archive(
    name = "rules_java",
    urls = ["https://github.com/bazelbuild/rules_java/releases/download/8.11.0/rules_java-8.11.0.tar.gz",],
    sha256 = "d31b6c69e479ffa45460b64dc9c7792a431cac721ef8d5219fc9f603fa2ff877",
)

load("@rules_java//java:rules_java_deps.bzl", "rules_java_dependencies")
rules_java_dependencies()

# note that the following line is what is minimally required from protobuf for the java rules
# consider using the protobuf_deps() public API from @com_google_protobuf//:protobuf_deps.bzl
load("@com_google_protobuf//bazel/private:proto_bazel_features.bzl", "proto_bazel_features")  # buildifier: disable=bzl-visibility
proto_bazel_features(name = "proto_bazel_features")

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
    sha256 = "690e0141724abb568267e003c7b6d9a54925df40c275a870a4d934161dc9dd53",
    strip_prefix = "rules_python-0.40.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.40.0/rules_python-0.40.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

py_repositories()

python_register_toolchains(
    name = "python_3_10",
    ignore_root_user_error = True,
    python_version = "3.10",
)

# Download Extra java rules
http_archive(
    name = "rules_jvm_external",
    sha256 = "08ea921df02ffe9924123b0686dc04fd0ff875710bfadb7ad42badb931b0fd50",
    strip_prefix = "rules_jvm_external-6.1",
    url = "https://github.com/bazelbuild/rules_jvm_external/releases/download/6.1/rules_jvm_external-6.1.tar.gz",
)

load("@rules_jvm_external//:repositories.bzl", "rules_jvm_external_deps")

rules_jvm_external_deps()

http_archive(
    name = "rules_bzlmodrio_jdk",
    integrity = "sha256-SrikyrF2v2lENdqn9aFC//d0TkIE620lR60yXTrWFTs=",
    strip_prefix = "rules_bzlmodrio_jdk-4ecd4cbc97dfbfe2ceefa627de1228e2f2ca5773",
    urls = ["https://github.com/wpilibsuite/rules_bzlmodRio_jdk/archive/4ecd4cbc97dfbfe2ceefa627de1228e2f2ca5773.tar.gz"],
)

# local_repository(
#     name = "bzlmodRio",
#     path = "../bzlmodRio/monorepo/bzlmodRio",
# )
http_archive(
    name = "bzlmodRio",
    sha256 = "f157e74bac16a1f48affb6fd5732afcfdb3838f5366df4a5b559ca1bb6190032",
    strip_prefix = "bzlmodRio-05d4fe3a29210c009c4a6ff9384952c2c774bb98",
    url = "https://github.com/bzlmodRio/bzlmodRio/archive/05d4fe3a29210c009c4a6ff9384952c2c774bb98.tar.gz",
)

http_archive(
    name = "bzlmodrio-opencv",
    sha256 = "a84a108bd543c7884a42ffba9e884941fca447af820374ff7568360854a6337f",
    strip_prefix = "bzlmodRio-opencv-515c8a17dbbdecf1970a04a41131b77eeb33027e",
    urls = ["https://github.com/bzlmodrio/bzlmodrio-opencv/archive/515c8a17dbbdecf1970a04a41131b77eeb33027e.tar.gz"],
)

load("@bzlmodRio//private/non_bzlmod:download_dependencies.bzl", "download_dependencies")

download_dependencies(
    allwpilib_version = None,
    # apriltaglib_version = None,
    # imgui_version = None,
    # libssh_version = "2024.0.105-1",
    local_monorepo_base = "../bzlmodRio/monorepo",
    ni_version = "2025.2.0",
    opencv_version = "2025.4.10.0-3",
    phoenix_version = None,
    revlib_version = None,
    rules_bazelrio_version = "0.0.13",
    rules_checkstyle_version = None,
    rules_pmd_version = None,
    rules_spotless_version = None,
    rules_toolchains_version = "2025-1.bcr2",
    rules_wpi_styleguide_version = None,
    rules_wpiformat_version = None,
    studica_version = None,
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

http_archive(
    name = "bzlmodrio-libssh",
    sha256 = "79f7194e82879af044599883cb3fbf13afe4baf03df6da977d5beaed788fd678",
    strip_prefix = "bzlmodRio-libssh-fc9ad9a0e143c5955cb08f409b7fae53fe6a2b40",
    urls = ["https://github.com/bzlmodrio/bzlmodRio-libssh/archive/fc9ad9a0e143c5955cb08f409b7fae53fe6a2b40.tar.gz"],
)

load("@bzlmodrio-libssh//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_libssh_cpp_dependencies")

setup_legacy_bzlmodrio_libssh_cpp_dependencies()

load("@rules_bzlmodrio_jdk//:maven_deps.bzl", "setup_legacy_setup_jdk_dependencies")

setup_legacy_setup_jdk_dependencies()

http_archive(
    name = "rules_proto",
    sha256 = "0e5c64a2599a6e26c6a03d6162242d231ecc0de219534c38cb4402171def21e8",
    strip_prefix = "rules_proto-7.0.2",
    url = "https://github.com/bazelbuild/rules_proto/releases/download/7.0.2/rules_proto-7.0.2.tar.gz",
)

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies")

rules_proto_dependencies()

load("@rules_proto//proto:setup.bzl", "rules_proto_setup")

rules_proto_setup()
