from typing import List
import requests
from requests.models import HTTPError
import json
import time
import urllib
import os
import argparse


def get_search_url(species: str) -> str:
    params = {'q': species, 'page': 1, 'exact': True}
    return "https://eol.org/api/search/1.0.json?" + urllib.parse.urlencode(params)


def get_objects_url(id: int) -> str:
    return f'https://eol.org/api/pages/1.0/{id}.json?details=true&images_per_page=10'


def fetch_species_id(species: str) -> int:

    try:
        url = get_search_url(species)
        print(f'Calling search: {url}')
        response = requests.get(url)
        response.raise_for_status()

        json = response.json()
        id = 0
        for res in json['results']:
            if res['title'].upper() == species.upper():
                id = res['id']
                break
        return id
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error: {err}')


def fetch_data_objects(eol_id: int) -> str:

    try:
        url = get_objects_url(eol_id)
        print(f'Calling {url}')
        response = requests.get(url)
        response.raise_for_status()

        json = response.json()

        return json['taxonConcept']['dataObjects']

    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error: {err}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download images for species in species.json file')
    parser.add_argument('jsonfile', help='Path to species.json file.')
    parser.add_argument('start', type=int, nargs='?', default=0, help='Position to start at.')
    parser.add_argument('end', type=int, nargs='?', default=0, help='Position to end at.')
    args = parser.parse_args()

    data = json.load(open(args.jsonfile, 'r'))
    missing_ids = open('./missing.txt', 'a+')

    start = 0
    end = len(data)
    if args.start:
        start = args.start
    if args.end and (args.end > 0) and (args.end < len(data)):
        end = args.end
    print(f'Processing entries {start} to {end}...')
    for tree in data[start:end]:
        new_dir = './images/' + tree['ID']
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        eol_id = fetch_species_id(tree['SCIENTIFIC'])

        if eol_id == 0:
            missing_ids.write(str(tree['ID'])+': '+tree['SCIENTIFIC']+'\n')
            continue
        else:
            print(f'found id: {eol_id}')

        images = fetch_data_objects(eol_id)

        if images is not None:
            for image in images:
                image_path = new_dir+'/'+image['identifier'].replace('/', '_')
                print(f'Image path: {image_path}')
                if not os.path.isdir(image_path):
                    os.mkdir(image_path)

                with open(image_path + '/info.json', 'w') as outfile:
                    json.dump(image, outfile, indent=2, ensure_ascii=False)

                try:
                    thumb_file = image_path + '/thumb.' + image['dataSubtype']
                    urllib.request.urlretrieve(image['eolThumbnailURL'], thumb_file)

                    image_file = image_path + '/full.' + image['dataSubtype']
                    urllib.request.urlretrieve(image['eolMediaURL'], image_file)
                except Exception as e:
                    print(f'Error retrieving image: {e}')

            time.sleep(1)

    missing_ids.close()
