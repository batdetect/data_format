import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')

with open('bat_metadata.json') as da:
    data = json.load(da)


taxa = data['taxa']

print('# List of Bats - Version ' + data['info']['version'])
print('| id  | name | common name | rank |')
print('| :-- | :--- | :---------- | :--- |')

for tt in taxa:
    if tt['wikipedia_url'] is not None:
        print('|' + str(tt['id']) + ' | ' + tt['name'] + ' | [' + tt['preferred_common_name']  + '](' + str(tt['wikipedia_url']) + ') | ' + tt['rank'] + ' |')
    else:
        print('|' + str(tt['id']) + ' | ' + tt['name'] + ' | ' + tt['preferred_common_name']  + ' | ' + tt['rank'] + ' |')
