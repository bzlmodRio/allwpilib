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
        diffs = dictdiffer.diff(original, generated)

        additions = []

        for diff in diffs:
            # print(diff)
            action = diff[0]
            if action == "change":
                # print(diff)
                # changes = [1]
                print("CHANGES: ", diff) 
                print(diff[0])
                print(diff[1])
                print(diff[2])
                print(len(diff[2]))
                print("------------------------")
                assert 2 == len(diff[2])
                if diff[2][1] == None:
                    continue
                else:
                    print("!!!!!!!!!!!!!!!")
            elif action == "add":
                additions.append(diff)
            elif action == "remove":
                removals = diff[2]
                # print("REMOVALS: ")
                
                for removal in removals:
                    # print("  ", removal)
                    modified_diff = [(diff[0], diff[1], [removal])]
                    # print(modified_diff)
                    if removal[0] not in ["defaults", "extra_includes", "nodelete", "template_params", "force_no_trampoline", "ignore", "templates", "typealias", "inline_code", "base_qualnames", "force_type_casters", "force_no_default_constructor", "subpackage", "is_polymorphic", "template_inline_code", "ignored_bases", "doc", "rename", "constants", "strip_prefixes"]:
                        original = dictdiffer.patch(modified_diff, original)
                    # else:
                    #     print("  --Ignoring removal")

            else:
                print(action)
        # print(list(result))

        if not original.get("defaults", {}).get("ignore", False):
            print(additions)
            print("Got additions")
            original = dictdiffer.patch(additions, original)
        
        output_file = output_directory / f
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(original, f)
        
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
