from python.runfiles import Runfiles
import argparse
import subprocess
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proto_files", nargs="+")
    parser.add_argument("--output_files", nargs="+")

    args = parser.parse_args()
    assert len(args.proto_files) * 2 == len(args.output_files)

    r = Runfiles.Create()
    protoc = r.Rlocation("com_google_protobuf/protoc")
    plugin = r.Rlocation("__main__/protoplugin/src/main/java/org/wpilib/protoplugin")

    output_directory = os.path.dirname(args.output_files[0])

    cmd = []
    cmd.append(protoc)
    cmd.append(f"--cpp_out={output_directory}")
    cmd.append(f"-Iwpimath/src/main/proto")
    cmd.append(
        f"--wpilib_out=bazel-out/k8-fastbuild/bin/wpimath/src/main/proto/temp_proto"
    )
    cmd.append(f"--plugin=protoc-gen-wpilib={plugin}")
    cmd.extend(args.proto_files)

    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
