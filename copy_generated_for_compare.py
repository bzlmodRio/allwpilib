
import shutil
import os

test_directory = "/home/pjreiniger/git/temp/robotpy_gen_test"

for project in [
    "apriltag",
    "datalog",
    "hal",
    "ntcore",
    "wpilibc",
    "wpimath",
    "wpinet",
    "wpiutil",
    ]:

    python_dir = test_directory + f"/{project}/src/main/python"
    gen_dir = test_directory + f"/{project}/generated"

    if os.path.exists(python_dir):
        shutil.rmtree(python_dir)
    if os.path.exists(gen_dir):
        shutil.rmtree(gen_dir)

    shutil.copytree(f"bazel-bin/{project}/src/main/python", python_dir, symlinks=True)
    shutil.copytree(f"bazel-bin/{project}/generated", gen_dir, symlinks=True)
