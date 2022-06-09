import json
import argparse

# Usage:
# python split_species.py ./species.json 4

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Split species file into n equal(ish) parts.')
    parser.add_argument('jsonfile', help='Path to species.json file.')
    parser.add_argument('number', type=int, help='Number of files to create.')
    args = parser.parse_args()

    data = json.load(open(args.jsonfile, 'r'))

    chunksize = int(len(data) / args.number)
    splitdata = []

    for i in range(0, args.number - 1):
        splitdata.append(data[i*chunksize:(i+1)*chunksize-1])
    splitdata.append(data[(args.number-1)*chunksize:])

    if args.jsonfile[0:2] == './':
        args.jsonfile = args.jsonfile[2:]
    for i in range(0, args.number):
        spl = args.jsonfile.rsplit('.')
        with open(spl[0]+str(i+1)+'.json', 'w') as outfile:
            json.dump(splitdata[i], outfile, indent=2, ensure_ascii=False)