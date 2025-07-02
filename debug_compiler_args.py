import os
import shutil
import pathlib
import platform


def sort_and_rewrite_file(input_file, output_file):
    with open(input_file, 'r') as f:
        for line in f.readlines():
            lines.append(str(pathlib.Path(line.strip()).name))
            
    with open(output_file, 'w') as f:
        f.write("\n".join(sorted(lines)))

def dump_static(project, project_upper, operating_system, release_type):
    gradle_file = os.path.join(project, "build", "tmp", f"generateExports{project_upper}{operating_system}{release_type}SharedLibrary/exports.def")
    gradle_file = os.path.join(project, "build", "tmp", f"create{project_upper}Base{operating_system}{release_type}StaticLibrary/options.txt")
    bazel_file = os.path.join("bazel-bin", project, "_" + project + ".lib-0.params")

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


def copy_compiler_flags(project, project_upper, operating_system, release_type, cpp_file):
    if project == "wpiutil":
        gradle_file = os.path.join(project, "build", "tmp", f"compile{project_upper}Base{operating_system}{release_type}StaticLibrary{project_upper}Base{operating_system}ReleaseStaticLibrary{project_upper}WindowsCpp", "options.txt")
    else:
        gradle_file = os.path.join(project, "build", "tmp", f"compile{project_upper}Base{operating_system}{release_type}StaticLibrary{project_upper}BaseCpp", "options.txt")
    bazel_file = os.path.join("bazel-bin", project, "_objs", "_" + project, cpp_file + ".obj.params")

    print(gradle_file)
    print(r"wpilibc\build\tmp\compileWpilibcBaseWindowsx86-64ReleaseStaticLibraryWpilibcBaseCpp\options.txt")
    shutil.copy(gradle_file, "compare.gradle.txt")
    shutil.copy(bazel_file, "compare.bazel.txt")


def copy_exports(project, project_upper, operating_system, release_type):
    
    gradle_file = os.path.join(project, "build", "tmp", f"generateExports{project_upper}{operating_system}{release_type}SharedLibrary/exports.def")
    bazel_file = f"bazel-bin/{project}/{project}.gen.def"
    
    shutil.copy(gradle_file, "def.gradle.txt")

    shutil.copy(bazel_file, "def.bazel.txt")
    os.chmod("def.bazel.txt", 0o777)



def collect_gradle_info(base_output_directory, project, cpp_file, release_type):
    system = platform.system()
    if system == "Linux":
        operating_system = "Linuxx86-64"
    elif system == "Windows":
        operating_system = "Windowsx86-64"
    elif system == "Darwin":
        operating_system = "Osxx86-64"
    
    project_upper = project[0].upper() + project[1:]


    output_directory = base_output_directory / project / cpp_file
    output_directory.mkdir(parents=True, exist_ok=True)

    
    static_lib_linker_options = os.path.join(project, "build", "tmp", f"create{project_upper}Base{operating_system}{release_type}StaticLibrary/options.txt")
    try:
        sort_and_rewrite_file(static_lib_linker_options, output_directory / "static.gradle.txt")
    except:
        pass

    if system == "Windows":
        dll_exports_options = os.path.join(project, "build", "tmp", f"generateExports{project_upper}{operating_system}{release_type}SharedLibrary/exports.def")
        shutil.copy(gradle_file, "def.gradle.txt")

        
    if project == "wpiutil":
        compiler_flag_options = os.path.join(project, "build", "tmp", f"compile{project_upper}Base{operating_system}{release_type}StaticLibrary{project_upper}Base{operating_system}ReleaseStaticLibrary{project_upper}WindowsCpp", "options.txt")
    else:
        compiler_flag_options = os.path.join(project, "build", "tmp", f"compile{project_upper}Base{operating_system}{release_type}StaticLibrary{project_upper}BaseCpp", "options.txt")
    shutil.copy(compiler_flag_options, output_directory / "compare.gradle.txt")

def main():
    project = "wpilibc"
    cpp_file = "Solenoid"
    
    release_type = "Debug"

    info_to_gather = [
        ("wpilibc", "Solenoid"),
        ("wpinet", "WebServer"),
        ("apriltag", "AprilTag"),
    ]
    
    # project = "wpiutil"
    # cpp_file = "SmallVector"
    
    # project = "wpinet"
    # cpp_file = "WebServer"
    
    # project = "apriltag"
    # cpp_file = "AprilTag"

    for release_type in ["Release", "Debug"]:
        for project, cpp_file in info_to_gather:
            base_output_directory = pathlib.Path("xxx__debug_compiler") / release_type
            collect_gradle_info(base_output_directory, project, cpp_file, release_type)

    

    # operating_system = "Windowsx86-64"
    # project_upper = project[0].upper() + project[1:]
    

    # copy_compiler_flags(project, project_upper, operating_system, release_type, cpp_file)
    # copy_exports(project, project_upper, operating_system, release_type)
    # dump_static(project, project_upper, operating_system, release_type)


if __name__ == "__main__":
    main()