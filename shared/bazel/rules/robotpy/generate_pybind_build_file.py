import argparse
import collections
import json
import pathlib
import re
from typing import Dict, List, Tuple, Union

import jinja2
import tomli
from jinja2 import BaseLoader, Environment
from semiwrap.makeplan import (
    BuildTarget,
    BuildTargetOutput,
    CppMacroValue,
    Entrypoint,
    ExtensionModule,
    LocalDependency,
    makeplan,
)
from semiwrap.pkgconf_cache import PkgconfCache
from semiwrap.pyproject import PyProject

from shared.bazel.rules.robotpy.generation_utils import (
    load_config,
    try_tomli_lookup,
)
from shared.bazel.rules.robotpy.hack_pkgcfgs import hack_pkgconfig

CONVERSION_CONFIG = load_config()


class HeaderToDatConfig:
    def __init__(
        self,
        header_to_dat_args: BuildTarget,
        extension_name_transforms: List[Tuple[str, str]],
    ):
        includes = []
        defines = []

        idx = 0
        while True:
            if header_to_dat_args.args[idx] == "-I":
                includes.append(header_to_dat_args.args[idx + 1])
            elif header_to_dat_args.args[idx] == "-D":
                defines.append(header_to_dat_args.args[idx + 1])
            else:
                break
            idx += 2
        if header_to_dat_args.args[idx] == "--cpp":
            idx += 2

        transforms = []
        while True:
            if header_to_dat_args.args[idx] in [
                "--name-transform-attribute",
                "--name-transform-default",
                "--name-transform-enum-value",
                "--name-transform-function",
                "--name-transform-known-word",
                "--name-transform-method",
                "--name-transform-parameter",
            ]:
                transforms.append(
                    (header_to_dat_args.args[idx], header_to_dat_args.args[idx + 1])
                )
                idx += 2
            else:
                break

        # We assume that the transforms remain the same in a given extension
        if extension_name_transforms:
            assert extension_name_transforms == transforms
        else:
            extension_name_transforms.extend(transforms)

        args = header_to_dat_args.args[idx:]
        self.class_name = args[0]
        self.yml_file = args[1].path
        self.defines = defines

        include_root = str(args[3]).replace("\\", "/")
        if "native" in include_root:
            base_include_file = args[2].relative_to(include_root)
            base_library = re.search("native/(.*?)/", include_root).groups(1)[0]

            self.include_file = f"$(execpath {CONVERSION_CONFIG.get_copy_headers_target_from_base_library(base_library)})/{base_include_file}"
            self.include_root = f"$(execpath {CONVERSION_CONFIG.get_copy_headers_target_from_base_library(base_library)})"
        else:
            root_dir = pathlib.Path.cwd().absolute()
            self.include_file = pathlib.Path(args[2]).absolute().relative_to(root_dir)
            self.include_root = pathlib.Path(args[3]).absolute().relative_to(root_dir)
        # type casters         = 4
        # dat file             = 5
        # d file               = 6
        # compiler info        = 7

        self.templates = []
        self.trampolines = []

        args = args[8:]
        assert 0 == len(args)


class ResolveCastersConfig:
    def __init__(self, item: BuildTarget, pybind_prefix):
        self.pkl_file = item.args[0].name
        self.dep_file = item.args[1].name
        # semiwrap casters = 2
        self.caster_files = []
        caster_deps = set()

        for dep_path in item.args[3:]:
            if isinstance(dep_path, BuildTargetOutput):
                output_file = dep_path.target.args[2]
                caster_deps.add(
                    f":{pybind_prefix}{dep_path.target.install_path}/{output_file.name}"
                )
            else:
                relevant_parts = dep_path.parts[3:]
                caster_deps.add(
                    f"//{relevant_parts[0]}:" + "/".join(relevant_parts[1:])
                )

        self.caster_deps = sorted(caster_deps)


class GenLibInitPyConfig:
    def __init__(self, item: BuildTarget):
        self.output_file = item.args[0].name
        self.modules = item.args[1:]
        self.install_path = item.install_path


