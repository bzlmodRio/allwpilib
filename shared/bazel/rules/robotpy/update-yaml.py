import argparse
import importlib
import os
import pathlib
import sys
from typing import List
import shutil


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

    args.pyproject = args.pyproject.absolute()
    args.output_dir = args.output_dir.absolute()
    os.chdir(args.pyproject.parent)

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

    # print("Original")
    # for root, _, files in os.walk(args.pyproject.parent / "semiwrap"):
    #     print(root, files)
    if (args.output_dir / "semiwrap2").exists():
        os.unlink(args.output_dir / "semiwrap2")

    import tempfile
    # with tempfile.TemporaryDirectory() as gendir:
    #     shutil.move(args.output_dir / "semiwrap/semiwrap", pathlib.Path(gendir))
    #     shutil.move(pathlib.Path(gendir) / "semiwrap", args.output_dir)

if __name__ == "__main__":
    main()
