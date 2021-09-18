import math
import os
import shelve
from collections import deque
from Authorization import *
from threading import Thread
from datetime import datetime
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class shelf_class():
    def __init__(self):

        self.all_accs = {}
        self.normal_accs = {}
        self.all_accs_gold = shelve.open('accounts_gold', writeback=True)
        self.tokens = shelve.open('tokens', writeback=True)
        self.normal_accs_minute_limit = 0
        self.last_minute = datetime.now().minute
        self.accs_minute_limit = 0

        with open('./accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    self.all_accs.update({line[0]: line[1]})

        self.accs_minute_limit = math.ceil(len(self.all_accs)/60 + 0.2)
        self.accs_minute = 0
        with open('./normal_accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    self.normal_accs.update({line[0]: line[1]})
        self.normal_accs_minute_limit = math.ceil(len(self.normal_accs) / 60)
        self.normal_accs_minute = 0
        # with open('./new_accs.txt', 'r') as fa:
        #     for line in fa:
        #         if line:
        #             line = line.split()
        #             self.new_accounts.update({line[0]: line[1]})
        #             self.new_accounts_copy.update({line[0]: line[1]})
        #             self.all_accs.update({line[0]: line[1]})



        for account in self.all_accs:
            flag = True
            if account in self.all_accs_gold:
                flag = False
            if flag:
                self.all_accs_gold[account] = 0


        try:
            self.accounts_time = shelve.open('accounts_time', writeback=True)
        except Exception as e:
            print(e)
        try:
            k =self.accounts_time['accs']
            k =self.accounts_time['normal_accs']
        except:
            self.accounts_time['accs'] = deque()
            self.accounts_time['normal_accs'] = deque()
        #print(self.accounts_time['accs'])
        for account in self.all_accs:
            flag = True
            for acc_time in self.accounts_time['accs']:
                if account in acc_time[0]:
                    flag = False
            if flag:
                self.accounts_time['accs'].appendleft([account, 0])


        for account in self.normal_accs:
            try:
                for acc in self.accounts_time['accs']:
                    if acc[0] == account:
                        print('yes')
                        self.accounts_time['accs'].remove(acc)
                        print('deleted ', account)
            except:
                pass
            flag = True
            for acc_time in self.accounts_time['normal_accs']:
                if account in acc_time[0]:
                    flag = False
            if flag:
                self.accounts_time['normal_accs'].appendleft([account, 0])
        self.tokens_get_first_time()
        # self.get_all_accs_with_new_cards()
        # input()
        # thrd = Thread(target=self.check_gold)
        # thrd.start()
        print(self.normal_accs)
        print(self.accounts_time['normal_accs'])


    def get_new_acc(self):
        cur_time = time.time()

        if self.last_minute != datetime.now().minute:
            self.last_minute = datetime.now().minute
            self.normal_accs_minute = 0
            self.accs_minute = 0
        try:
            if cur_time - self.accounts_time['normal_accs'][0][1] > 0:
                if self.normal_accs_minute < self.normal_accs_minute_limit:
                    acc_name = self.accounts_time['normal_accs'].popleft()[0]
                    return (acc_name, self.get_token(acc_name), 'simple')
        except Exception as e:
            # print('asdasd', e)
            pass
        if cur_time - self.accounts_time['accs'][0][1] > 0:
            if self.accs_minute < self.accs_minute_limit:
                acc_name = self.accounts_time['accs'].popleft()[0]
                return (acc_name, self.get_token(acc_name), 'easy')
        # print(cur_time - self.accounts_time['accs'][0][1])
        return False

    def add_acc_timer(self, account, time_p):
        # if account in self.new_accounts_copy:
        #     print('add_to_file')
        #     self.new_accounts_copy.pop(account)
        #     with open('./accs.txt', 'a') as fe:
        #         fe.write("\n" + account + " " + self.all_accs[account])
        #     with open('./new_accs.txt', 'r') as fe:
        #         lines = fe.readlines()
        #
        #     # запишем файл построчно пропустив первую строку
        #     with open('./new_accs.txt', 'w') as fe:
        #         fe.writelines(lines[1:])
        flag = True
        if time_p:
            acc_time = time_p
            flag = False
        else:
            acc_time = time.time() + 3600+5
        if account in self.normal_accs:
            if flag:
                self.normal_accs_minute += 1
            self.accounts_time['normal_accs'].append([account, acc_time])
        else:
            if flag:
                self.accs_minute += 1
            self.accounts_time['accs'].append([account, acc_time])
        self.accounts_time.sync()

    def tokens_get_first_time(self):
        for account in self.normal_accs:
            try:
                self.tokens[account]
            except:
                self.tokens[account] = get_token_pair(account, self.normal_accs[account])
                self.tokens.sync()

        for account in self.all_accs:
            try:
                self.tokens[account]
            except:
                self.tokens[account] = get_token_pair(account, self.all_accs[account])
                self.tokens.sync()

    def get_token(self, account):
        if self.tokens[account]['expires_time'] + 60 < time.time():
            try:
                self.tokens[account] = refresh_token(self.tokens[account]['refresh_token'])
            except:
                try:
                    passw = self.all_accs[account]
                except:
                    passw = self.normal_accs[account]
        #
                self.tokens[account] = get_token_pair(account, passw)
        else:
            token = self.tokens[account]['access_token']

        # try:
        #     passw = self.all_accs[account]
        # except:
        #     passw = self.normal_accs[account]
        #
        # self.tokens[account] = get_token_pair(account, passw)
        self.tokens.sync()
        return self.tokens[account]['access_token']

    def check_gold(self):
        while True:
            GOLD = 0
            try:
                for acc in self.normal_accs:
                    if self.tokens[acc]['expires_time'] < time.time():
                        token = self.get_token(acc)
                    else:
                        token =self.tokens[acc]['access_token']
                    r = requests.post('https://app.pagangods.io/api/v1/users/list-my-sums',
                                      headers={'Authorization': 'Bearer ' + token})

                    data = r.json()['data']
                    if data:
                        for x in data:
                            if x['currency'] == 'FUR':
                                GOLD += float(x['sum'])

                for acc in self.all_accs:
                    if self.tokens[acc]['expires_time'] < time.time():
                        token = self.get_token(acc)
                    else:
                        token =self.tokens[acc]['access_token']
                    r = requests.post('https://app.pagangods.io/api/v1/users/list-my-sums',
                                      headers={'Authorization': 'Bearer ' + token})
                    data = r.json()['data']
                    if data:
                        for x in data:
                            if x['currency'] == 'FUR':
                                GOLD += float(x['sum'])
                os.system('cls||clear')
                print('GOLD = ', GOLD)
                time.sleep(3600)
            except Exception as e:
                print(e)
                pass

    def get_all_accs_with_new_cards(self):



        for acc in self.all_accs:
            token = self.get_token(acc)
            response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                                     headers={'Authorization': 'Bearer ' + token})
            data = response.json()['data']
            for x in data:
                if x['lockReason'] == None and x['attributes']['multiplier'] == 1:
                    print(acc)

        for acc in self.normal_accs:
            if self.tokens[acc]['expires_time'] < time.time():
                token = self.get_token(acc)
            else:
                token = self.tokens[acc]['access_token']
            response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                                     headers={'Authorization': 'Bearer ' + token})
            data = response.json()['data']
            for x in data:
                if x['lockReason'] == None and x['attributes']['multiplier'] == 1:
                    print(acc)

shelf_class()