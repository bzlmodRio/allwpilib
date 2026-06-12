/home/pjreiniger/git/bazel/bazel-bin/src/tools/execlog/parser \
  --log_path=/tmp/exec.log \
  --log_path=/tmp/local_compact.log \
  --output_path=/tmp/exec.log.txt \
  --output_path=/tmp/local_compact.log.txt

mv /tmp/exec.log.txt .
git add exec.log.txt

# diff /tmp/exec.log.txt /tmp/local_compact.log.txt > diff.patch
