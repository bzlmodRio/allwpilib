import os
import sys
import argparse

from wpilibc.generate_hids import main as generate_hids
from wpilibc.generate_pwm_motor_controllers import generate_pwm_motor_controllers


def main():
    dirname, _ = os.path.split(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_directory",
        help="Optional. If set, will output the generated files to this directory, otherwise it will use a path relative to the script",
        default=os.path.join(dirname, "src/generated"),
    )
    parser.add_argument(
        "--schema_root",
        help="Optional. If set, will use this directory as the root for discovering the pwm controller schema",
        default=os.path.join(dirname, "../wpilibj/src/generate"),
    )
    parser.add_argument(
        "--template_root",
        help="Optional. If set, will use this directory as the root for the jinja templates",
        default=os.path.join(dirname, "src/generate"),
    )
    args = parser.parse_args()

    sys.argv = ["x", f"--output_directory={args.output_directory}", "--always_write"]
    generate_hids()
    generate_pwm_motor_controllers(
        args.output_directory, args.template_root, args.schema_root
    )


if __name__ == "__main__":
    main()
