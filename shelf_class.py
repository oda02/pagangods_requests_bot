import shelve
from collections import deque
from Authorization import *
from threading import Thread

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

        with open('./accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    self.all_accs.update({line[0]: line[1]})

        with open('./normal_accs.txt', 'r') as fa:
            for line in fa:
                if line:
                    line = line.split()
                    self.normal_accs.update({line[0]: line[1]})


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
        thrd = Thread(target=self.tokens_get_first_time)
        thrd.start()
        # self.tokens_get_first_time()
        print(self.normal_accs)
        print(self.accounts_time['normal_accs'])


    def get_new_acc(self):
        cur_time = time.time()
        try:
            if cur_time - self.accounts_time['normal_accs'][0][1] > 0:
                acc_name = self.accounts_time['normal_accs'].popleft()[0]
                return (acc_name, self.get_token(acc_name), 'simple')
        except Exception as e:
            # print('asdasd', e)
            pass
        if cur_time - self.accounts_time['accs'][0][1] > 0:
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

        if time_p:
            acc_time = time_p
        else:
            acc_time = time.time() + 3600
        if account in self.normal_accs:
            self.accounts_time['normal_accs'].append([account, acc_time])
        else:
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
        self.tokens[account] = refresh_token(self.tokens[account]['refresh_token'])
        self.tokens.sync()
        return self.tokens[account]['access_token']
