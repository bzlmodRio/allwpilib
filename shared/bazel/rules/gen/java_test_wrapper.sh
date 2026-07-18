#!/usr/bin/env bash
# Bazel Java test launcher — resolves native-library paths via runfiles.
#
# On every OS we resolve the flat native-libs directory from the runfiles
# manifest and inject -Djava.library.path via --wrapper_script_flag (which
# the launcher applies after the params-file jvm_flags, so it always wins).
# That covers the JVM's own initial System.loadLibrary() call for the
# top-level JNI library (e.g. libwpiHaljni.so).
#
# -Djava.library.path/RPATH is not enough on any OS, though: once the JVM
# dlopen()s that first library, resolving *its* transitive native
# dependencies (e.g. libwpiHal.so, a sibling in the same flattened directory)
# is entirely up to the OS loader, which does not consult java.library.path.
# Relying on the .so's own baked-in RPATH/RUNPATH for this has proven
# unreliable for this flattened-directory layout (some $ORIGIN-relative
# entries point at Bazel's solib symlink farm, which can contain dangling
# symlinks; even the plain "$ORIGIN" fallback entry does not reliably find
# a sibling file that demonstrably exists in the same directory). So on
# every OS we also export the OS loader's own library-search-path env var
# pointing at the flattened native-libs dir, which does reliably work:
#   - Linux:   LD_LIBRARY_PATH
#   - macOS:   DYLD_FALLBACK_LIBRARY_PATH only (never DYLD_LIBRARY_PATH: unlike
#     LD_LIBRARY_PATH, it's consulted *before* a binary's own load-time paths,
#     which hijacks the java launcher's own bootstrap dylibs like libjli.dylib
#     and breaks JVM startup entirely ("Failed setting boot class path").
#     DYLD_FALLBACK_LIBRARY_PATH is only consulted once the normal search
#     already failed, so it can't clobber a lookup that was already working.)
#   - Windows: PATH (MSYS2's compiled .exe launcher additionally can't do
#     shell variable expansion at all, so PATH is prepended unconditionally
#     there; the Windows DLL loader also uses PATH to find transitive DLL
#     dependencies, same rationale as LD_LIBRARY_PATH/DYLD_LIBRARY_PATH).
#
# Required environment variables (set by the enclosing target in java_rules.bzl):
#   NATIVE_LIBS_RLOCATION  rlocation key of the flat native-libs directory
#   JAVA_TEST_RLOCATION    rlocation key of the _java_impl test executable

# --- begin runfiles.bash initialization v3 ---
# Copy-pasted from the Bazel Bash runfiles library v3.
set -uo pipefail; set +e; f=bazel_tools/tools/bash/runfiles/runfiles.bash
# shellcheck disable=SC1090
source "${RUNFILES_DIR:-/dev/null}/$f" 2>/dev/null || \
  source "$(grep -sm1 "^$f " "${RUNFILES_MANIFEST_FILE:-/dev/null}" | cut -f2- -d' ')" 2>/dev/null || \
  source "$0.runfiles/$f" 2>/dev/null || \
  source "$(grep -sm1 "^$f " "$0.runfiles_manifest" | cut -f2- -d' ')" 2>/dev/null || \
  source "$(grep -sm1 "^$f " "$0.exe.runfiles_manifest" | cut -f2- -d' ')" 2>/dev/null || \
  { echo>&2 "ERROR: cannot find $f"; exit 1; }; f=; set -e
# --- end runfiles.bash initialization v3 ---

java_test_key="${JAVA_TEST_RLOCATION:?JAVA_TEST_RLOCATION must be set}"
native_libs_key="${NATIVE_LIBS_RLOCATION:?NATIVE_LIBS_RLOCATION must be set}"

# Resolve the java test binary.
# On Windows, Bazel appends .exe to binary rlocation keys in the manifest.
java_test_bin="$(rlocation "$java_test_key" 2>/dev/null || true)"
if [[ -z "$java_test_bin" ]]; then
  java_test_bin="$(rlocation "${java_test_key}.exe" 2>/dev/null || true)"
fi
if [[ -z "$java_test_bin" ]]; then
  echo >&2 "ERROR: cannot resolve java test binary: $java_test_key"
  exit 1
fi

# Not every target has native libs (e.g. pure-Java modules with no JNI
# deps), in which case the flattened directory is empty and may not resolve
# via rlocation at all. Treat that as "nothing to inject" rather than a
# fatal error.
native_libs_dir="$(rlocation "$native_libs_key" 2>/dev/null || true)"

wrapper_flags=()
if [[ -n "$native_libs_dir" ]]; then
  wrapper_flags+=("--wrapper_script_flag=--jvm_flag=-Djava.library.path=$native_libs_dir")

  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
      # rlocation returns a mixed-style Windows path (C:/...) on Windows.
      # PATH prepend: use as-is; MSYS2 converts it for the Windows exe child.
      # This ensures the whole transitive DLL chain is found
      # (LOAD_WITH_ALTERED_SEARCH_PATH only covers first-level deps, PATH
      # covers the rest).
      export PATH="$native_libs_dir:$PATH"
      ;;
    Darwin*)
      export DYLD_FALLBACK_LIBRARY_PATH="$native_libs_dir:${DYLD_FALLBACK_LIBRARY_PATH:-}"
      ;;
    *)
      export LD_LIBRARY_PATH="$native_libs_dir:${LD_LIBRARY_PATH:-}"
      ;;
  esac
fi

# The ${arr[@]+"${arr[@]}"} form (rather than plain "${wrapper_flags[@]}") is
# required for macOS's default bash (3.2, frozen there for licensing reasons):
# it throws "unbound variable" under `set -u` when expanding an empty array,
# a bug fixed upstream in bash 4.4+ but never backported by Apple.
exec "$java_test_bin" ${wrapper_flags[@]+"${wrapper_flags[@]}"} "$@"
