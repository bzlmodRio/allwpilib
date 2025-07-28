import importlib
import os
import sys
import pathlib
import argparse
import shutil
from typing import List


def hack_pkgconfig(pkgcfgs: List[pathlib.Path]):
    """
    This will place the given files in the PKG_CONFIG_PATH in such a way that will trick
    semiwrap into thinking the libraries have been installed
    """

    pkg_config_paths = os.environ.get("PKG_CONFIG_PATH", "").split(os.pathsep)

    if pkgcfgs:
        for pc in pkgcfgs:
            pkg_config_paths.append(str(pc.parent.absolute()))

    os.environ["PKG_CONFIG_PATH"] = os.pathsep.join(pkg_config_paths)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=pathlib.Path)
    parser.add_argument("--pyproject", type=pathlib.Path)
    parser.add_argument("--directory", required=True, type=pathlib.Path)
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")
    args = parser.parse_args()

    # args.output_dir = args.output_dir.absolute()
    # if args.output_dir.exists:
    #     shutil.rmtree(args.output_dir)

    hack_pkgconfig(args.pkgcfgs)

    os.chdir(args.directory)

    module = importlib.import_module("semiwrap.tool")
    tool_main = getattr(module, "main")


    sys.argv = [""] + ["scan-headers", "--check"]

    for root, _, files in os.walk("."):
        print(root, files)
        
    
    try:
        tool_main()
    except SystemExit as e:
        if e != 0:
            print("scan-headers has detected an unaccounted for change. See text above and add it to the projects pyproject.toml file")
            raise


if __name__ == "__main__":
    main()
