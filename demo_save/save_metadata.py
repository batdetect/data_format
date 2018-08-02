"""
This script loads in a csv file with audio meta data and saves the contents to a
json file.
"""

import json
import pandas as pd
import sys

ip_file = sys.argv[1]

required_fields = ['file_name', 'time_expansion_factor', 'year', 'month', 'day',
                   'hour', 'minute', 'second', 'lat', 'long', 'duration',
                   'sampling_rate', 'license', 'rights_holder_name', 'notes',
                   'taxon']
df = pd.read_csv(ip_file)

if len(list(set(required_fields) - set(df.columns.tolist()))) != 0:
    print('Not all of the required fields are present.')
    print('Missing:', list(set(required_fields) - set(df.columns.tolist())))
    sys.exit()

# creating output list by looping through each row in the csv file
print(str(df.shape[0]) + ' audio files listed.')
audio_files = []
for index, row in df.iterrows():
    aud = {}
    aud['id'] = int(index)+1
    aud['file_name'] = row['file_name']
    aud['sampling_rate'] = row['sampling_rate']
    aud['time_expansion_factor'] = int(row['time_expansion_factor'])
    date_str = '-'.join([str(row['year']), str(row['month']).zfill(2), str(row['day']).zfill(2)]) + \
         ' ' + ':'.join([str(row['hour']).zfill(2), str(row['minute']).zfill(2), str(row['second']).zfill(2)])
    aud['date_recorded'] = date_str
    aud['duration'] = row['duration']
    aud['lat'] = row['lat']
    aud['long'] = row['long']
    aud['license'] = int(row['license'])
    aud['rights_holder_name'] = row['rights_holder_name']
    if row['notes'] != row['notes']:  # check for empty string
        aud['notes'] = ""
    else:
        aud['notes'] = row['notes']
    aud['taxon'] = int(row['taxon'])
    aud['exhaustively_annotated'] = False
    audio_files.append(aud)

# save the data to a json file
print('Saving output as: ' + ip_file[:-3] + 'json')
with open(ip_file[:-3] + 'json', 'w') as da:
    json.dump({'audio_files': audio_files}, da, indent=2)
