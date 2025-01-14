load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive", "http_file")

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
    maven.artifact("org.junit.jupiter", "junit-jupiter", "5.10.1", testonly = True),
    maven.artifact("org.junit.platform", "junit-platform-console", "1.10.1", testonly = True),
    maven.artifact("org.junit.platform", "junit-platform-launcher", "1.10.1", testonly = True),
    maven.artifact("org.junit.platform", "junit-platform-reporting", "1.10.1", testonly = True),
    maven.artifact("com.google.code.gson", "gson", "2.10.1", testonly = False),
    maven.artifact("org.hamcrest", "hamcrest-all", "1.3", testonly = True),
    maven.artifact("com.googlecode.junit-toolbox", "junit-toolbox", "2.4", testonly = True),
    maven.artifact("org.apache.ant", "ant", "1.10.12", testonly = True),
    maven.artifact("org.apache.ant", "ant-junit", "1.10.12", testonly = True),
    maven.artifact("org.mockito", "mockito-core", "4.1.0", testonly = True),
    "com.google.auto.service:auto-service:1.1.1",
    maven.artifact("com.google.testing.compile", "compile-testing", "0.21.0", testonly = True),
]

load("@rules_jvm_external//:defs.bzl", "maven_install")

maven_install(
    name = "maven",
    artifacts = maven_artifacts,
    repositories = [
        "https://repo1.maven.org/maven2",
        "https://frcmaven.wpi.edu/artifactory/release/",
    ],
)

# Setup aspect lib
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
    sha256 = "6087424b77f7ee453a4090510d304e09c8d4725041632b34faf3d8f76cd5aeb4",
    strip_prefix = "bzlmodRio-libssh-8bb529e686069e9b198c0f55302d150df66da5d3",
    urls = ["https://github.com/bzlmodrio/bzlmodRio-libssh/archive/8bb529e686069e9b198c0f55302d150df66da5d3.tar.gz"],
)

load("@bzlmodrio-libssh//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_libssh_cpp_dependencies")

setup_legacy_bzlmodrio_libssh_cpp_dependencies()

# Download toolchains
http_archive(
    name = "rules_bzlmodrio_toolchains",
    sha256 = "fe267e2af53c1def1e962700a9aeda9e8fdfa9fb46b72167c615ec0e25447dd6",
    url = "https://github.com/wpilibsuite/rules_bzlmodRio_toolchains/releases/download/2025-1/rules_bzlmodRio_toolchains-2025-1.tar.gz",
)

load("@rules_bzlmodrio_toolchains//:maven_deps.bzl", "setup_legacy_setup_toolchains_dependencies")

setup_legacy_setup_toolchains_dependencies()

load("@rules_bzlmodrio_toolchains//toolchains:load_toolchains.bzl", "load_toolchains")

load_toolchains()

http_archive(
    name = "rules_bzlmodrio_jdk",
    sha256 = "a00d5fa971fbcad8a17b1968cdc5350688397035e90b0cb94e040d375ecd97b4",
    url = "https://github.com/wpilibsuite/rules_bzlmodRio_jdk/releases/download/17.0.8.1-1/rules_bzlmodRio_jdk-17.0.8.1-1.tar.gz",
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
    sha256 = "197fceac88bf44fb8427d5e000b0083118d3346172dd2ad31eccf83a5e61b3ce",
    url = "https://github.com/wpilibsuite/bzlmodRio-ni/releases/download/2025.0.0/bzlmodRio-ni-2025.0.0.tar.gz",
)

load("@bzlmodrio-ni//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_ni_cpp_dependencies")

setup_legacy_bzlmodrio_ni_cpp_dependencies()

http_archive(
    name = "bzlmodrio-opencv",
    sha256 = "4f4a607956ca8555618736c3058dd96e09d02df19e95088c1e352d2319fd70c7",
    url = "https://github.com/wpilibsuite/bzlmodRio-opencv/releases/download/2025.4.10.0-2/bzlmodRio-opencv-2025.4.10.0-2.tar.gz",
)

load("@bzlmodrio-opencv//:maven_cpp_deps.bzl", "setup_legacy_bzlmodrio_opencv_cpp_dependencies")

setup_legacy_bzlmodrio_opencv_cpp_dependencies()

load("@bzlmodrio-opencv//:maven_java_deps.bzl", "setup_legacy_bzlmodrio_opencv_java_dependencies")

setup_legacy_bzlmodrio_opencv_java_dependencies()

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

load("//shared/bazel/deps:quickbuf_protoc.bzl", "setup_non_bzlmod_quickbuf_protoc")

setup_non_bzlmod_quickbuf_protoc()