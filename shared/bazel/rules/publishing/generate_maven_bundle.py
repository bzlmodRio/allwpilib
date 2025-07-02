import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file")
    parser.add_argument("--platform")
    parser.add_argument("--debug_suffix", default="")
    parser.add_argument("--maven_infos", nargs="+")
    args = parser.parse_args()

    args.debug_suffix = args.debug_suffix or ""
    args.platform = args.platform or ""

    json_data = []

    for maven_info in args.maven_infos:
        artifact, maven_base, artifact_name, suffix = maven_info.split(",")
        json_data.append(
            dict(
                artifact=artifact.replace("##PLATFORM##", args.platform).replace("##DEBUG##", args.debug_suffix),
                maven_base=maven_base.replace("##PLATFORM##", args.platform).replace("##DEBUG##", args.debug_suffix),
                artifact_name=artifact_name.replace("##PLATFORM##", args.platform).replace("##DEBUG##", args.debug_suffix),
                suffix=suffix.replace("##PLATFORM##", args.platform).replace("##DEBUG##", args.debug_suffix),
            )
        )

    with open(args.output_file, "w") as f:
        f.write(json.dumps(json_data))


if __name__ == "__main__":
    main()
