#!/bin/bash
# set -e

git checkout 2027 -- .

git diff 2027 --name-only --diff-filter=A | xargs git rm -f

git clean -fd
# git checkout HEAD ntcore/generate_topics.py
# git checkout HEAD ntcore/src/generate


# git checkout HEAD wpiutil/robotpy_pybind_build_info.bzl
# git checkout HEAD wpiutil/src/main/python/pyproject.toml
# git checkout HEAD wpiutil/src/main/python/semiwrap/Sendable.yml
# git checkout HEAD wpiutil/src/main/python/semiwrap/SendableRegistry.yml
# git checkout HEAD wpiutil/src/test/native/cpp/llvm/FunctionExtrasTest.cpp
# git checkout HEAD wpinet/robotpy_pybind_build_info.bzl
# git checkout HEAD wpinet/src/main/python/pyproject.toml
git checkout HEAD refactor* reset.sh

find . -type d -empty -delete
git --no-pager diff --name-status 2027
git reset

# bazel run //ntcore:write_ntcore

# git diff --name-only --diff-filter=D
