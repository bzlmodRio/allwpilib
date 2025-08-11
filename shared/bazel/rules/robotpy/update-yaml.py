import argparse
import importlib
import os
import pathlib
import sys
from typing import List
import shutil
from shared.bazel.rules.robotpy.hack_pkgcfgs import hack_pkgconfig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=pathlib.Path)
    parser.add_argument("--pyproject", type=pathlib.Path)
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")
    args = parser.parse_args()

    args.pyproject = args.pyproject.absolute()
    args.output_dir = args.output_dir.absolute()
    args.pkgcfgs = [x.absolute() for x in args.pkgcfgs]
    os.chdir(args.pyproject.parent)

    hack_pkgconfig(args.pkgcfgs)

    module = importlib.import_module("semiwrap.tool")
    tool_main = getattr(module, "main")

    sys.argv = [""] + [
        "update-yaml",
        "--write",
        "-v",
        f"--project_file={args.pyproject}",
        f"--output_directory={args.output_dir}", # Do the .. to get rid of the extra semiwrap directory that gets generated.
    ]

    try:
        tool_main()
    except SystemExit as e:
        # print("Catching a exit...", e.code)
        if e.code != 0:
            raise

if __name__ == "__main__":
    main()
