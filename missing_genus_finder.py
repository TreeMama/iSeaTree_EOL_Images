import json
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find missing genera')
    parser.add_argument('jsonfile', help='Path to species.json file.')
    args = parser.parse_args()

    data = json.load(open(args.jsonfile, 'r'))

	# create empty lists to hold genera
    genusList = []
    sppList = []

    for tree in data:
        commonName = tree['COMMON']
        genus = tree['GENUS']
		
		# append genus if it is not already in the list
        if genus not in genusList:
            genusList.append(genus)
			
		# append genus if it is already represented as a species (i.e. contains 'spp' in the common name)
        if 'spp' in commonName:
            sppList.append(genus)
	
	# create a new list of unique genera, removing those that are already accounted for
    missingGenusList = [x for x in genusList if x not in sppList]
	
	# print result
    print(missingGenusList)
