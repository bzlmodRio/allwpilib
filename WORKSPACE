load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

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
    name = "python_3_10",
    ignore_root_user_error = True,
    python_version = "3.10",
)

load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "allwpilib_pip_deps",
    python_interpreter_target = "@python_3_10_host//:python",
    requirements_lock = "//:requirements_lock.txt",
)

load("@allwpilib_pip_deps//:requirements.bzl", "install_deps")

install_deps()

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
    "com.google.code.gson:gson:2.10.1",
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

load("@maven//:defs.bzl", "pinned_maven_install")

pinned_maven_install()

# Setup aspect lib
http_archive(
    name = "aspect_bazel_lib",
    sha256 = "a8a92645e7298bbf538aa880131c6adb4cf6239bbd27230f077a00414d58e4ce",
    strip_prefix = "bazel-lib-2.7.2",
    url = "https://github.com/aspect-build/bazel-lib/releases/download/v2.7.2/bazel-lib-v2.7.2.tar.gz",
)

load("@aspect_bazel_lib//lib:repositories.bzl", "aspect_bazel_lib_dependencies")

aspect_bazel_lib_dependencies()

# Download toolchains
http_archive(
    name = "rules_bzlmodrio_toolchains",
    sha256 = "ff25b5f9445cbd43759be4c6582b987d1065cf817c593eedc7ada1a699298c84",
    url = "https://github.com/wpilibsuite/rules_bzlmodRio_toolchains/releases/download/2025-1.bcr2/rules_bzlmodRio_toolchains-2025-1.bcr2.tar.gz",
)

load("@rules_bzlmodrio_toolchains//:maven_deps.bzl", "setup_legacy_setup_toolchains_dependencies")

setup_legacy_setup_toolchains_dependencies()

load("@rules_bzlmodrio_toolchains//toolchains:load_toolchains.bzl", "load_toolchains")

load_toolchains()

#
http_archive(
    name = "rules_bzlmodrio_jdk",
    sha256 = "81869fe9860e39b17e4a9bc1d33c1ca2faede7e31d9538ed0712406f753a2163",
    url = "https://github.com/wpilibsuite/rules_bzlmodRio_jdk/releases/download/17.0.12-7/rules_bzlmodRio_jdk-17.0.12-7.tar.gz",
)

load("@rules_bzlmodrio_jdk//:maven_deps.bzl", "setup_legacy_setup_jdk_dependencies")

setup_legacy_setup_jdk_dependencies()

register_toolchains(
    "@local_roborio//:macos",
    "@local_roborio//:linux",
    "@local_roborio//:windows",
    "@local_systemcore//:macos",
    "@local_systemcore//:linux",
    "@local_systemcore//:windows",
    "@local_raspi_bullseye_32//:macos",
    "@local_raspi_bullseye_32//:linux",
    "@local_raspi_bullseye_32//:windows",
    "@local_raspi_bookworm_32//:macos",
    "@local_raspi_bookworm_32//:linux",
    "@local_raspi_bookworm_32//:windows",
    "@local_bullseye_32//:macos",
    "@local_bullseye_32//:linux",
    "@local_bullseye_32//:windows",
    "@local_bullseye_64//:macos",
    "@local_bullseye_64//:linux",
    "@local_bullseye_64//:windows",
    "@local_bookworm_32//:macos",
    "@local_bookworm_32//:linux",
    "@local_bookworm_32//:windows",
    "@local_bookworm_64//:macos",
    "@local_bookworm_64//:linux",
    "@local_bookworm_64//:windows",
)

setup_legacy_setup_jdk_dependencies()

http_archive(
    name = "bzlmodrio-ni",
    sha256 = "fff62c3cb3e83f9a0d0a01f1739477c9ca5e9a6fac05be1ad59dafcd385801f7",
    url = "https://github.com/wpilibsuite/bzlmodRio-ni/releases/download/2025.2.0/bzlmodRio-ni-2025.2.0.tar.gz",
)

load("@bzlmodrio-ni//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_ni_cpp_dependencies")

setup_legacy_bzlmodrio_ni_cpp_dependencies()

http_archive(
    name = "bzlmodrio-opencv",
    sha256 = "6e8544fae07ed5b4fedc146f6ad083d0d8947e3efb5332a20abc46601a52a1b5",
    url = "https://github.com/wpilibsuite/bzlmodRio-opencv/releases/download/2025.4.10.0-3.bcr2/bzlmodRio-opencv-2025.4.10.0-3.bcr2.tar.gz",
)

load("@bzlmodrio-opencv//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_opencv_cpp_dependencies")

setup_legacy_bzlmodrio_opencv_cpp_dependencies()

load("@bzlmodrio-opencv//:maven_java_deps.bzl", "setup_legacy_bzlmodrio_opencv_java_dependencies")

setup_legacy_bzlmodrio_opencv_java_dependencies()

http_archive(
    name = "bzlmodrio-libssh",
    sha256 = "65caef82554617403a16c79e8bcac6553d40eca3e23197e63275bba22db7d5b5",
    strip_prefix = "bzlmodRio-libssh-8405fbd5eb4e42b495f08f6ccf6fbbe5ced28bb7",
    urls = ["https://github.com/bzlmodrio/bzlmodRio-libssh/archive/8405fbd5eb4e42b495f08f6ccf6fbbe5ced28bb7.tar.gz"],
)

load("@bzlmodrio-libssh//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_libssh_cpp_dependencies")

setup_legacy_bzlmodrio_libssh_cpp_dependencies()

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

# Setup quickbuf compiler
load("//shared/bazel:setup_quickbuf_protoc.bzl", "setup_non_bzlmod_quickbuf_protoc")

setup_non_bzlmod_quickbuf_protoc()

# Setup rules_proto
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
