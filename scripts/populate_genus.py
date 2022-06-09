import json
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Augment species.json file with additional fields')
    parser.add_argument('jsonfile', help='Path to species.json file.')
    args = parser.parse_args()

    data = json.load(open(args.jsonfile, 'r'))

    for tree in data:
        tree['GENUS'] = tree['SCIENTIFIC'].split()[0]

    with open(args.jsonfile, 'w') as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)