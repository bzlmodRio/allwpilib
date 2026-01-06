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
        raise


if __name__ == "__main__":
    main()
