git diff --name-status origin/main \
    ':!*.bazel' \
    ':!*.bzl' \
    ':!/shared/bazel/*' \
    ':!.bazelignore' \
    ':!.bazelrc' \
    ':!.bazelversion' \
    ':!.github/workflows/bazel.yml' \
    ':!.github/workflows/sync_fork.yml' \
    ':!MODULE.bazel.lock' \
    ':!WORKSPACE' \
    ':!WORKSPACE.bzlmod' \
    ':!/requirements*' \
