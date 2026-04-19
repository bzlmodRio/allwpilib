import argparse
import pathlib
import importlib
import sys
import os
import shutil


def main():
    module = importlib.import_module("semiwrap.cmd.make_pyi")
    tool_main = getattr(module, "main")

    semiwrap_args = sys.argv[1:]

    sys.argv = [""] + [str(x) for x in semiwrap_args]

    try:
        tool_main()
    except:
        print("-------------------------------------")
        print("Failed to run wrapped tool.")
        print(f"Args:")
        for a in semiwrap_args:
            print("  ", a)
        print("-------------------------------------")
        print("You likely have native references leaking into the python docstring. Usually this can be fixed in one of two ways:")
        print("1. Adding an 'extra_include: []' section to classes yaml file")
        print("2. Ignoring the problematic field if it is exporting a type that does not have a pybind wrapper.")
        raise


if __name__ == "__main__":
    main()
