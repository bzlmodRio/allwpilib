load("@rules_cc//cc:defs.bzl", "cc_library")

def wpi_proto_library(
        name,
        proto_files):
    gen_srcs = []
    gen_hdrs = []

    for pf in proto_files:
        gen_srcs.append("generated_proto/" + pf[:-5] + "pb.cc")
        gen_hdrs.append("generated_proto/" + pf[:-5] + "pb.h")

    print(gen_srcs)

    cmd = "$(locations //protoplugin:bazel_proto_generator) --proto_files $(SRCS) --output_files $(OUTS)"
    native.genrule(
        name = "generate_proto",
        srcs = proto_files,
        outs = gen_srcs + gen_hdrs,
        cmd = cmd,
        tools = [
            "//protoplugin:bazel_proto_generator",
        ],
        visibility = ["//visibility:public"],
    )

    cc_library(
        name = "cc_proto",
        srcs = gen_srcs,
        hdrs = gen_hdrs,
        includes = ["generated_proto"],
        visibility = ["//visibility:public"],
        deps = [
            "//wpiutil/src/main/native:wpiutil.static",
        ],
    )
