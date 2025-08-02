import argparse
import importlib
import os
import pathlib
import sys
from typing import List


def hack_pkgconfig(pkgcfgs: List[pathlib.Path]):
    """
    This will place the given files in the PKG_CONFIG_PATH in such a way that will trick
    semiwrap into thinking the libraries have been installed
    """

    pkg_config_paths = os.environ.get("PKG_CONFIG_PATH", "").split(os.pathsep)

    if pkgcfgs:
        for pc in pkgcfgs:
            assert pc.exists()
            pkg_config_paths.append(str(pc.parent.absolute()))

    os.environ["PKG_CONFIG_PATH"] = os.pathsep.join(pkg_config_paths)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", type=pathlib.Path)
    parser.add_argument("--to_update")
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")
    args = parser.parse_args()

    hack_pkgconfig(args.pkgcfgs)

    module = importlib.import_module("semiwrap.tool")
    tool_main = getattr(module, "main")

    if " " in args.to_update:
        base, compiled = args.to_update.split(" ", 1)
    else:
        base = args.to_update
        compiled = None

    sys.argv = [""] + [
        "create-imports",
        "--write",
        base,
        compiled,
        f"--override_output_file={args.output_file}",
    ]

    try:
        tool_main()
    except SystemExit as e:
        if e.code != 0:
            raise


if __name__ == "__main__":
    main()
