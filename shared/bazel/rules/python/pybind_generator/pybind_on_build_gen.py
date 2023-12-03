import argparse

from shared.bazel.rules.python.pybind_generator.load_project_config import load_project_config
from shared.bazel.rules.python.pybind_generator.pybind_gen_utils import Setup
from robotpy_build.wrapper import Wrapper
import os
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output_directory", required=True)
    parser.add_argument("--project_name", required=True)
    args = parser.parse_args()

    intermediate_directory = args.output_directory + ".intermediate"

    setup = Setup(args.config, intermediate_directory)

    for wrapper in setup.wrappers:
        wrapper.on_build_gen(os.path.join(intermediate_directory, "pybind_gen"))

    print("Done gen")

    shutil.copytree(
        os.path.join(intermediate_directory, "pybind_gen"),
        os.path.join(args.output_directory, "gensrc"),
    )

    project_name = args.project_name

    shutil.copytree(
        os.path.join(intermediate_directory, f"{project_name}/rpy-include"),
        os.path.join(args.output_directory, f"rpy-include/{project_name}"),
    )

    # for root, _, files in os.walk(os.path.join(args.output_directory, "gensrc")):
    #     for f in files:
    #         if f.endswith(".json"):
    #             os.remove(os.path.join(root, f))


        

if __name__ == "__main__":
    main()
