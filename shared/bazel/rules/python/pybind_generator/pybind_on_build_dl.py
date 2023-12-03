import argparse
from shared.bazel.rules.python.pybind_generator.pybind_gen_utils import Setup
from robotpy_build.wrapper import Wrapper
import os


def main():
    print("BUILD DL")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output_directory", required=True)
    args = parser.parse_args()

    setup = Setup(args.config, args.output_directory)
    print(setup)
    print(setup.wrappers)
    for wrapper in setup.wrappers:
        print("WRAPPER", wrapper)
        wrapper.on_build_dl("", "")
        

if __name__ == "__main__":
    main()
