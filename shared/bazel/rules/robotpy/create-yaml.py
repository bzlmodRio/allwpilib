import importlib
import os
import sys
import pathlib
import argparse
import shutil
import dictdiffer 
import dictdiffer.utils
from typing import List
from ruamel.yaml import YAML


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
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")
    args = parser.parse_args()

    hack_pkgconfig(args.pkgcfgs)

    module = importlib.import_module("semiwrap.tool")
    tool_main = getattr(module, "main")

    sys.argv = [""] + ["update-yaml", "--write", "-v", f"--project_file={args.pyproject}", f"--output_directory={args.output_dir}"]
    
    try:
        tool_main()
    except SystemExit as e:
        if e.code != 0:
            raise
        pass


if __name__ == "__main__":
    main()
