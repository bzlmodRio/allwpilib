import sys
import json

def main(argv):

    output_file = argv[0]
    print(output_file)

    config = []
    
    for i in range(1, len(argv), 2):
        config.append((argv[i].format(platform="linuxx86-64"), argv[i + 1]))
        # config.append((argv[i].format(platform="linuxx86-64debug"), argv[i + 1]))

    with open(output_file, 'w') as f:
        print("WRiting ta thit")
        json.dump(config, f, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])