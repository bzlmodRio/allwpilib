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


def merge_data(generated_directory, backup_directory, output_directory):
    generated_files = set()
    for root, _, files in os.walk(generated_directory):
        for f in files:
            generated_files.add((pathlib.Path(root) / f).relative_to(generated_directory))
            
    backup_files = set()
    for root, _, files in os.walk(backup_directory):
        for f in files:
            backup_files.add((pathlib.Path(root) / f).relative_to(backup_directory))

    

    print(generated_files)
    print(backup_files)
    print(backup_files.difference(generated_files))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=pathlib.Path)
    parser.add_argument("--backup_dir", type=pathlib.Path)
    parser.add_argument("--pyproject", type=pathlib.Path)
    parser.add_argument("--directory", type=pathlib.Path)
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")
    args = parser.parse_args()

    args.output_dir = args.output_dir.absolute()
    if args.output_dir.exists:
        shutil.rmtree(args.output_dir)

    backup_dir = args.backup_dir.absolute()
    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    hack_pkgconfig(args.pkgcfgs)

    os.chdir(args.directory)
    for root, _, files in os.walk("."):
        print(root, files)
    shutil.move("semiwrap", backup_dir)

    module = importlib.import_module("semiwrap.tool")
    tool_main = getattr(module, "main")


    sys.argv = [""] + ["create-yaml", "--write", "-v"]
    
    try:
        tool_main()
    except SystemExit as e:
        if e.code != 0:
            raise
        pass

    print('after')

    merge_data(pathlib.Path("semiwrap"), backup_dir, args.output_dir)
    # shutil.copytree("semiwrap", args.output_dir)


if __name__ == "__main__":
    main()
