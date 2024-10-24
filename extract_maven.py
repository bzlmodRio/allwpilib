import os
import zipfile
import shutil

from elftools.elf.elffile import ELFFile
from elftools.elf.constants import E_FLAGS, E_FLAGS_MASKS
from elftools.elf.dynamic import DynamicSection
from elftools.elf.sections import SymbolTableSection


def delete_file(filepath):
    print("DELETING ", filepath)
    os.remove(filepath)
    pass

PROJECT_FILTER = [
    # "wpiutil",
    # "wpinet",
]

def extract_zip_files(maven_location):

    hdr_src_zips = []
    cpp_libs_zips = []
    for root, _, files in os.walk(maven_location):
        for f in files:
            full_file = os.path.join(root, f)
            extraction_path = os.path.splitext(full_file)[0]

            keep_going = False
            if PROJECT_FILTER:
                for project in PROJECT_FILTER:
                    if project in f:
                        keep_going = True
                        break
                if "zip" in f:
                    print(keep_going, f)
            else:
                keep_going = True
            if not keep_going:
                continue

            if f.endswith("-sources.zip") or f.endswith("-headers.zip") or f.endswith("-sources.jar"):
                if "debug" in f:
                    delete_file(full_file)
                    continue
                hdr_src_zips.append((full_file, extraction_path))
            elif f.endswith(".zip"):
                if "debug" in f:
                    delete_file(full_file)
                    continue
                cpp_libs_zips.append((full_file, extraction_path))
            elif f.endswith("linuxx86-64.jar"):
                cpp_libs_zips.append((full_file, extraction_path))
            elif f.endswith(".jar"):
                os.remove(full_file)

    # print(hdr_src_zips)
    # print(cpp_libs_zips)

    for full_file, extraction_path in hdr_src_zips:
        print("Extracting hdr/src to\n  ", full_file , " ->\n  ", extraction_path)
        if not os.path.exists(extraction_path):
            os.mkdir(extraction_path)

        with zipfile.ZipFile(full_file, 'r') as zip_ref:
            zip_ref.extractall(extraction_path)
        
        delete_file(full_file)
            
    for full_file, extraction_path in cpp_libs_zips:
        print("Extracting libs to\n  ", full_file , " ->\n  ", extraction_path)
        if not os.path.exists(extraction_path):
            os.mkdir(extraction_path)

        with zipfile.ZipFile(full_file, 'r') as zip_ref:
            zip_ref.extractall(extraction_path)
            
        delete_file(full_file)

    return cpp_libs_zips


def extract_cpp_info(cpp_libs_zips):
    print(cpp_libs_zips)

    lib_files = []

    for _, extraction_path in cpp_libs_zips:
        for root, _, files in os.walk(extraction_path):
             for f in files:
                full_file = os.path.join(root, f)
                extraction_path = os.path.splitext(full_file)[0]

                if f.endswith(".so"):
                    lib_files.append((full_file, extraction_path))

    for full_file, extraction_path in lib_files:
        print("Testing ", full_file)
        lib = ELFFile(open(full_file, 'rb'))
        
        if not os.path.exists(extraction_path):
            os.mkdir(extraction_path)
        
        for section in lib.iter_sections():
            if not isinstance(section, DynamicSection):
                continue

            dependencies = []
            for tag in section.iter_tags():
                if tag.entry.d_tag == 'DT_NEEDED':
                    dependencies.append(tag.needed)
            with open(os.path.join(extraction_path, "dependencies.txt"), 'w') as f:
                f.write("\n".join(dependencies))

        
        # check to make sure no symbols are defined in frc:: namespace
        for section in lib.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue
            symbols = []
            for symbol in section.iter_symbols():
                if symbol['st_info']['bind'] != 'STB_GLOBAL':
                    continue
                if symbol['st_shndx'] == 'SHN_UNDEF':
                    continue

                if symbol.name in ["__bss_start", "_edata", "_end"]:
                    continue

                symbols.append(symbol.name)

            symbols = sorted(symbols)
            
            with open(os.path.join(extraction_path, "symbols.txt"), 'w') as f:
                f.write("\n".join(symbols))

        delete_file(full_file)


def fixup_stupid_rename(maven_location, golden_release, new_release):

    the_files = []

    for root, _, files in os.walk(maven_location):
        for f in files:
            new_file = os.path.join(root, f)
            as_golden = new_file.replace(new_release, golden_release)

            the_files.append((new_file, as_golden))
            
    for new_file, as_golden in the_files:
        golden_parent = os.path.dirname(as_golden)
        if not os.path.exists(golden_parent):
            os.makedirs(golden_parent)

        shutil.move(new_file, as_golden)


def main():
    maven_location = "/home/pjreiniger/git/tmp_maven/edu/wpi/first"

    golden_release = "6969"
    new_release = "2025.424242.1.1-beta-1-20241023232716-35-gcd4a09d"

    fixup_stupid_rename(maven_location, golden_release, new_release)
    cpp_libs_zips = extract_zip_files(maven_location)
    extract_cpp_info(cpp_libs_zips)


if __name__ == "__main__":
    # ./gradlew publishToMavenLocal
    # mv ~/.m2/repository/edu/ ../tmp_maven/edu

    # git clean -fd *static/lib*.static/dependencies.txt *static/lib*.static/symbols.txt *jni/MANIFEST.MF; git checkout *jni/dependencies.txt *jni/symbols.txt
    main()