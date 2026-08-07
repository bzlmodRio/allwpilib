import dataclasses
import typing
import pathlib
import tomli
import functools
import validobj.validation

@dataclasses.dataclass
class SubprojectConfig:
    bazel_project_root: typing.Optional[str] = None
    # is_native: typing.Optional[bool] = None
    # project_base_name: typing.Optional[str] = ""
    # copy_headers_target: typing.Optional[str] = None
    # copy_headers_target_from_target: typing.Optional[str] = None
    # local_extension_targets: typing.Optional[list[str]] = None
    # pybind_target: typing.Optional[str] = None
    # dynamic_dep: typing.Optional[str] = None

    # def populate_defaults(self, project_name):
    #     if self.is_native is None:
    #         self.is_native = "native" in project_name

    #     base_name = project_name.replace("robotpy-native-", "")
    #     if self.is_native and self.copy_headers_target is None:
    #         self.copy_headers_target = f"//{base_name}:{project_name}.copy_headers"
            
    #     if self.local_extension_targets is None:
    #         self.local_extension_targets = [f"//{base_name}:{base_name}"]
            
    #     if self.pybind_target is None:
    #         self.pybind_target = pybind_target = f"//{base_name}:{base_name}_pybind_library"

    #     if self.dynamic_dep is None:
    #         self.dynamic_dep = f"//{project_name}:shared/{project_name}"

    #     if self.copy_headers_target_from_target is None:
    #         self.copy_headers_target_from_target = f":robotpy-native-{project_name}.copy_headers"


@dataclasses.dataclass
class BazelTranslationConfig:
    projects: typing.Dict[str, SubprojectConfig]

    # def __post_init__(self):
    #     for key in self.projects:
    #         self.projects[key].populate_defaults(key)

    # def get_copy_headers_target(self, project_name):
    #     return self.projects[project_name].copy_headers_target

    # def get_copy_headers_target_from_base_library(self, project_name):
    #     return self.projects[project_name].copy_headers_target_from_target

    # def get_local_extension_targets(self, project_name: str, include_pybind_target: bool):
    #     output = self.projects[project_name].local_extension_targets
    #     if include_pybind_target:
    #         output.append(self.projects[project_name].pybind_target)

    #     return output

    # def get_dynamic_dep(self, project_name) -> typing.Optional[str]:
    #     return self.projects[project_name].dynamic_dep



_CONFIG_PATH = pathlib.Path(__file__).parent / "project_config.toml"

@functools.lru_cache
def load_config():
    with open(_CONFIG_PATH, "rb") as fp:
        toml_data = tomli.load(fp)

    config = validobj.validation.parse_input(toml_data, BazelTranslationConfig)
    return config


def fixup_root_package_name(name):
    config = load_config()

    if name in config.projects:
        if config.projects[name].bazel_project_root:
            return config.projects[name].bazel_project_root

    print(f"Using default for {name}")
    return name


def fixup_native_lib_name(name):
    return name


def fixup_native_package_name(name):
    return f"{fixup_root_package_name(name)}"


def fixup_python_package_name(name):
    return f"{fixup_root_package_name(name)}"


def fixup_shared_lib_name(name):
    if name == "wpihal":
        return "wpiHal"
    if name == "hal":
        return "wpiHal"
    if name == "wpilib":
        return "wpilibc"
    if name == "xrp":
        return "xrpVendordep"
    if name == "romi":
        return "romiVendordep"
    return name


def fixup_python_dep_name(name):
    if name == "robotpy-datalog":
        return "robotpy-wpilog"
    if name == "robotpy-ntcore":
        return "pyntcore"
    if name == "wpilib":
        return "robotpy-wpilib"
    return name


def try_tomli_lookup(tomli_map, str_key, default_value=None):
    keys = str_key.split(".")
    submap = tomli_map

    try:
        for key in keys:
            submap = submap[key]
    except KeyError:
        return default_value

    return submap