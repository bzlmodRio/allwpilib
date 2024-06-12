#!/usr/bin/env python3

# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
import json
import os
import argparse

from jinja2 import Environment, FileSystemLoader


def write_controller_file(outPath, controllerName, contents, always_write):
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    outpathname = f"{outPath}/{controllerName}"

    if not always_write:
        if os.path.exists(outpathname):
            with open(outpathname, "r") as f:
                if f.read() == contents:
                    return

    # File either doesn't exist or has different contents
    with open(outpathname, "w", newline="\n") as f:
        f.write(contents)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_directory",
        help="Optional. If set, will output the generated files to this directory, otherwise it will use a path relative to the script",
    )
    parser.add_argument(
        "--always_write",
        action="store_true",
        help="If set, will always genenerate the files. Not recommended for use with gradle as it will cause cache misses",
    )
    args = parser.parse_args()

    if args.output_directory:
        generation_root = args.output_directory
        schema_root = "wpilibj/src/generate"
        template_root = "wpilibNewCommands/src/generate"
    else:
        dirname, _ = os.path.split(os.path.abspath(__file__))
        generation_root = os.path.join(dirname, "src/generated")
        schema_root = os.path.join(dirname, "../wpilibj/src/generate")
        template_root = os.path.join(dirname, "src/generate")

    with open(f"{schema_root}/hids.json") as f:
        controllers = json.load(f)

    # Java files
    env = Environment(
        loader=FileSystemLoader(
            f"{template_root}/main/java/edu/wpi/first/wpilibj2/command/button"
        ),
        autoescape=False,
        keep_trailing_newline=True,
    )
    rootPath = f"{generation_root}/main/java/edu/wpi/first/wpilibj2/command/button"
    template = env.get_template("commandhid.java.jinja")
    for controller in controllers:
        controllerName = os.path.basename(
            f"Command{controller['ConsoleName']}Controller.java"
        )
        output = template.render(controller)
        write_controller_file(rootPath, controllerName, output, args.always_write)

    # C++ headers
    env = Environment(
        loader=FileSystemLoader(
            f"{template_root}/main/native/include/frc2/command/button"
        ),
        autoescape=False,
        keep_trailing_newline=True,
    )
    rootPath = f"{generation_root}/main/native/include/frc2/command/button"
    template = env.get_template("commandhid.h.jinja")
    for controller in controllers:
        controllerName = os.path.basename(
            f"Command{controller['ConsoleName']}Controller.h"
        )
        output = template.render(controller)
        write_controller_file(rootPath, controllerName, output, args.always_write)

    # C++ files
    env = Environment(
        loader=FileSystemLoader(f"{template_root}/main/native/cpp/frc2/command/button"),
        autoescape=False,
    )
    rootPath = f"{generation_root}/main/native/cpp/frc2/command/button"
    template = env.get_template("commandhid.cpp.jinja")
    for controller in controllers:
        controllerName = os.path.basename(
            f"Command{controller['ConsoleName']}Controller.cpp"
        )
        output = template.render(controller)
        write_controller_file(rootPath, controllerName, output, args.always_write)


if __name__ == "__main__":
    main()
