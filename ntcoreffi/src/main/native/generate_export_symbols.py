import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file")
    parser.add_argument("--symbols_file")
    args = parser.parse_args()

    with open(args.symbols_file) as f:
        symbols = f.readlines()

    with open(args.output_file, "w") as f:
        for line in symbols:
            f.write(f"AddFunctionToLink({line.strip()});\n")


if __name__ == "__main__":
    main()