class GenPkgConfConfig:
    def __init__(self, item: BuildTarget):
        self.module_pkg_name = item.args[0]
        self.pkg_name = item.args[1]
        self.project_file = item.args[2].path
        self.output_file = item.args[3].name
        # --libinit-py = 4
        self.libinit_py = item.args[5]

        assert 0 == len(item.args[6:])

        self.install_path = item.install_path


class GenModInitHpp:
    def __init__(self, item: BuildTarget):
        self.lib_name = item.args[0]
        self.output_file = item.args[1].name
        idx = 2
        while idx < len(item.args):
            if item.args[idx].command != "header2dat":
                break
            idx += 1

        assert 0 == len(item.args[idx:])


class PublishCastersConfig:
    def __init__(self, projectcfg, item: BuildTarget, pybind_prefix):
        self.project_file = item.args[0].path
        self.casters_name = item.args[1]
        self.json_output = item.args[2].name
        self.pc_output = item.args[3].name
        assert 0 == len(item.args[4:])

        self.install_path = item.install_path

        self.include_paths = []
        caster_cfg = projectcfg.export_type_casters[self.casters_name]

        for inc_dir in caster_cfg.includedir:
            self.include_paths.append(f"{pybind_prefix}{inc_dir}")


class BazelExtensionModule:
    def __init__(
        self,
        extension_module: ExtensionModule,
        additional_extension_targets: Dict[str, BuildTarget],
        pybind_prefix,
    ):
        self.name = extension_module.name
        self.package_name = extension_module.package_name
        self.install_path = extension_module.install_path

        self.extension_name_transforms: List[Tuple[str, str]] = []
        self.generation_data = self._extract_header_generation(
            extension_module.sources, self.extension_name_transforms
        )
        self.resolve_casters = ResolveCastersConfig(
            additional_extension_targets["resolve-casters"], pybind_prefix
        )
        self.gen_libinit = GenLibInitPyConfig(
            additional_extension_targets["gen-libinit-py"]
        )
        self.gen_pkgconf = GenPkgConfConfig(additional_extension_targets["gen-pkgconf"])
        self.gen_modinit = GenModInitHpp(
            additional_extension_targets["gen-modinit-hpp"]
        )

        self.pkgcache = PkgconfCache()

        all_dependencies = set()

        for d in extension_module.depends:
            if isinstance(d, LocalDependency):
                all_dependencies.add(d.name)
            self._collect_local_dependency_names(d, all_dependencies)

        native_wrapper_dependencies = set()
        local_extension_dependencies = set()
        dynamic_dependencies = set()
        for dep_name in all_dependencies:
            if "native" in dep_name:
                transitive_deps = set()
                self._get_transitive_native_dependencies(dep_name, transitive_deps)
                for d in transitive_deps:
                    if d == "robotpy-native-mrclib":
                        continue
                    native_wrapper_dependencies.add(CONVERSION_CONFIG.get_copy_headers_target(d))
            elif "-casters" in dep_name:
                base_library = dep_name.split("-")[0]
                local_extension_dependencies.add(f"//{base_library}:{dep_name}")
            else:
                local_extension_dependencies.update(CONVERSION_CONFIG.get_local_extension_targets(dep_name, dep_name != self.name))
                dynamic_dependencies.add(CONVERSION_CONFIG.get_dynamic_dep(dep_name))

        self.native_wrapper_dependencies = sorted(native_wrapper_dependencies)
        self.local_extension_dependencies = sorted(local_extension_dependencies)
        self.dynamic_dependencies = sorted(dynamic_dependencies)

    def get_defines(self):
        defines = set()
        for h2d_def in self.generation_data.values():
            defines.update(h2d_def.defines)
        return sorted(defines)

    def _get_transitive_native_dependencies(self, dep_name, transitive_deps):
        entry = self.pkgcache.get(dep_name)
        transitive_deps.add(dep_name)
        for req in entry.requires:
            if req not in transitive_deps:
                transitive_deps.add(req)
                self._get_transitive_native_dependencies(req, transitive_deps)

    def _collect_local_dependency_names(self, dep, all_dependencies):
        for child_dep in dep.depends:
            if isinstance(child_dep, str):
                if child_dep != "semiwrap":
                    all_dependencies.add(child_dep)
            elif isinstance(child_dep, LocalDependency):
                all_dependencies.add(child_dep.name)
                self._collect_local_dependency_names(child_dep, all_dependencies)
            else:
                raise

    def _extract_header_generation(
        self, sources, extension_name_transforms: List[Tuple[str, str]]
    ) -> Dict[str, HeaderToDatConfig]:
        generation_data: Dict[str, HeaderToDatConfig] = {}

        def get_h2d_config(target_info: BuildTarget) -> HeaderToDatConfig:
            config = HeaderToDatConfig(target_info, extension_name_transforms)
            if config.class_name not in generation_data:
                generation_data[config.class_name] = config
            return generation_data[config.class_name]

        for source in sources:
            if source.command == "dat2cpp":
                h2d_config = get_h2d_config(source.args[0])
            elif source.command == "dat2trampoline":
                h2d_config = get_h2d_config(source.args[0])
                name, out_file = source.args[1:]
                h2d_config.trampolines.append((name, out_file.name))
            elif source.command == "dat2tmplcpp":
                h2d_config = get_h2d_config(source.args[0])
                name, out_file = source.args[1:]
                h2d_config.templates.append((out_file.name[:-4], name))
            elif source.command == "dat2tmplhpp":
                # Handled by dat2tmplcpp
                continue
            elif source.command == "gen-modinit-hpp":
                # Handled elsewhere
                continue
            else:
                raise Exception("Unknown command", source.command)

        return generation_data


