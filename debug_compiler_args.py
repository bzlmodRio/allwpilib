import os
import shutil
import pathlib


def dump_static():
    gradle_file = r"C:\Users\PJ\git\wpilibsuite\allwpilib\wpiutil\build\tmp\createWpiutilBaseWindowsx86-64ReleaseStaticLibrary\options.txt"
    bazel_file = r"C:\Users\PJ\git\wpilibsuite\allwpilib\bazel-bin\wpiutil\_wpiutil.lib-0.params"

    lines = []
    with open(gradle_file, 'r') as f:
        for line in f.readlines():
            lines.append(str(pathlib.Path(line.strip()).name))
            
    with open("static.gradle.txt", 'w') as f:
        f.write("\n".join(sorted(lines)))
        
    lines = []
    with open(bazel_file, 'r') as f:
        for line in f.readlines():
            lines.append(str(pathlib.Path(line.strip()).name))
            
    with open("static.bazel.txt", 'w') as f:
        f.write("\n".join(sorted(lines)))


def main():
    project = "wpiutil"
    project_upper = project[0].upper() + project[1:]
    cpp_file = "SmallVector"
    release_type = "Release"
    

    gradle_file = os.path.join(project, "build", "tmp", f"compile{project_upper}BaseWindowsx86-64{release_type}StaticLibrary{project_upper}BaseWindowsx86-64ReleaseStaticLibrary{project_upper}WindowsCpp", "options.txt")
    print(r"wpiutil\build\tmp\compileWpiutilBaseWindowsx86-64ReleaseStaticLibraryWpiutilBaseWindowsx86-64ReleaseStaticLibraryWpiutilWindowsCpp\options.txt")
    print(gradle_file)
    print(os.path.exists(gradle_file))

    bazel_file = os.path.join("bazel-bin", project, "_objs", "_" + project, cpp_file + ".obj.params")
    print("bazel-bin\wpiutil\_objs\wpiutil\DataLog.obj.params")
    print(bazel_file)
    print(os.path.exists(bazel_file))


    shutil.copy(gradle_file, "compare.gradle.txt")
    shutil.copy(bazel_file, "compare.bazel.txt")


    gradle_file = os.path.join(project, "build", "tmp", "generateExportsWpiutilWindowsx86-64ReleaseSharedLibrary/exports.def")
    bazel_file = f"bazel-out/x64_windows-opt/bin/{project}/{project}.gen.def"
    
    # shutil.copy(gradle_file, "def.gradle.txt")
    # shutil.copy(bazel_file, "def.bazel.txt")

    dump_static()

if __name__ == "__main__":
    main()