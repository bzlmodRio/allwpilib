import importlib
import os
import sys
import pathlib
import argparse
import shutil
import yaml
import dictdiffer 
import dictdiffer.utils
from typing import List
from ruyaml import YAML
import ruyaml


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
    common_files = backup_files.intersection(generated_files)
    for f in common_files:
        # generated = YAML(typ='safe').load(generated_directory / f)
        # original = YAML(typ='safe').load(backup_directory / f)
        with open(generated_directory / f, 'r') as xxx:
            generated = ruyaml.load(xxx, ruyaml.RoundTripLoader)
        with open(backup_directory / f, 'r') as xxx:
            original = ruyaml.load(xxx, ruyaml.RoundTripLoader)
        print("\n\n")
        print(f)
        # print(generated)
        # print(original)
        diffs = dictdiffer.diff(generated, original)
        for diff in diffs:
            action = diff[0]
            if action == "change":
                changes = diff[2][1]
                print("CHANGES: ", changes) 
                # if 'no_release_gil' in diff[2][0]:
                generated = dictdiffer.patch([diff], generated)
                # print(diff[2])
            elif action == "add":
                additions = diff[2]
                print("ADDITIONS: ", additions)
                
                for addition in additions:
                    print("  ", addition)
                    modified_diff = [(diff[0], diff[1], [addition])]
                    if addition[0] == "defaults":
                        temp = dictdiffer.patch(modified_diff, generated)
                        generated = dict(defaults=temp["defaults"], **generated)
                    elif addition[0] == "extra_includes":
                        temp = dictdiffer.patch(modified_diff, generated)
                        old = dict(generated)
                        defaults = old.pop("defaults", {})
                        generated = dict(defaults=defaults, extra_includes=temp["extra_includes"], **old)
                        if defaults == {}:
                            del generated["defaults"]
                    elif addition[0] in ["nodelete"]:
                        generated = dictdiffer.patch(modified_diff, generated)
                        # print(addition)
                        # temp = dictdiffer.patch(modified_diff, generated)
                        # print(modified_diff)
                        # print(dictdiffer.utils.dot_lookup(temp, modified_diff[0][1]))
                        # generated = dict(defaults=temp["nodelete"], **generated)
                    else:
                        print("  -- Ignored")
            else:
                print(action)
        # print(list(result))
        
        output_file = output_directory / f
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(generated, f)
        
    # for f in backup_files.intersection(generated_files):
    #     output_file = output_directory / f
    #     output_file.parent.mkdir(parents=True, exist_ok=True)
    #     shutil.copy(generated_directory / f, output_file)
# backup_directory
    # for f in backup_files.difference(generated_files):
        

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