def generate_pybind_build_file(
    pkgcfgs: List[pathlib.Path],
    project_file: pathlib.Path,
    package_root_file: str,
    stripped_include_prefix: str,
    yml_prefix: Union[str, None],
    output_file: pathlib.Path,
    package_name: str,
):
    include_root_prefix = f"{stripped_include_prefix}/" if stripped_include_prefix else ""

    project_dir = project_file.parent
    plan = makeplan(project_dir)

    hack_pkgconfig(pkgcfgs)

    extension_modules = []
    entry_points = collections.defaultdict(list)

    pyproject = PyProject(project_file)
    projectcfg = pyproject.project

    # Cache built up for an extension module. Gets reset when an ExtensionModule is encountered
    additional_extension_targets: Dict[str, BuildTarget] = {}
    publish_casters_targets = []

    for item in plan:
        if isinstance(item, ExtensionModule):
            extension_modules.append(
                BazelExtensionModule(item, additional_extension_targets, pybind_prefix=include_root_prefix)
            )
            additional_extension_targets = {}
        elif isinstance(item, BuildTarget):
            if item.command in [
                "resolve-casters",
                "gen-libinit-py",
                "gen-pkgconf",
                "gen-modinit-hpp",
            ]:
                if item.command in additional_extension_targets:
                    raise Exception(f"Repeated target {item.command}")
                additional_extension_targets[item.command] = item
            elif item.command in [
                "header2dat",
                "dat2cpp",
                "dat2tmplcpp",
                "dat2tmplhpp",
                "dat2trampoline",
                "make-pyi",
            ]:
                pass
            elif item.command == "publish-casters":
                publish_casters_targets.append(PublishCastersConfig(projectcfg, item, pybind_prefix=include_root_prefix))
            else:
                raise Exception(f"Unhandled build target {item.command}")
        elif isinstance(item, Entrypoint):
            entry_points[item.group].append(f"{item.name} = {item.package}")
        elif isinstance(item, LocalDependency):
            pass
        elif isinstance(item, CppMacroValue):
            pass
        else:
            raise Exception(f"Unknown item {type(item)}")

    with open(project_file, "rb") as fp:
        raw_config = tomli.load(fp)

    top_level_name = try_tomli_lookup(raw_config, "tool.hatch.build.targets.wheel.packages", default_value = [raw_config["project"]["name"]])
    assert len(top_level_name) == 1
    top_level_name = top_level_name[0]

    template_file = "shared/bazel/rules/robotpy/pybind_build_file_template.jinja2"
    with open(template_file, "r") as f:
        template_contents = f.read()

    def jsonify(item):
        if isinstance(item, jinja2.runtime.Undefined):
            return "None"
        return json.dumps(item)

    EXTERNAL_PYPI_DEPS = [
        "robotpy-cli",
        "pytest-reraise",
        "pytest",
        "typing_extensions",
    ]

    python_deps = []
    has_external_python_deps = False
    if "dependencies" in raw_config["project"]:
        for d in raw_config["project"]["dependencies"]:
            # Strip version strings out
            dep_no_version = re.compile(r"^[A-Za-z0-9_.\-]+").match(d).group(0)

            for external_dep in EXTERNAL_PYPI_DEPS:
                if external_dep == dep_no_version:
                    has_external_python_deps = True
                    python_deps.append(f'requirement("{dep_no_version}")')
                    break
            else:
                pd = CONVERSION_CONFIG.target_from_python_dep(dep_no_version)
                python_deps.append(pd)

    env = Environment(loader=BaseLoader)
    env.filters["jsonify"] = jsonify
    template = env.from_string(template_contents)

    all_local_native_deps = set()
    for em in extension_modules:
        all_local_native_deps.update(em.native_wrapper_dependencies)
    all_local_native_deps = sorted(all_local_native_deps)

    version_file = try_tomli_lookup(raw_config, "tool.hatch.build.hooks.robotpy.version_file")

    # The entry points defined above are implicit to how the project is broken down in the toml files.
    # This adds potentially extra explicitly declared entry points
    if "entry-points" in raw_config["project"]:
        explicit_entry_points = raw_config["project"]["entry-points"]
        for entry_point_type in explicit_entry_points:
            for ep_key, ep_value in explicit_entry_points[entry_point_type].items():
                entry_points[entry_point_type].append(f"{ep_key} = {ep_value}")

    imports_dir = stripped_include_prefix if stripped_include_prefix else "."
    strip_path_prefixes = [
        f"{project_dir}",
        f"{package_name}",
    ]

    is_semiwrap_project = try_tomli_lookup(raw_config, "tool.semiwrap") is not None
    maven_downloads = try_tomli_lookup(raw_config, "tool.hatch.build.hooks.robotpy.maven_lib_download", [])

    maven_libs = []
    for maven_info in maven_downloads:
        for lib in maven_info["libs"]:
            lib_package = CONVERSION_CONFIG.fixup_root_package_name(lib)
            library_label = f"//{lib_package}:shared/{lib}"
            maven_libs.append(
                {
                    "name": lib,
                    "base_path": f"{include_root_prefix}{maven_info['extract_to']}/",
                    "library": library_label,
                }
            )

    with open(output_file, "w") as f:
        f.write(
            template.render(
                extension_modules=extension_modules,
                top_level_name=top_level_name,
                publish_casters_targets=publish_casters_targets,
                python_deps=sorted(python_deps),
                all_local_native_deps=all_local_native_deps,
                stripped_include_prefix=stripped_include_prefix,
                include_root_prefix=include_root_prefix,
                imports_dir=imports_dir,
                strip_path_prefixes=strip_path_prefixes,
                yml_prefix=yml_prefix,
                package_root_file=package_root_file,
                raw_project_config=raw_config["project"],
                entry_points=entry_points,
                version_file=version_file,
                has_external_python_deps=has_external_python_deps,
                is_semiwrap_project=is_semiwrap_project,
                maven_libs=maven_libs,
            )
            + "\n"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_file", type=pathlib.Path, required=True)
    parser.add_argument("--output_file", type=pathlib.Path, required=True)
    parser.add_argument(
        "--stripped_include_prefix", type=str, default="src/main/python"
    )
    parser.add_argument("--yml_prefix", type=str)
    parser.add_argument("--package_root_file", type=str)
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")
    parser.add_argument("--package_name", type=str, required=True)

    args = parser.parse_args()

    generate_pybind_build_file(
        args.pkgcfgs,
        args.project_file,
        args.package_root_file,
        args.stripped_include_prefix,
        args.yml_prefix,
        args.output_file,
        args.package_name,
    )


if __name__ == "__main__":
    main()
