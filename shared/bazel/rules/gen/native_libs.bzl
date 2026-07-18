"""Flattens the transitively-collected native shared libraries of a set of
java targets into a single directory, so OS dynamic loaders (particularly
Windows' implicit DLL search, which prefers the loading DLL's own directory)
can resolve every native dependency uniformly."""

def _is_shared_lib_name(basename):
    if basename.endswith((".dylib", ".dll")):
        return True

    # Match ".so" as well as versioned sonames like "libfoo.so.4.13".
    so_index = basename.find(".so")
    if so_index == -1:
        return False
    remainder = basename[so_index + len(".so"):]
    return remainder == "" or remainder.startswith(".")

def _is_native_lib(f):
    return _is_shared_lib_name(f.basename)

def _is_solib_path(path):
    # Bazel's internal "_solib_*" symlink farm re-exposes cc_shared_library
    # (and cc_import-wrapped prebuilt library) outputs under a mangled path,
    # used for C++-level dynamic linking. For libraries built in this repo, a
    # canonical (non-mangled) copy also exists and is preferred; for some
    # prebuilt third-party libraries (e.g. OpenCV), the "_solib_*" copy is the
    # only one available, so it can't just be excluded outright.
    return "/_solib_" in path.replace("\\", "/")

# Flattens the (possibly empty) set of chosen native libs into out_dir via a
# single inline shell action: TreeArtifact outputs must be produced by one
# action, so there's no way to populate out_dir with per-file
# ctx.actions.symlink/declare_file calls. File contents are passed as
# argv (via ctx.actions.args()) rather than interpolated into the command
# string, so no shell quoting of paths is needed.
_FLATTEN_COMMAND = """
set -euo pipefail
out_dir="$1"
shift
mkdir -p "$out_dir"
while [ "$#" -gt 0 ]; do
  basename="$1"
  src="$2"
  shift 2
  cp "$src" "$out_dir/$basename"
done
"""

def _wpilib_flatten_native_libs_impl(ctx):
    file_sets = []
    for dep in ctx.attr.deps:
        if DefaultInfo not in dep:
            continue
        default_info = dep[DefaultInfo]
        if default_info.default_runfiles:
            file_sets.append(default_info.default_runfiles.files)
        file_sets.append(default_info.files)

    native_libs = [
        f
        for f in depset(transitive = file_sets).to_list()
        if _is_native_lib(f)
    ]

    # Dedupe by basename: prefer a canonical (non-solib) copy over one found
    # only in Bazel's "_solib_*" symlink farm, matching the old tool's logic.
    chosen = {}
    for f in native_libs:
        basename = f.basename
        existing = chosen.get(basename)
        if existing == None or (_is_solib_path(existing.path) and not _is_solib_path(f.path)):
            chosen[basename] = f

    out_dir = ctx.actions.declare_directory(ctx.label.name)

    args = ctx.actions.args()
    args.add(out_dir.path)
    for basename, f in chosen.items():
        args.add(basename)
        args.add(f.path)

    ctx.actions.run_shell(
        outputs = [out_dir],
        inputs = chosen.values(),
        arguments = [args],
        command = _FLATTEN_COMMAND,
        mnemonic = "WpilibFlattenNativeLibs",
        progress_message = "Flattening native libraries for %{label}",
    )
    return [DefaultInfo(files = depset([out_dir]))]

wpilib_flatten_native_libs = rule(
    implementation = _wpilib_flatten_native_libs_impl,
    attrs = {
        "deps": attr.label_list(mandatory = True),
    },
)
