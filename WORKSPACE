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

python_register_toolchains(
    name = "python_3_11",
    ignore_root_user_error = True,
    python_version = "3.11",
)

load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "allwpilib_pip_deps",
    requirements_lock = "//:requirements_lock.txt",
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

load("@rules_jvm_external//:defs.bzl", "maven_install")
load("@rules_jvm_external//:specs.bzl", "maven")

maven_artifacts = [
    "org.ejml:ejml-simple:0.43.1",
    "com.fasterxml.jackson.core:jackson-annotations:2.15.2",
    "com.fasterxml.jackson.core:jackson-core:2.15.2",
    "com.fasterxml.jackson.core:jackson-databind:2.15.2",
    "us.hebi.quickbuf:quickbuf-runtime:1.3.3",
    maven.artifact(
        "org.junit.jupiter",
        "junit-jupiter",
        "5.10.1",
        testonly = True,
    ),
    maven.artifact(
        "org.junit.platform",
        "junit-platform-console",
        "1.10.1",
        testonly = True,
    ),
    maven.artifact(
        "org.junit.platform",
        "junit-platform-launcher",
        "1.10.1",
        testonly = True,
    ),
    maven.artifact(
        "org.junit.platform",
        "junit-platform-reporting",
        "1.10.1",
        testonly = True,
    ),
    maven.artifact(
        "com.google.code.gson",
        "gson",
        "2.10.1",
        testonly = False,
    ),
    maven.artifact(
        "org.hamcrest",
        "hamcrest-all",
        "1.3",
        testonly = True,
    ),
    maven.artifact(
        "com.googlecode.junit-toolbox",
        "junit-toolbox",
        "2.4",
        testonly = True,
    ),
    maven.artifact(
        "org.apache.ant",
        "ant",
        "1.10.12",
        testonly = True,
    ),
    maven.artifact(
        "org.apache.ant",
        "ant-junit",
        "1.10.12",
        testonly = True,
    ),
    maven.artifact(
        "org.mockito",
        "mockito-core",
        "4.1.0",
        testonly = True,
    ),
    "com.google.auto.service:auto-service:1.1.1",
    maven.artifact(
        "com.google.testing.compile",
        "compile-testing",
        "0.21.0",
        testonly = True,
    ),
]

maven_install(
    name = "maven",
    artifacts = maven_artifacts,
    maven_install_json = "//:maven_install.json",
    repositories = [
        "https://repo1.maven.org/maven2",
        "https://frcmaven.wpi.edu/artifactory/release/",
    ],
)

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

# Download toolchains
http_archive(
    name = "rules_bzlmodrio_toolchains",
    sha256 = "cd3ff046427e9c6dbc0c86a458c8cf081b8045fc3fb4265d08c0ebfc17f9cb30",
    url = "https://github.com/bzlmodRio/rules_bzlmodRio_toolchains/releases/download/2024-1/rules_bzlmodRio_toolchains-2024-1.tar.gz",
)

load("@rules_bzlmodrio_toolchains//:maven_deps.bzl", "setup_legacy_setup_toolchains_dependencies")

setup_legacy_setup_toolchains_dependencies()

load("@rules_bzlmodrio_toolchains//toolchains:load_toolchains.bzl", "load_toolchains")

load_toolchains()

#
http_archive(
    name = "rules_bzlmodrio_jdk",
    sha256 = "a00d5fa971fbcad8a17b1968cdc5350688397035e90b0cb94e040d375ecd97b4",
    url = "https://github.com/bzlmodRio/rules_bzlmodRio_jdk/releases/download/17.0.8.1-1/rules_bzlmodRio_jdk-17.0.8.1-1.tar.gz",
)

load("@rules_bzlmodrio_jdk//:maven_deps.bzl", "setup_legacy_setup_jdk_dependencies")

setup_legacy_setup_jdk_dependencies()

register_toolchains(
    "@local_roborio//:macos",
    "@local_roborio//:linux",
    "@local_roborio//:windows",
    "@local_raspi_32//:macos",
    "@local_raspi_32//:linux",
    "@local_raspi_32//:windows",
    "@local_bullseye_32//:macos",
    "@local_bullseye_32//:linux",
    "@local_bullseye_32//:windows",
    "@local_bullseye_64//:macos",
    "@local_bullseye_64//:linux",
    "@local_bullseye_64//:windows",
)

setup_legacy_setup_jdk_dependencies()

# Download other dependencies
http_archive(
    name = "rules_bazelrio",
    sha256 = "0c5a98476ac5b606689863b7b9ef3f7d685c47ce2681e448ca977e8e95de31c1",
    url = "https://github.com/bzlmodRio/rules_bazelrio/releases/download/0.0.14/rules_bazelrio-0.0.14.tar.gz",
)

http_archive(
    name = "bzlmodrio-ni",
    sha256 = "02a9b1d9722ad3cc7d55ee31a709938884d981f69634dfe93f92e3986bb7a43f",
    url = "https://github.com/bzlmodRio/bzlmodRio-ni/releases/download/2024.2.1/bzlmodRio-ni-2024.2.1.tar.gz",
)

load("@bzlmodrio-ni//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_ni_cpp_dependencies")

setup_legacy_bzlmodrio_ni_cpp_dependencies()

http_archive(
    name = "bzlmodrio-opencv",
    sha256 = "f61f21220bf3d01d9585af30d23714b774235fe0f5334446745f6eee682a9b14",
    url = "https://github.com/bzlmodRio/bzlmodRio-opencv/releases/download/2024.4.8.0-4/bzlmodRio-opencv-2024.4.8.0-4.tar.gz",
)

load("@bzlmodrio-opencv//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_opencv_cpp_dependencies")

setup_legacy_bzlmodrio_opencv_cpp_dependencies()

load("@bzlmodrio-opencv//:maven_java_deps.bzl", "setup_legacy_bzlmodrio_opencv_java_dependencies")

setup_legacy_bzlmodrio_opencv_java_dependencies()

http_archive(
    name = "bzlmodrio-libssh",
    sha256 = "56b8d02ee82dfc127ad1f41172858bbf244756c31f18d1264760d775f66c21ec",
    url = "https://github.com/bzlmodRio/bzlmodRio-libssh/releases/download/2024.0.105-1/bzlmodRio-libssh-2024.0.105-1.tar.gz",
)

load("@bzlmodrio-libssh//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_libssh_cpp_dependencies")

setup_legacy_bzlmodrio_libssh_cpp_dependencies()
