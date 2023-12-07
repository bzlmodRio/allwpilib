load("@rules_robotpy_utils//rules_robotpy_utils:generate_robopy_files.bzl", _generate_robopy_files = "generate_robopy_files")

def generate_robopy_files(name, **kwargs):
    _generate_robopy_files(name, disable = False, **kwargs)
