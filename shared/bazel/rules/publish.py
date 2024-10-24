import os
import sys
import json
import shutil


def write_pom_file(group_id, artifact_id, version, output_file):
    contents = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group_id}</groupId>
  <artifactId>{artifact_id}</artifactId>
  <version>{version}</version>"""
    if "java" not in artifact_id:
        contents += "\n  <packaging>pom</packaging>"

    contents += """
</project>
"""

    with open(output_file, 'w') as f:
        f.write(contents)


def write_maven_metadata_file(group_id, artifact_id, version, output_file):
    contents = f"""<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <groupId>{group_id}</groupId>
  <artifactId>{artifact_id}</artifactId>
  <versioning>
    <latest>{version}</latest>
    <release>{version}</release>
    <versions>
      <version>{version}</version>
    </versions>
    <lastUpdated>20241024032743</lastUpdated>
  </versioning>
</metadata>
"""

    with open(output_file, 'w') as f:
        f.write(contents)



def main(argv):

    print(argv)
    version = "6969"
    maven_base = "/home/pjreiniger/git/tmp_maven/"

    unique_artifact_folders_info = set()

    print("*" * 80)
    for bundle_config_file in argv[:]:
        bundle_config = json.load(open(bundle_config_file))
        for maven_coordinate, original_file in bundle_config:
            parts = maven_coordinate.split(":")
            if len(parts) == 2:
                group_id, artifact_name = parts
                suffix = ""
            elif len(parts) == 3:
                group_id, artifact_name, suffix = parts

            unique_artifact_folders_info.add((group_id, artifact_name))

            group_id_dir = group_id.replace(".", "/")

            print(original_file)

            output_file = os.path.join(maven_base, group_id_dir, artifact_name, version, f"{artifact_name}-{version}{suffix}")
            if not original_file.endswith(".jar"):
                output_file += ".zip"
            else:
                output_file += ".jar"
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            shutil.copy("/home/pjreiniger/git/allwpilib/" + original_file, output_file)
            os.chmod(output_file, 0o777)
            print(output_file, os.path.exists(output_file))
            # print(group_id, artifact_name)
    print("*" * 80)

    # print("Hello world")

    hack_version = "2025.424242.1.1-beta-1-20241023232716-35-gcd4a09d"

    for group_id, artifact_name in unique_artifact_folders_info:
        group_id_dir = group_id.replace(".", "/")
        write_maven_metadata_file(group_id, artifact_name, hack_version, os.path.join(maven_base, group_id_dir, artifact_name, "maven-metadata-local.xml"))
        write_pom_file(group_id, artifact_name, hack_version, os.path.join(maven_base, group_id_dir, artifact_name, version, f"{artifact_name}-{version}.pom"))
        print(group_id, artifact_name)


if __name__ == "__main__":
    main(sys.argv[1:])