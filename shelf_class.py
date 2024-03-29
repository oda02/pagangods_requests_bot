import decimal
import math
import os
import random
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
        self.GOLD = ' - '
        self.refresh_button_on = True
        self.CD = ""
        self.all_accs = {}
        self.accs_to_stop = []
        self.normal_accs = {}
        self.hard_accs = {}
        self.all_accs_gold = shelve.open('accounts_gold', writeback=True)
        self.tokens = shelve.open('tokens', writeback=True)
        self.stat = shelve.open('stat', writeback=True)
        try:
            self.stat['all']
        except:
            self.stat['all'] = 0
            self.stat['successful'] = 0
            self.stat['cards'] = 0
        self.stat.sync()
        # self.normal_accs_minute_limit = 0
        # self.last_minute = datetime.now().minute
        # self.accs_minute_limit = 0

        with open('./accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    self.all_accs.update({line[0]: line[1]})

        # self.accs_minute_limit = math.ceil(len(self.all_accs)/60 + 0.2)
        # self.accs_minute = 0
        with open('./normal_accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    self.normal_accs.update({line[0]: line[1]})
        try:
            with open('./accs_to_stop.txt', 'r') as fa:
                for line in fa:
                    if line:
                        line = line.split()
                        self.accs_to_stop.append(line[0])
        except:
            pass

        try:
            with open('./hard_accs.txt', 'r') as fa:
                for line in fa:
                    if line:
                        line = line.split()
                        self.hard_accs.update({line[0]: line[1]})
        except:
            pass
        # self.normal_accs_minute_limit = math.ceil(len(self.normal_accs) / 60)
        # self.normal_accs_minute = 0
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
            print(len(self.accounts_time['accs']))
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

        self.accounts_time['normal_accs'] = deque()
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


        for account in self.hard_accs:
            try:
                for acc in self.accounts_time['accs']:
                    if acc[0] == account:
                        print('yes')
                        self.accounts_time['accs'].remove(acc)
                        print('deleted ', account)
            except:
                pass
            flag = True
            for acc_time in self.accounts_time['hard_accs']:
                if account in acc_time[0]:
                    flag = False
            if flag:
                self.accounts_time['hard_accs'].appendleft([account, 0])

        self.tokens_get_first_time()
        # self.get_all_accs_with_new_cards()
        # input()
        # thrd = Thread(target=self.check_gold)
        # thrd.start()
        # print(self.normal_accs)
        # print(self.accounts_time['normal_accs'])
        # self.get_all_accs_with_new_cards()
        # input()

        for account in self.accs_to_stop:
            try:
                for acc in self.accounts_time['accs']:

                    if acc[0] == account:
                        self.accounts_time['accs'].remove(acc)
                        print('will stop ', account)
            except:
                pass
            try:
                for acc in self.accounts_time['normal_accs']:
                    if acc[0] == account:
                        self.accounts_time['normal_accs'].remove(acc)
                        print('will stop ', account)
            except:
                pass
            try:
                for acc in self.accounts_time['hard_accs']:
                    if acc[0] == account:
                        self.accounts_time['hard_accs'].remove(acc)
                        print('will stop ', account)
            except:
                pass



    def get_new_acc(self):
        # if 22 > datetime.now().hour > 7:
        #     return False
        cur_time = time.time()

        # if self.last_minute != datetime.now().minute:
        #     self.last_minute = datetime.now().minute
        #     self.normal_accs_minute = 0
        #     self.accs_minute = 0
        coooldown = 3600

        try:
            tm = cur_time - self.accounts_time['hard_accs'][0][1]
            if tm > 0:
                # if self.normal_accs_minute < self.normal_accs_minute_limit:
                acc_name = self.accounts_time['hard_accs'].popleft()[0]
                self.CD =""
                return (acc_name, self.get_token(acc_name), 'normal')
            else:
                coooldown = -tm
        except Exception as e:
            # print('asdasd', e)
            pass

        try:
            tm = cur_time - self.accounts_time['normal_accs'][0][1]
            if tm > 0:
                # if self.normal_accs_minute < self.normal_accs_minute_limit:
                self.CD = ""
                acc_name = self.accounts_time['normal_accs'].popleft()[0]
                return (acc_name, self.get_token(acc_name), 'simple')
            else:
                if coooldown > -tm:
                    coooldown = -tm
        except Exception as e:
            # print('asdasd', e)
            pass
        tm = cur_time - self.accounts_time['accs'][0][1]
        if tm > 0:
            # if self.accs_minute < self.accs_minute_limit:
            self.CD = ""
            acc_name = self.accounts_time['accs'].popleft()[0]
            return (acc_name, self.get_token(acc_name), 'easy')
        # print(cur_time - self.accounts_time['accs'][0][1])
        else:
            if coooldown > -tm:
                coooldown = -tm
        self.CD = "cooldown - " + str(round(coooldown, 2)) + " s"
        return False

    def add_acc_timer(self, account, time_p, banned):
        if banned:
            return
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
        # flag = True
        appended_time = random.randint(15, 1200)
        appended_time = 5
        if time_p:
            acc_time = time_p + appended_time
            # flag = False
        else:
            acc_time = time.time() + 3600 + appended_time
        if account in self.normal_accs:
            i = 0
            for acc in self.accounts_time['normal_accs']:
                if acc[1] > acc_time:
                    self.accounts_time['normal_accs'].insert(i, [account, acc_time])
                    break
                i += 1
            else:
                self.accounts_time['normal_accs'].insert(i, [account, acc_time])

        elif account in self.hard_accs:
            i = 0
            for acc in self.accounts_time['hard_accs']:
                if acc[1] > acc_time:
                    self.accounts_time['hard_accs'].insert(i, [account, acc_time])
                    break
                i += 1
            else:
                self.accounts_time['hard_accs'].insert(i, [account, acc_time])
        elif account in self.all_accs:
            i = 0
            for acc in self.accounts_time['accs']:
                if acc[1] > acc_time:
                    self.accounts_time['accs'].insert(i, [account, acc_time])
                    break
                i += 1
            else:
                self.accounts_time['accs'].insert(i, [account, acc_time])

        self.accounts_time.sync()

    def tokens_get_first_time(self):
        for account in self.normal_accs:
            try:
                self.tokens[account]
            except:
                self.tokens[account] = get_token_pair(account, self.normal_accs[account])
                self.tokens.sync()

        for account in self.hard_accs:
            try:
                self.tokens[account]
            except:
                self.tokens[account] = get_token_pair(account, self.hard_accs[account])
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
                    try:
                        passw = self.normal_accs[account]
                    except:
                        passw = self.hard_accs[account]
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
        self.refresh_button_on = False
        GOLD = 0
        try:
            all_accounts = []

            for acc in self.hard_accs:
                all_accounts.append(acc)
            for acc in self.normal_accs:
                all_accounts.append(acc)
            for acc in self.all_accs:
                all_accounts.append(acc)
            i = 0
            for acc in all_accounts:
                flag = True
                try:
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
                    i+=1
                    self.GOLD = str(i) + '/' + str(len(all_accounts)) + '    ' + str(round(i/len(all_accounts)*100, 2)) + "%"
                    flag = False
                except:
                    if flag:
                        all_accounts.append(acc)

            n = decimal.Decimal(int(GOLD))
            self.GOLD = ('{0:,}'.format(n).replace(',', ' '))
        except Exception as e:
            self.GOLD = e
            pass
        self.refresh_button_on = True

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

# shelf_class()