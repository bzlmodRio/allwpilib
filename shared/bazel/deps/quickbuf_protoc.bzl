load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_file")

QUICKBUF_VERSION = "1.3.2"

def __setup_quickbuf_protoc(mctx):
    http_file(
        name = "quickbuffer_protoc_linux",
        url = "https://repo1.maven.org/maven2/us/hebi/quickbuf/protoc-gen-quickbuf/" + QUICKBUF_VERSION + "/protoc-gen-quickbuf-" + QUICKBUF_VERSION + "-linux-x86_64.exe",
        sha256 = "f9a041bccaa7040db523666ef1b5fe9f6f94e70a82c88951f18f58aadd9c50b5",
        executable = True,
    )

    http_file(
        name = "quickbuffer_protoc_osx",
        url = "https://repo1.maven.org/maven2/us/hebi/quickbuf/protoc-gen-quickbuf/" + QUICKBUF_VERSION + "/protoc-gen-quickbuf-" + QUICKBUF_VERSION + "-osx-x86_64.exe   ",
        # sha256 = "a75b8ad50028c2a82e2f8c2ac857afc17bb4342fdedf77f9fc493e58b47321b2",
        executable = True,
    )

    http_file(
        name = "quickbuffer_protoc_windows",
        url = "https://repo1.maven.org/maven2/us/hebi/quickbuf/protoc-gen-quickbuf/" + QUICKBUF_VERSION + "/protoc-gen-quickbuf-" + QUICKBUF_VERSION + "-windows-x86_64.exe ",
        # sha256 = "71482c5163a7b6ec96d748d6d3c3ad712e7d2610645ba2eea4cb21bc11566e07",
        executable = True,
    )

setup_quickbuf_protoc = module_extension(
    __setup_quickbuf_protoc,
)

def setup_non_bzlmod_quickbuf_protoc():
    __setup_quickbuf_protoc(None)
