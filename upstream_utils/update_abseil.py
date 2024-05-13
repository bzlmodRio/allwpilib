#!/usr/bin/env python3

import os
import shutil

from upstream_utils import (
    get_repo_root,
    clone_repo,
    comment_out_invalid_includes,
    copy_to,
    walk_cwd_and_copy_if,
    walk_if,
    git_am,
)


def main():
    upstream_root = clone_repo(
        "https://github.com/abseil/abseil-cpp.git", "20230802.1"
    )
    wpilib_root = get_repo_root()
    wpiutil = os.path.join(wpilib_root, "wpiutil")

    # Apply patches to upstream Git repo
    os.chdir(upstream_root)
    for f in [
    ]:
        git_am(os.path.join(wpilib_root, "upstream_utils/abseil_patches", f))

    # Delete old install
    for d in [
        "src/main/native/thirdparty/abseil/src",
        # "src/main/native/thirdparty/abseil/include",
    ]:
        shutil.rmtree(os.path.join(wpiutil, d), ignore_errors=True)

    def src_filter(dp, f):
        print(dp, f)

        if f.endswith("_test.cc"):
            return False

        if f.endswith("_benchmark.cc"):
            return False

        if "benchmark" in f:
            return False

        if "test" in f:
            return False

        if "mock" in f:
            return False

        if not f.endswith(".cc"):
            return False

        if "chi_square.cc" == f:
            return False

        if "gaussian_distribution_gentables.cc" == f:
            return False

        # if ("base/internal" in dp):
        #     return True

        # if ("log" in dp):
        #     return True

        # if ("status" in dp):
        #     return True

        # if ("time" in dp):
        #     return True

        # if ("strings" in dp):
        #     return True

        # if ("container" in dp):
        #     return True

        # if ("crc" in dp):
        #     return True

        # if ("flags" in dp):
        return True

        return False

    # Copy source files into allwpilib
    src_files = walk_if(".", src_filter)
    os.chdir(os.path.join(upstream_root))
    copy_to(src_files, os.path.join(wpiutil, "src/main/native/thirdparty/abseil/src"))

    # Copy header files into allwpilib
    def include_filter(dp, f):
        print(dp, f)
        if not dp.startswith("./absl"):
            return False

        return f.endswith(".h") or f.endswith(".inc")
        
    os.chdir(upstream_root)
    include_files = walk_if(".", include_filter)
    print(include_files)
    os.chdir(os.path.join(upstream_root))
    copy_to(
        include_files,
        os.path.join(wpiutil, "src/main/native/thirdparty/abseil/include"),
    )

    # Move internal files


if __name__ == "__main__":
    main()