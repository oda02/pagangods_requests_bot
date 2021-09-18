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

    response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    units = json.loads(response.text)['data']
    cards = []
    for unit in units:
        cards.append(unit['serverData']['id'])
    response = requests.post('https://app.pagangods.io/api/v1/teams/list',
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    teams = json.loads(response.text)['data']
    team_id = teams[0]['teamId']
    team_name = teams[0]['name']
    response = requests.post('https://app.pagangods.io/api/v1/teams/set',
                             json={'teamId': team_id, 'name': team_name, 'AssetIds': cards},
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    if response.status_code == 200:
        with open('./accs.txt', 'a') as fe:
            fe.write("\n" + acc + " " + new_accs[acc])
        with open('./new_accs.txt', 'r') as fe:
            lines = fe.readlines()
        # запишем файл построчно пропустив первую строку
        with open('./new_accs.txt', 'w') as fe:
            fe.writelines(lines[1:])
        print('Аккаунт ' + acc + ' успешно добавлен')
    else:
        print('Вышло недоразумение')
    time.sleep(5)
