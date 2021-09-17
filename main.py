
import time

import requests

from shelf_class import shelf_class




class GamerBot:
    def __init__(self, shelf_class_p):
        self.shelf_class = shelf_class_p
        self.main_cycle()


    def main_cycle(self):
        while True:
            try:
                while True:
                    new_acc = self.shelf_class.get_new_acc()
                    if new_acc == False:

                        time.sleep(0.5)
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
                    self.complete_expedition(token, expeditionId)
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
    def complete_expedition(self, token, expeditionId):
        r = requests.post('https://app.pagangods.io/api/v1/expeditions/complete_expedition',
                          headers={'Authorization': 'Bearer ' + token},
                          json={"expeditionId": expeditionId})
        if r.json()['data']:
            if r.json()['data']['isSuccessful']:
                print(r.json()['data']['reward'])
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



shelf_class_ob = shelf_class()

GamerBot(shelf_class_ob)