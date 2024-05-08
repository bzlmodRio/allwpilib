load("@rules_robotpy_utils//rules_robotpy_utils:generate_robotpy_project_files.bzl", _generate_robotpy_project_files = "generate_robotpy_project_files")
load("//shared/bazel/rules/python/pybind_generator:disable_flags.bzl", "DISABLE_PROJECT_GEN_TEST")

def generate_robotpy_project_files(name, **kwargs):
    _generate_robotpy_project_files(name, disable_gen_test = DISABLE_PROJECT_GEN_TEST, **kwargs)
