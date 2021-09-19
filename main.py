import json
import shelve
from test import write_msg
import time

import requests

from shelf_class import shelf_class


def updater(shelf_class_p, window_p):
    while True:
        try:
            window_p['raids'].update(
                str(shelf_class_p.stat['successful']) + '/' + str(shelf_class_p.stat['all']) + '    ' +
                str(round(shelf_class_p.stat['successful'] / shelf_class_p.stat['all'] * 100, 2)) + "%")

            window_p['cards'].update(
                str(shelf_class_p.stat['cards']) + '/' + str(shelf_class_p.stat['successful']) + '    ' +
                str(round(shelf_class_p.stat['cards'] / shelf_class_p.stat['successful'] * 100, 2)) + "%")

            window_p['gold'].update(shelf_class_p.GOLD)
            if shelf_class_p.refresh_button_on:
                window['refresh_gold'].update(disabled=False)
        except:
            pass
        time.sleep(0.2)



class GamerBot:
    def __init__(self, shelf_class_p, useless_shit):
        self.shelf_class = shelf_class_p

        self.main_cycle()

    def main_cycle(self):
        while True:
            try:
                while True:
                    new_acc = self.shelf_class.get_new_acc()
                    if new_acc == False:

                        time.sleep(1)
                        continue
                    break
                acc_name = new_acc[0]
                token = new_acc[1]
                difficulty = new_acc[2]


                print(acc_name)
                expeditionId = self.get_current_expeditionId(token)
                if expeditionId:
                    if expeditionId['endUtc'] > time.time():
                        self.shelf_class.add_acc_timer(acc_name, expeditionId['endUtc']+1)
                        print('cd')
                        continue
                    else:
                        expeditionId = expeditionId['expeditionId']
                    self.complete_expedition(token, expeditionId, acc_name)
                teamId = self.get_teamsId(token)
                if self.start_expedition(token, teamId, difficulty) == None:
                    print('success')
                    self.shelf_class.add_acc_timer(acc_name, False)
                else:
                    print(token)

            except Exception as e:
                try:
                    self.shelf_class.add_acc_timer(acc_name, 0)
                except:
                    print('err')
                    pass
                print(e)
                pass

    def get_current_expeditionId(self, token):
        r = requests.post('https://app.pagangods.io/api/v1/expeditions/list', headers={'Authorization': 'Bearer ' + token})
        if r.json()['data']:
            return r.json()['data'][0]
        return False
    def complete_expedition(self, token, expeditionId, acc):
        r = requests.post('https://app.pagangods.io/api/v1/expeditions/complete_expedition',
                          headers={'Authorization': 'Bearer ' + token},
                          json={"expeditionId": expeditionId})
        if r.json()['data']:
            self.shelf_class.stat['all'] += 1
            if r.json()['data']['isSuccessful']:
                self.shelf_class.stat['successful'] += 1
                print(r.json()['data']['reward']['userSums'])
            if r.json()['data']['reward']['assets']:
                self.shelf_class.stat['cards'] += 1
                self.add_acc_to_file(acc)
                try:
                    card_id = r.json()['data']['reward']['assets'][0]
                    response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                                             headers={'Authorization': 'Bearer ' + token})
                    units = json.loads(response.text)['data']
                    for x in units:
                        if x['serverData']['id'] == card_id:
                            print(x['attributes']['name'])
                            write_msg(str(acc) + ' ' + str(x['attributes']['name']))
                except:
                    try:
                        write_msg(str(acc) + ' error ' + str(r.json()['data']['reward']['assets']))
                    except:
                        write_msg(str(acc) + ' error3228 ')
        self.shelf_class.stat.sync()
        return False
    def get_teamsId(self, token):
        r = requests.post('https://app.pagangods.io/api/v1/teams/list',
                          headers={'Authorization': 'Bearer ' + token})
        data = r.json()['data']
        for x in data:
            if x['name'] == "Team 1":
                return x['teamId']
        return False
    def start_expedition(self, token, teamId, difficulty):
        r = requests.post('https://app.pagangods.io/api/v1/expeditions/start',
                          headers={'Authorization': 'Bearer ' + token},
                          json={"teamId": teamId, "difficulty": difficulty})
        try:
            return r.json()['error']
        except:
            return False

    def add_acc_to_file(self, acc_p):
        accs = []

        with open('./cards_accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    accs.append(line)
        if acc_p not in accs:
            with open('./cards_accs.txt', 'a') as f:
                f.writelines(acc_p+'\n')



import threading
import PySimpleGUI as sg



shelf_class_ob = shelf_class()
layout = []
layout_line = [sg.Text("Your Gold:  "), sg.Text(size=(20,1), key='gold',visible=True), sg.Button('Refresh',key='refresh_gold', disabled=False)]
layout.append(layout_line)

layout_line = [sg.Text("                               STATS:           ")]
layout.append(layout_line)
layout_line = [sg.Text("Successful raids: "), sg.Text(size=(20,1), key='raids',visible=True)]
layout.append(layout_line)

layout_line = [sg.Text("Cards dropped:"), sg.Text(size=(20,1), key='cards',visible=True)]
layout.append(layout_line)
# Create the window
window = sg.Window('Window Title', layout, finalize=True)
threading.Thread(target=GamerBot, args=(shelf_class_ob, 1)).start()
threading.Thread(target=updater,
                         args=(shelf_class_ob, window)).start()
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    print(event)
    if event == 'refresh_gold':
        window['refresh_gold'].update(disabled=True)
        threading.Thread(target=shelf_class_ob.check_gold).start()





# Finish up by removing from the screen
window.close()



