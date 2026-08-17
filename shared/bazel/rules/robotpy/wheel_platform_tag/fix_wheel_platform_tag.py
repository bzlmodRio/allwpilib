"""
Renames a built wheel to carry the platform tag it actually satisfies.

Ported from mostrobotpy's Subproject._fix_wheel_name / _fix_linux_wheel_name
(devtools/subproject.py), which uses auditwheel to inspect the glibc/libstdc++
symbols the compiled extensions inside the wheel actually reference, rather than
hardcoding a manylinux tag per target/toolchain.
"""

import argparse
import pathlib
import shutil
import sys

# Needed for compatibility with python compiled with older xcode.
_ADJUST_WHEEL_TAGS = {
    "macosx_11_0_x86_64": "macosx_10_16_x86_64",
    "macosx_12_0_x86_64": "macosx_10_16_x86_64",
}


def _fix_linux_wheel_name(wheel_path: pathlib.Path) -> str:
    from auditwheel.error import AuditwheelError
    from auditwheel.wheel_abi import analyze_wheel_abi
    from auditwheel.wheeltools import get_wheel_architecture, get_wheel_libc

    try:
        arch = get_wheel_architecture(wheel_path.name)
    except AuditwheelError:
        arch = None

    try:
        libc = get_wheel_libc(wheel_path.name)
    except AuditwheelError:
        libc = None

    try:
        winfo = analyze_wheel_abi(
            libc,
            arch,
            wheel_path,
            frozenset(),
            disable_isa_ext_check=True,
            allow_graft=True,
        )
    except AuditwheelError:
        return wheel_path.name
    else:
        parts = wheel_path.name.split("-")
        parts[-1] = winfo.overall_policy.name
        return "-".join(parts) + ".whl"


def _fix_wheel_name(wheel_path: pathlib.Path) -> str:
    if sys.platform == "linux":
        return _fix_linux_wheel_name(wheel_path)

    name = wheel_path.name
    for old, new in _ADJUST_WHEEL_TAGS.items():
        old_whl = f"{old}.whl"
        new_whl = f"{new}.whl"
        if name.endswith(old_whl):
            name = f"{name[:-len(old_whl)]}{new_whl}"
    return name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--wheel", dest="wheels", action="append", required=True, type=pathlib.Path
    )
    parser.add_argument("--output_dir", required=True, type=pathlib.Path)
    args = parser.parse_args()

    for wheel in args.wheels:
        fixed_name = _fix_wheel_name(wheel)
        shutil.copyfile(wheel, args.output_dir / fixed_name)


if __name__ == "__main__":
    main()
