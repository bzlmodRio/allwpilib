import argparse
from shared.bazel.rules.python.pybind_generator.pybind_gen_utils import Setup
from robotpy_build.wrapper import Wrapper
import os
import importlib
from robotpy_build.pkgcfg_provider import PkgCfgProvider, PkgCfg


def main():
    print("BUILD DL")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output_files", nargs="+", required=True)
    args = parser.parse_args()

    print(args.output_files)
    # for f in args.output_files:
    #     with open(f, 'w') as of:
    #         of.write(f"HELLO {f}")

    output_directory = os.path.dirname(args.output_files[0]) +  "/.."
    print(args.output_files[0])
    print(output_directory)

    setup = Setup(args.config, output_directory)

    
    # for dependency in dependencies:

    print(setup)
    print(setup.wrappers)
    for wrapper in setup.wrappers:
        print("WRAPPER", wrapper)
        wrapper.on_build_dl("", "")

    print(os.listdir(output_directory))
    print("___")
        

if __name__ == "__main__":
    main()
