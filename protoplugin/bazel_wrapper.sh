echo $@


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

TEMP_DIR=bazel-out/k8-fastbuild/bin/wpimath/src/main/proto/temp_proto
# mkdir $TEMP_DIR
touch hello_world.txt
pwd
echo "THING"
echo $(rlocation com_google_protobuf/protoc)
echo "THANG"
$(rlocation com_google_protobuf/protoc) --cpp_out=$TEMP_DIR $@ -Iwpimath/src/main/proto \
    --wpilib_out=bazel-out/k8-fastbuild/bin/wpimath/src/main/proto/temp_proto \
    --plugin=protoc-gen-wpilib=bazel-out/k8-opt-exec-ST-a828a81199fe/bin/protoplugin/src/main/java/org/wpilib/protoplugin
