import shelve
import time

import requests
from Authorization import get_token_pair
import json

new_accs = {}
with open('./new_accs.txt', 'r') as fa:
    for line in fa:
        if line:
            line = line.split()
            new_accs[line[0]] = line[1]

tokens_p = shelve.open('tokens', writeback=True)
for acc in new_accs:
    tokens = get_token_pair(acc, new_accs[acc])
    tokens_p[acc] = tokens

    response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    units = json.loads(response.text)['data']
    for x in units:
        if x['serverData']['id'] == '2581bf8d-b970-471a-a57e-cbeccd84dffa':
            print(x['attributes']['name'])
    print(units)
    input()