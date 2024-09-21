find . -name *.bzl | xargs git add
find . -name BUILD.bazel | xargs git add
git add shared/bazel .bazelignore .bazelrc .bazelversion .github/workflows/bazel.yml  MODULE.bazel \
    MODULE.bazel.lock WORKSPACE WORKSPACE.bzlmod requirements.txt requirements_lock.txt \
    wpilibc/generate_wpilibc.py wpilibcExamples/generate_bazel_files.py wpilibj/generate_wpilibj.py wpilibjExamples/generate_bazel_files.py
git add .github/workflows/sync_fork.yml diff_origin.sh squashed_bzlmod_release_helper.sh .styleguide
git add upstream_utils/protobuf_patches/bzlmod/0001-Add-MODULE.bazel.patch
