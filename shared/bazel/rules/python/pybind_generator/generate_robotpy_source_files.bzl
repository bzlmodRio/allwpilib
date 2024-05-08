load("@rules_robotpy_utils//rules_robotpy_utils:generate_robotpy_source_files.bzl", _generate_robotpy_source_files = "generate_robotpy_source_files")
load("//shared/bazel/rules/python/pybind_generator:disable_flags.bzl", "DISABLE_SOURCE_GEN")

def generate_robotpy_source_files(name, **kwargs):
    _generate_robotpy_source_files(name, disable = DISABLE_SOURCE_GEN, **kwargs)
