load("@rules_robotpy_utils//rules_robotpy_utils:generate_robotpy_project_files.bzl", _generate_robotpy_project_files = "generate_robotpy_project_files")

def generate_robotpy_project_files(name, **kwargs):
    _generate_robotpy_project_files(name, disable_gen_test = True, **kwargs)
