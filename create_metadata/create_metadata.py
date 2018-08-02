# uses the inaturalist public api to get the list of bats (species and genera)
import urllib2
import json
import time
import numpy as np
import datetime

def get_info(data):
    res = {}
    res['inat_id'] = data['id']
    res['inat_parent_id'] = data['parent_id']
    res['rank'] = data['rank']
    res['name'] = data['name']
    res['inat_url'] = 'https://www.inaturalist.org/taxa/' + str(res['inat_id'])
    if 'wikipedia_url' in data.keys():
        res['wikipedia_url'] = data['wikipedia_url']
    if 'preferred_common_name' in data.keys():
        res['preferred_common_name'] = data['preferred_common_name']
    else:
        res['preferred_common_name'] = res['name']
    return res

def search_api(api_url, tid, taxa):
    url = api_url + tid
    response = urllib2.urlopen(url)
    data = json.load(response)
    rank = data['results'][0]['rank']

    if rank == 'species' or rank == 'genus':
        print(data['results'][0]['name'])
        res = get_info(data['results'][0])
        taxa.append(res)

    if 'children' in data['results'][0].keys():
        for tt in data['results'][0]['children']:
            time.sleep(1.0)
            search_api(api_url, str(tt['id']), taxa)

# define call types
call_types =\
    [{"id": 1, "name": "unknown"},
     {"id": 2, "name": "echolocation"},
     {"id": 3, "name": "social"},
     {"id": 4, "name": "feeding"}]

# define licenses
licenses =\
    [{"url": "http://creativecommons.org/licenses/by-nc/4.0/", "id": 1,
      "name": "Attribution-NonCommercial License"},
     {"url": "http://creativecommons.org/licenses/by-nc-sa/4.0/", "id": 2,
      "name": "Attribution-NonCommercial-ShareAlike License"},
     {"url": "http://creativecommons.org/licenses/by-nc-nd/4.0/", "id": 3,
      "name": "Attribution-NonCommercial-NoDerivatives License"},
     {"url": "http://creativecommons.org/licenses/by-nd/4.0/", "id": 4,
      "name": "Attribution-NoDerivatives License"},
     {"url": "http://creativecommons.org/licenses/by-sa/4.0/", "id": 5,
      "name": "Attribution-ShareAlike License"},
     {"url": "http://creativecommons.org/licenses/by/4.0/", "id": 6,
      "name": "Attribution License"},
     {"url": "http://creativecommons.org/publicdomain/zero/1.0/", "id": 7,
      "name": "Public Domain Dedication"},
     {"url": "http://en.wikipedia.org/wiki/Copyright", "id": 8,
      "name": "No known copyright restrictions"}]


op_file_name = 'bat_metadata.json'
version = '1.0'
base_id = '40268'  # bats
api_url = 'https://api.inaturalist.org/v1/taxa/'
taxa = []

# get taxa info
search_api(api_url, base_id, taxa)

# sort alphabetically
names = [tt['name'] for tt in taxa]
taxa_sorted = [taxa[tt] for tt in np.argsort(names)]

# add "bats" to the start of the list
url = api_url + base_id
response = urllib2.urlopen(url)
data = json.load(response)
res = get_info(data['results'][0])
taxa = [res] + taxa_sorted

# add "class id" to data
for ii, tt in enumerate(taxa):
    tt['id'] = ii + 1

# combine into single metadata file
meta_data = {}
meta_data['info'] = {'date_created':str(datetime.datetime.now()), 'version': version}
meta_data['licenses'] = licenses
meta_data['call_types'] = call_types
meta_data['taxa'] = taxa

with open(op_file_name, 'w') as da:
    json.dump(meta_data, da, indent=2)
