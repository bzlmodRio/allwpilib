import json


def load_foldernames(filename):
    output = []

    with open(filename, 'r') as f:
        data = json.load(f)

    for test_data in data:
        output.append(test_data["foldername"])

    return sorted(set(output))

def load_tests(filename):
    output = []

    with open(filename, 'r') as f:
        data = json.load(f)

    for test_data in data:
        if test_data.get('hasunittests', False):
            output.append(test_data["foldername"])

    return sorted(set(output))


def main():
    examples = load_foldernames("wpilibcExamples/src/main/cpp/examples/examples.json")
    commands = load_foldernames("wpilibcExamples/src/main/cpp/commands/commands.json")
    templates = load_foldernames("wpilibcExamples/src/main/cpp/templates/templates.json")
    tests = load_tests("wpilibcExamples/src/main/cpp/examples/examples.json")

    with open("wpilibcExamples/example_projects.bzl", 'w') as f:
        f.write("EXAMPLE_FOLDERS = [\n    \"" + "\",\n    \"".join(examples) + "\",\n]\n\n")
        f.write("COMMANDS_V2_FOLDERS = [\n    \"" + "\",\n    \"".join(commands) + "\",\n]\n\n")
        f.write("TEMPLATES_FOLDERS = [\n    \"" + "\",\n    \"".join(templates) + "\",\n]\n\n")
        f.write("TESTS_FOLDERS = [\n    \"" + "\",\n    \"".join(tests) + "\",\n]\n\n")


if __name__ == "__main__":
    main()