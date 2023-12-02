#!/usr/bin/env python3

import glob
import os
import sys
from jinja2 import Environment, FileSystemLoader
import json
import argparse


GENERATED_FILES = []


def Output(outPath, outfn, contents):
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    outpathname = f"{outPath}/{outfn}"
    GENERATED_FILES.append(outpathname)

    if os.path.exists(outpathname):
        with open(outpathname, "r") as f:
            if f.read() == contents:
                return

    # File either doesn't exist or has different contents
    with open(outpathname, "w", newline="\n") as f:
        f.write(contents)


def main():
    dirname, _ = os.path.split(os.path.abspath(__file__))

    with open(f"{dirname}/src/generate/types.json") as f:
        types = json.load(f)

    # Java files
    if args.generate_java:
        generate_java_files(dirname, generation_root, types)

    if args.generate_cpp_includes:
        generate_cpp_includes(dirname, generation_root, types)

    if args.generate_cpp_srcs:
        generate_cpp_srcs(dirname, generation_root, types)

    if args.generate_jni:
        generate_jni_files(dirname, generation_root, types)

    if is_bazel:
        diff = set(GENERATED_FILES).difference(files_to_generate)
        if len(diff) != 0:
            raise Exception(
                "File generated that was not listed in bazel:\n  "
                + "\n  ".join(x for x in diff)
            )


def generate_java_files(dirname, generation_root, types):
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/main/java"), autoescape=False
    )
    rootPath = f"{dirname}/src/generated/main/java/edu/wpi/first/networktables"
    for fn in glob.glob(f"{dirname}/src/generate/main/java/*.jinja"):
        template = env.get_template(os.path.basename(fn))
        outfn = os.path.basename(fn)[:-6]  # drop ".jinja"
        if os.path.basename(fn).startswith("NetworkTable") or os.path.basename(
            fn
        ).startswith("Generic"):
            output = template.render(types=types)
            Output(rootPath, outfn, output)
        else:
            for replacements in types:
                output = template.render(replacements)
                if outfn == "Timestamped.java":
                    outfn2 = f"Timestamped{replacements['TypeName']}.java"
                else:
                    outfn2 = f"{replacements['TypeName']}{outfn}"
                Output(rootPath, outfn2, output)


def generate_cpp_includes(dirname, generation_root, types):
    # C++ classes
    env = Environment(
        loader=FileSystemLoader(
            f"{dirname}/src/generate/main/native/include/networktables"
        ),
        autoescape=False,
    )
    rootPath = f"{dirname}/src/generated/main/native/include/networktables"
    for fn in glob.glob(
        f"{dirname}/src/generate/main/native/include/networktables/*.jinja"
    ):
        template = env.get_template(os.path.basename(fn))
        outfn = os.path.basename(fn)[:-6]  # drop ".jinja"
        for replacements in types:
            output = template.render(replacements)
            outfn2 = f"{replacements['TypeName']}{outfn}"
            Output(rootPath, outfn2, output)

    # C++ handle API (header)
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/main/native/include"),
        autoescape=False,
    )
    template = env.get_template("ntcore_cpp_types.h.jinja")
    output = template.render(types=types)
    Output(
        f"{dirname}/src/generated/main/native/include",
        "ntcore_cpp_types.h",
        output,
    )

    # C++ handle API (source)
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/main/native/cpp"),
        autoescape=False,
    )
    template = env.get_template("ntcore_cpp_types.cpp.jinja")
    output = template.render(types=types)
    Output(f"{dirname}/src/generated/main/native/cpp", "ntcore_cpp_types.cpp", output)

    # C handle API (header)
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/main/native/include"),
        autoescape=False,
    )
    template = env.get_template("ntcore_c_types.h.jinja")
    output = template.render(types=types)
    Output(
        f"{dirname}/src/generated/main/native/include",
        "ntcore_c_types.h",
        output,
    )


def generate_cpp_srcs(dirname, generation_root, types):
    # C++ handle API (source)
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/cpp"), autoescape=False
    )
    template = env.get_template("ntcore_cpp_types.cpp.jinja")
    output = template.render(types=types)
    Output(f"{generation_root}/native/cpp", "ntcore_cpp_types.cpp", output)

    # C handle API (source)
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/main/native/cpp"),
        autoescape=False,
    )
    template = env.get_template("ntcore_c_types.cpp.jinja")
    output = template.render(types=types)
    Output(f"{dirname}/src/generated/main/native/cpp", "ntcore_c_types.cpp", output)


def generate_jni_files(dirname, generation_root, types):
    # JNI
    env = Environment(
        loader=FileSystemLoader(f"{dirname}/src/generate/main/native/cpp/jni"),
        autoescape=False,
    )
    template = env.get_template("types_jni.cpp.jinja")
    output = template.render(types=types)
    Output(f"{dirname}/src/generated/main/native/cpp/jni", "types_jni.cpp", output)


if __name__ == "__main__":
    main()
