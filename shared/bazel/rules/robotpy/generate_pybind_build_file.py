import argparse
import collections
import pathlib
import re

import tomli
from jinja2 import BaseLoader, Environment
from packaging.markers import Marker
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
    fixup_native_lib_name,
    fixup_python_dep_name,
    fixup_root_package_name,
    fixup_shared_lib_name,
    jsonify,
    maven_dep_to_library,
    try_tomli_lookup,
)
from shared.bazel.rules.robotpy.hack_pkgcfgs import hack_pkgconfig
from shared.bazel.rules.robotpy.hatchlib_native_port.config import PcFileConfig
from shared.bazel.rules.robotpy.hatchlib_native_port.validate import parse_input


class HeaderToDatConfig:
    def __init__(
        self,
        header_to_dat_args: BuildTarget,
        extension_name_transforms: list[tuple[str, str]],
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
        self.yml_file = pathlib.Path(args[1].path).as_posix()
        self.defines = defines

        include_root = str(args[3]).replace("\\", "/")
        if "native" in include_root:
            # base_include_root = pathlib.Path(*args[3].relative_to(root_dir).parts[3:])
            base_include_file = args[2].relative_to(include_root).as_posix()
            base_library = re.search("native/(.*?)/", include_root).groups(1)[0]

            native_library = fixup_native_lib_name("robotpy-native-" + base_library)
            self.include_file = f"$(execpath //{fixup_root_package_name(base_library)}:{native_library}.copy_headers)/{base_include_file}"
            self.include_root = f"$(execpath //{fixup_root_package_name(base_library)}:{native_library}.copy_headers)"
        else:
            root_dir = pathlib.Path.cwd().absolute()
            self.include_file = (
                pathlib.Path(args[2]).absolute().relative_to(root_dir).as_posix()
            )
            self.include_root = (
                pathlib.Path(args[3]).absolute().relative_to(root_dir).as_posix()
            )
        # type casters         = 4
        # dat file             = 5
        # d file               = 6
        # compiler info        = 7

        self.templates = []
        self.trampolines = []

        args = args[8:]
        assert 0 == len(args)


class ResolveCastersConfig:
    def __init__(self, item: BuildTarget, stripped_include_prefix: str):
        self.pkl_file = item.args[0].name
        self.dep_file = item.args[1].name
        # semiwrap casters = 2
        self.caster_files = []
        caster_deps = set()

        for dep_path in item.args[3:]:
            if isinstance(dep_path, BuildTargetOutput):
                output_file = dep_path.target.args[2]
                caster_deps.add(
                    f":{stripped_include_prefix}{dep_path.target.install_path}/{output_file.name}"
                )
            else:
                relevant_parts = dep_path.parts[3:]
                package = relevant_parts[0]
                caster_deps.add(
                    f"//{package}/src/main/python:" + "/".join(relevant_parts[4:])
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
    def __init__(self, projectcfg, item: BuildTarget, stripped_include_prefix: str):
        self.project_file = item.args[0].path
        self.casters_name = item.args[1]
        self.json_output = item.args[2].name
        self.pc_output = item.args[3].name
        assert 0 == len(item.args[4:])

        self.install_path = item.install_path

        self.include_paths = []
        caster_cfg = projectcfg.export_type_casters[self.casters_name]

        for inc_dir in caster_cfg.includedir:
            self.include_paths.append(f"{stripped_include_prefix}{inc_dir}")


class BazelExtensionModule:
    def __init__(
        self,
        extension_module: ExtensionModule,
        additional_extension_targets: dict[str, BuildTarget],
        stripped_include_prefix: str,
    ):
        self.name = extension_module.name
        self.package_name = extension_module.package_name
        self.install_path = extension_module.install_path

        self.extension_name_transforms: list[tuple[str, str]] = []
        self.generation_data = self._extract_header_generation(
            extension_module.sources, self.extension_name_transforms
        )
        self.resolve_casters = ResolveCastersConfig(
            additional_extension_targets["resolve-casters"], stripped_include_prefix
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
                    base_library = fixup_root_package_name(
                        d.replace("robotpy-native-", "").replace("-", "_")
                    )
                    native_wrapper_dependencies.add(
                        f"//{base_library}:{fixup_native_lib_name(d)}.copy_headers"
                    )
            elif "-casters" in dep_name:
                base_library = dep_name.split("-")[0]
                local_extension_dependencies.add(
                    f"//{base_library}/src/main/python:{dep_name}"
                )
            else:
                base_library = fixup_root_package_name(dep_name.rsplit("_", 1)[0])
                shared_lib_name = fixup_shared_lib_name(base_library.rsplit("/", 1)[-1])
                local_extension_dependencies.add(f"//{base_library}:{shared_lib_name}")
                dynamic_dependencies.add(f"//{base_library}:shared/{shared_lib_name}")
                if dep_name != self.name:
                    local_extension_dependencies.add(
                        f"//{base_library}/src/main/python:{dep_name}_pybind_library"
                    )

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
                raise  # noqa: PLE0704

    def _extract_header_generation(
        self, sources, extension_name_transforms: list[tuple[str, str]]
    ) -> dict[str, HeaderToDatConfig]:
        generation_data: dict[str, HeaderToDatConfig] = {}

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
                raise RuntimeError("Unknown command", source.command)

        return generation_data


def get_pc_dep(library):
    base_project = library.replace("robotpy-native-", "").replace("-", "_")
    wpilib_project = fixup_root_package_name(base_project)
    native_library = fixup_native_lib_name(library)
    return f"//{wpilib_project}:native/{base_project}/{native_library}.pc"


def get_python_dep(library):
    base_project = library.replace("robotpy-native-", "").replace("-", "_")
    wpilib_project = fixup_root_package_name(base_project)
    return (
        f"//{fixup_root_package_name(wpilib_project)}:{fixup_python_dep_name(library)}"
    )


def target_from_python_dep(python_dep):
    if "native" in python_dep:
        base_library = python_dep.replace("robotpy-native-", "").replace("-", "_")
        return f"//{fixup_root_package_name(base_library)}:{fixup_python_dep_name(python_dep)}"
    else:
        base_library = python_dep.replace("robotpy-", "")
        return f"//{fixup_root_package_name(base_library)}/src/main/python"


def strip_src_prefix(path):
    return pathlib.PurePath(path).as_posix().removeprefix("src/")


def native_wrapper_context(raw_config, args):
    """
    Template values for a library that wraps a standard allwpilib native library
    (tool.hatch.build.hooks.nativelib)
    """
    nativelib_config = raw_config["tool"]["hatch"]["build"]["hooks"]["nativelib"]
    project_name = (
        raw_config["project"]["name"].replace("robotpy-native-", "").replace("-", "_")
    )
    root_package = fixup_root_package_name(project_name)
    pc_files = []

    local_pc_names = set()
    for i, raw_pc in enumerate(nativelib_config.get("pcfile", [])):
        pcfile = parse_input(
            raw_pc,
            PcFileConfig,
            "pyproject.toml",
            f"tool.hatch.build.hooks.nativelib.pcfile[{i}]",
        )
        if pcfile.enable_if and not Marker(pcfile.enable_if).evaluate():
            continue
        pc_files.append(pcfile)
        local_pc_names.add(pcfile.get_pc_path().name[:-3])

    requires = set()
    for pcfile in pc_files:
        if pcfile.requires:
            for dep in pcfile.requires:
                if dep not in local_pc_names:
                    requires.add(dep)

    maven_libs = []
    for maven_dep in raw_config["tool"]["hatch"]["build"]["hooks"]["robotpy"][
        "maven_lib_download"
    ]:
        for lib in maven_dep["libs"]:
            maven_libs.append(
                dict(
                    name=lib,
                    library=f"shared/{lib}",
                    base_path=f"native/{project_name}/",
                )
            )

    # label=strip_prefix pairs for header trees that live in a Bazel module
    # rather than under thirdparty/, e.g. @libuv//:include_files=include.
    module_include_targets = []
    module_include_repos = set()
    for entry in args.module_include_targets:
        label = entry.partition("=")[0]
        module_include_targets.append(label)
        module_include_repos.add("*" + label.removeprefix("@").split("//")[0] + "*")

    replace_prefix_keys = []
    if args.native_srcs_root:
        replace_prefix_keys.append(
            args.package_name + "/" + args.native_srcs_root + "include"
        )
        for d in args.third_party_dirs:
            replace_prefix_keys.append(
                args.package_name
                + "/"
                + args.native_srcs_root
                + "thirdparty/"
                + d
                + "/include"
            )

    if args.generated_include_target:
        replace_prefix_keys.append(root_package + "/" + args.generated_include_root)
    for entry in args.module_include_targets:
        replace_prefix_keys.append(entry.partition("=")[2])
    replace_prefix_keys.sort()

    return dict(
        macro_signature="define_native_wrapper(name, pyproject_toml = None)",
        project_name=project_name,
        third_party_dirs=args.third_party_dirs,
        extra_include_root_files=args.extra_include_root_files,
        generated_include_target=args.generated_include_target,
        native_srcs_root=args.native_srcs_root,
        replace_prefix_keys=replace_prefix_keys,
        module_include_targets=module_include_targets,
        module_include_repos=sorted(module_include_repos),
        libinit_files=[strip_src_prefix(p.get_init_module_path()) for p in pc_files],
        pc_files=[strip_src_prefix(p.pcfile) for p in pc_files],
        pc_deps=[get_pc_dep(d) for d in sorted(requires)],
        python_deps=[get_python_dep(d) for d in sorted(requires)],
        maven_libs=maven_libs,
        strip_path_prefixes=[root_package],
        imports_dir=None,
        entry_points={
            "pkg_config": [f"{p.name} = native.{project_name}" for p in pc_files],
        },
    )


def pybind_library_context(raw_config, args):
    """
    Template values for a python library, which may or may not have semiwrap generated
    extension modules (tool.semiwrap)
    """
    stripped_include_prefix = args.stripped_include_prefix

    extension_modules = []
    entry_points = collections.defaultdict(list)

    # Cache built up for an extension module. Gets reset when an ExtensionModule is encountered
    additional_extension_targets: dict[str, BuildTarget] = {}
    publish_casters_targets = []

    # Pure python projects (no semiwrap section) have nothing for semiwrap to plan
    is_semiwrap_project = try_tomli_lookup(raw_config, "tool.semiwrap") is not None
    if is_semiwrap_project:
        plan = makeplan(args.project_file.parent)

        hack_pkgconfig(args.pkgcfgs)

        pyproject = PyProject(args.project_file)
        projectcfg = pyproject.project
    else:
        plan = []

    for item in plan:
        if isinstance(item, ExtensionModule):
            extension_modules.append(
                BazelExtensionModule(
                    item, additional_extension_targets, stripped_include_prefix
                )
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
                    raise RuntimeError(f"Repeated target {item.command}")
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
                publish_casters_targets.append(
                    PublishCastersConfig(projectcfg, item, stripped_include_prefix)
                )
            else:
                raise RuntimeError(f"Unhandled build target {item.command}")
        elif isinstance(item, Entrypoint):
            entry_points[item.group].append(f"{item.name} = {item.package}")
        elif isinstance(item, (LocalDependency, CppMacroValue)):
            pass
        else:
            raise TypeError(f"Unknown item {type(item)}")

    top_level_name = try_tomli_lookup(
        raw_config, "tool.hatch.build.targets.wheel.packages"
    )
    if top_level_name is None:
        top_level_name = [raw_config["project"]["name"]]
    assert len(top_level_name) == 1
    top_level_name = top_level_name[0]

    EXTERNAL_PYPI_DEPS = [
        "robotpy-cli",
        "pytest-reraise",
        "pytest",
    ]

    python_deps = []
    has_external_python_deps = False
    if "dependencies" in raw_config["project"]:
        for d in raw_config["project"]["dependencies"]:
            for external_dep in EXTERNAL_PYPI_DEPS:
                if external_dep in d:
                    has_external_python_deps = True
                    python_deps.append(f'requirement("{external_dep}")')
                    break
            else:
                pd = target_from_python_dep(d.split("==")[0])
                python_deps.append(pd)

    all_local_native_deps = set()
    for em in extension_modules:
        all_local_native_deps.update(em.native_wrapper_dependencies)
    all_local_native_deps = sorted(all_local_native_deps)

    # Shared libraries built elsewhere in allwpilib that get shipped inside this wheel
    maven_libs = []
    for maven_dep in try_tomli_lookup(
        raw_config, "tool.hatch.build.hooks.robotpy.maven_lib_download", []
    ):
        if maven_dep.get("use_headers", True):
            raise NotImplementedError(
                f"Shipping headers for {maven_dep['artifact_id']} is not supported"
            )
        for lib in maven_dep["libs"]:
            maven_libs.append(
                dict(
                    name=lib,
                    library=maven_dep_to_library(maven_dep, lib),
                    base_path=f"{stripped_include_prefix}{maven_dep['extract_to']}/",
                )
            )

    # The package the generated file is loaded from is usually the project root, but a
    # project can generate a build file for a module in a subpackage (e.g. test modules).
    bazel_package = args.package_name or fixup_root_package_name(top_level_name)

    has_semiwrap_files = False
    for em in extension_modules:
        if em.generation_data:
            has_semiwrap_files = True
            break

    return dict(
        macro_signature="define_pybind_library(name, pkgcfgs = [], extra_pybind_hdrs = [])",
        is_semiwrap_project=is_semiwrap_project,
        extension_modules=extension_modules,
        top_level_name=top_level_name,
        publish_casters_targets=publish_casters_targets,
        python_deps=sorted(python_deps),
        all_local_native_deps=all_local_native_deps,
        include_root_prefix=stripped_include_prefix,
        imports_dir=stripped_include_prefix if stripped_include_prefix else ".",
        strip_path_prefixes=[f"{bazel_package}/{stripped_include_prefix}"],
        yml_prefix=args.yml_prefix,
        package_root_file=args.package_root_file,
        entry_points=entry_points,
        version_file=try_tomli_lookup(
            raw_config, "tool.hatch.build.hooks.robotpy.version_file"
        ),
        maven_libs=maven_libs,
        has_external_python_deps=has_external_python_deps,
        has_semiwrap_files=has_semiwrap_files,
    )


def generate_build_file(raw_config, args):
    is_native_wrapper = (
        try_tomli_lookup(raw_config, "tool.hatch.build.hooks.nativelib") is not None
    )

    if is_native_wrapper:
        context = native_wrapper_context(raw_config, args)
    else:
        context = pybind_library_context(raw_config, args)

    # The entry points implied by the project layout are filled in above. This adds any
    # explicitly declared ones
    entry_points = context["entry_points"]
    for entry_point_type, explicit_entry_points in (
        raw_config["project"].get("entry-points", {}).items()
    ):
        for ep_key, ep_value in explicit_entry_points.items():
            entry_points.setdefault(entry_point_type, []).append(
                f"{ep_key} = {ep_value}"
            )

    authors = raw_config["project"].get("authors")
    if authors:
        author_email = f"{authors[0]['name']} <{authors[0]['email']}>"
    else:
        author_email = None

    template_file = "shared/bazel/rules/robotpy/pybind_build_file_template.jinja2"
    with open(template_file, "r") as f:
        template_contents = f.read()

    env = Environment(loader=BaseLoader)
    env.filters["jsonify"] = jsonify
    template = env.from_string(template_contents)

    with open(args.output_file, "w", newline="\n") as f:
        f.write(
            template.render(
                is_native_wrapper=is_native_wrapper,
                raw_project_config=raw_config["project"],
                author_email=author_email,
                readme=raw_config["project"].get("readme"),
                extra_distinfo_files={
                    f: f"licenses/{f}"
                    for f in raw_config["project"].get("license-files", [])
                },
                **context,
            )
            + "\n"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_file", type=pathlib.Path, required=True)
    parser.add_argument("--output_file", type=pathlib.Path, required=True)
    parser.add_argument("--package_name", type=str)

    # Arguments for pybind / pure python projects
    parser.add_argument("--stripped_include_prefix", type=str, default="")
    parser.add_argument("--yml_prefix", type=str)
    parser.add_argument("--package_root_file", type=str)
    parser.add_argument("--pkgcfgs", type=pathlib.Path, nargs="+")

    # Arguments for native library wrappers
    native_args = parser.add_argument_group("native wrapper arguments")
    native_args.add_argument("--third_party_dirs", nargs="+", default=[])
    native_args.add_argument("--module_include_targets", nargs="+", default=[])
    native_args.add_argument("--native_srcs_root")
    native_args.add_argument("--generated_include_target", default=None)
    native_args.add_argument("--generated_include_root")
    native_args.add_argument("--extra_include_root_files", nargs="+", default=[])

    args = parser.parse_args()

    with open(args.project_file, "rb") as fp:
        raw_config = tomli.load(fp)

    if try_tomli_lookup(raw_config, "tool.hatch.build.hooks.nativelib") is not None:
        if args.package_name is None:
            parser.error("--package_name is required for native wrappers")
    else:
        for action in native_args._group_actions:
            if getattr(args, action.dest) != action.default:
                parser.error(
                    f"{action.option_strings[0]} is only valid for native wrappers"
                )

    generate_build_file(raw_config, args)


if __name__ == "__main__":
    main()
