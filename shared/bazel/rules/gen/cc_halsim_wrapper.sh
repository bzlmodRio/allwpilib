#!/usr/bin/env bash
# Bazel C++ launcher — injects HALSIM_EXTENSIONS via runfiles, optionally
# smoke-testing the wrapped executable for a startup crash.
#
# Backs wpilib_cc_binary (shared/bazel/rules/cc_rules.bzl). Unlike the Java
# launcher (java_native_libs_wrapper.sh), a plain cc_binary already resolves
# all of its own linked native dependencies via RPATH with no help needed, so
# this script's only job is resolving the absolute path(s) of any declared
# HAL simulation extensions (halsim_deps) and exporting HALSIM_EXTENSIONS
# before exec'ing/monitoring the wrapped binary — see
# hal/src/main/native/sim/Extensions.cpp for the env var HAL itself reads.
#
# The smoke-test mechanism (background + poll instead of exec, plain bash
# job control instead of the external `timeout(1)`) is identical to
# java_native_libs_wrapper.sh — see that script's comments for the full
# rationale.
#
# Required environment variables (set by the enclosing target in cc_rules.bzl):
#   CC_EXECUTABLE_RLOCATION   rlocation key of the wrapped cc_binary
#
# Optional (wpilib_cc_binary only, when it has halsim_deps):
#   HALSIM_LIBS_RLOCATION      rlocation key of the flat halsim-libs directory
#   HALSIM_MANIFEST_RLOCATION  rlocation key of a newline-delimited list of
#                              HALSIM_LIBS_RLOCATION basenames to auto-load
#                              via HALSIM_EXTENSIONS.
#
# Optional (smoke tests only):
#   SMOKE_TEST_TIMEOUT_SECONDS  if set, don't exec the wrapped binary as the
#                              final process. Instead run it in the
#                              background, and treat it still being alive
#                              after this many seconds as success (these are
#                              robot simulation programs that run forever
#                              once started, so a program that exits early is
#                              the failure signal).

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

# The exec'd binary below may itself be a Bazel-built target that needs to
# resolve its own runfiles (e.g. if it reads data files) — see
# java_native_libs_wrapper.sh's identical call for why this is needed for
# `bazel run` specifically, not just `bazel test`.
runfiles_export_envvars

cc_bin_key="${CC_EXECUTABLE_RLOCATION:?CC_EXECUTABLE_RLOCATION must be set}"

# Resolve the wrapped executable.
# On Windows, Bazel appends .exe to binary rlocation keys in the manifest.
cc_bin="$(rlocation "$cc_bin_key" 2>/dev/null || true)"
if [[ -z "$cc_bin" ]]; then
  cc_bin="$(rlocation "${cc_bin_key}.exe" 2>/dev/null || true)"
fi
if [[ -z "$cc_bin" ]]; then
  echo >&2 "ERROR: cannot resolve C++ executable: $cc_bin_key"
  exit 1
fi

# HALSIM_LIBS_RLOCATION/HALSIM_MANIFEST_RLOCATION are only set by
# wpilib_cc_binary targets that declared halsim_deps; plain examples never
# set them, so this whole block is a no-op for them.
halsim_libs_key="${HALSIM_LIBS_RLOCATION:-}"
halsim_manifest_key="${HALSIM_MANIFEST_RLOCATION:-}"
if [[ -n "$halsim_libs_key" && -n "$halsim_manifest_key" ]]; then
  halsim_libs_dir="$(rlocation "$halsim_libs_key" 2>/dev/null || true)"
  halsim_manifest="$(rlocation "$halsim_manifest_key" 2>/dev/null || true)"
  if [[ -n "$halsim_libs_dir" && -n "$halsim_manifest" && -s "$halsim_manifest" ]]; then
    # The halsim .so's own transitive dependencies (e.g. libwpimath.so) live
    # alongside it in halsim_libs_dir, but dlopen()ing an extension by
    # absolute path doesn't consult its RPATH-relative siblings the way
    # normal executable startup does - the OS loader needs an explicit
    # search-path env var to find them (same reasoning as
    # java_native_libs_wrapper.sh's LD_LIBRARY_PATH/DYLD_FALLBACK_LIBRARY_PATH
    # export). Without this, the initial dlopen() fails, and
    # HAL_LoadOneExtension's non-Windows retry - which blindly wraps
    # whatever string it was given in "lib" and ".so" - mangles the already-
    # absolute path into a nonsensical name that also fails, obscuring the
    # real (missing-dependency) error.
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*)
        export PATH="$halsim_libs_dir:$PATH"
        ;;
      Darwin*)
        export DYLD_FALLBACK_LIBRARY_PATH="$halsim_libs_dir:${DYLD_FALLBACK_LIBRARY_PATH:-}"
        ;;
      *)
        export LD_LIBRARY_PATH="$halsim_libs_dir:${LD_LIBRARY_PATH:-}"
        ;;
    esac

    halsim_delim=":"
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*)
        # Matches DELIM in hal/src/main/native/sim/Extensions.cpp.
        halsim_delim=";"
        ;;
    esac

    halsim_extensions=""
    # `read`, not mapfile/readarray: the latter is a bash 4+ builtin, and
    # macOS ships bash 3.2.
    while IFS= read -r halsim_basename || [[ -n "$halsim_basename" ]]; do
      [[ -z "$halsim_basename" ]] && continue
      if [[ -n "$halsim_extensions" ]]; then
        halsim_extensions="${halsim_extensions}${halsim_delim}${halsim_libs_dir}/${halsim_basename}"
      else
        halsim_extensions="${halsim_libs_dir}/${halsim_basename}"
      fi
    done < "$halsim_manifest"

    if [[ -n "$halsim_extensions" ]]; then
      export HALSIM_EXTENSIONS="$halsim_extensions"
    fi
  fi
fi

if [[ -z "${SMOKE_TEST_TIMEOUT_SECONDS:-}" ]]; then
  exec "$cc_bin" "$@"
fi

# Smoke test mode: run in the background instead of exec'ing, so this script
# can observe whether the program is still alive once the budget elapses.
"$cc_bin" "$@" &
child_pid=$!

elapsed=0
while [[ "$elapsed" -lt "$SMOKE_TEST_TIMEOUT_SECONDS" ]] && kill -0 "$child_pid" 2>/dev/null; do
  sleep 1
  elapsed=$((elapsed + 1))
done

if kill -0 "$child_pid" 2>/dev/null; then
  echo "Smoke test PASS: still running after ${SMOKE_TEST_TIMEOUT_SECONDS}s, no startup crash."
  kill "$child_pid" 2>/dev/null || true
  grace=0
  while [[ "$grace" -lt 5 ]] && kill -0 "$child_pid" 2>/dev/null; do
    sleep 1
    grace=$((grace + 1))
  done
  kill -9 "$child_pid" 2>/dev/null || true
  wait "$child_pid" 2>/dev/null || true
  exit 0
fi

rc=0
wait "$child_pid" || rc=$?
echo "Smoke test FAIL: exited after ${elapsed}s with code $rc, before the ${SMOKE_TEST_TIMEOUT_SECONDS}s timeout - see output above for the crash." >&2
exit 1
