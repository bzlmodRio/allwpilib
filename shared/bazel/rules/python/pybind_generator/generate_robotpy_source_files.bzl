load("@rules_robotpy_utils//rules_robotpy_utils:generate_robotpy_source_files.bzl", _generate_robotpy_source_files = "generate_robotpy_source_files")

def generate_robotpy_source_files(name, **kwargs):
    _generate_robotpy_source_files(name, disable = False, **kwargs)
