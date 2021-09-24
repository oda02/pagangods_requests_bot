import shelve
import time

import requests
from Authorization import get_token_pair
import json


def get_current_expeditionId(token):
    r = requests.post('https://app.pagangods.io/api/v1/expeditions/list', headers={'Authorization': 'Bearer ' + token})
    if r.json()['data']:
        return r.json()['data'][0]
    return False


def complete_expedition(token, expeditionId, acc):
    r = requests.post('https://app.pagangods.io/api/v1/expeditions/complete_expedition',
                      headers={'Authorization': 'Bearer ' + token},
                      json={"expeditionId": expeditionId})
    if r.status_code == 403:
        print('banned')
    if r.json()['data']:
        if r.json()['data']['isSuccessful']:
            print(r.json()['data']['reward']['userSums'])
        if r.json()['data']['reward']['assets']:
            try:
                card_id = r.json()['data']['reward']['assets'][0]
                response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                                         headers={'Authorization': 'Bearer ' + token})
                units = json.loads(response.text)['data']
                for x in units:
                    if x['serverData']['id'] == card_id:
                        print(x['attributes']['name'])
            except:
                pass
    return False


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

    expeditionId = get_current_expeditionId(tokens['access_token'])
    expeditionId = expeditionId['expeditionId']
    complete_expedition(tokens['access_token'], expeditionId, acc)

    response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    units = json.loads(response.text)['data']
    cards = []
    for unit in units:
        if unit['attributes']['multiplier'] == 0.5:
            cards.append(unit['serverData']['id'])
    response = requests.post('https://app.pagangods.io/api/v1/teams/list',
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    team = 0
    data = response.json()['data']
    print(data)
    for x in data:
        team_id = x['teamId']
        team_name = x['name']
        response = requests.post('https://app.pagangods.io/api/v1/teams/set',
                                 json={'teamId': team_id, 'name': team_name, 'AssetIds': []},
                                 headers={'Authorization': 'Bearer ' + tokens['access_token']})
    for x in data:

        if x['name'] == "Team 1":
            team = x

    # team_id_xd = x['teamId']
    # team_nam_xd = x['name']
    # cards_xd = []
    # response = requests.post('https://app.pagangods.io/api/v1/teams/set',
    #                          json={'teamId': team_id_xd, 'name': team_nam_xd, 'AssetIds': cards_xd},
    #                          headers={'Authorization': 'Bearer ' + tokens['access_token']})
    # if response.status_code == 200:
    #     print('deleted')
    team_id = team['teamId']
    team_name = team['name']
    response = requests.post('https://app.pagangods.io/api/v1/teams/set',
                             json={'teamId': team_id, 'name': team_name, 'AssetIds': cards},
                             headers={'Authorization': 'Bearer ' + tokens['access_token']})
    if response.status_code == 200:
        # with open('./accs.txt', 'a') as fe:
        #     fe.write("\n" + acc + " " + new_accs[acc])
        with open('./new_accs.txt', 'r') as fe:
            lines = fe.readlines()
        # запишем файл построчно пропустив первую строку
        with open('./new_accs.txt', 'w') as fe:
            fe.writelines(lines[1:])
        print('Аккаунт ' + acc + ' успешно добавлен')
    else:
        print('Вышло недоразумение')
    # time.sleep(5)