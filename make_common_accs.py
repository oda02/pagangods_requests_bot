import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def export_cards():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--window-size=1600,900")
    driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
    with open('./wax_data.txt', 'r') as fa:
        lines = fa.readlines()
    LOGIN = lines[0].split()[0]
    PASSWORD = lines[1].split()[0]


    accs = {}
    with open('./accs.txt', 'r') as fa:
        for line in fa:
            if line:
                line = line.split()
                accs.update({line[0]: line[1]})

    common_accs = {}
    with open('./common_accs.txt', 'r') as fa:
        for line in fa:
            if line:
                line = line.split()
                common_accs.update({line[0]: line[1]})

    stop_this = False
    for account in accs:
        if stop_this:
            break
        if account in common_accs:
            continue
        all_flag = True
        while all_flag:
            try:
                driver.get("https://app.pagangods.io/")
                time.sleep(1)
                wait = WebDriverWait(driver, 30)
                button_login = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='inanomo']")))
                button_login.click()
                wait = WebDriverWait(driver, 10)
                username_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="login"]')))
                password_input = driver.find_element_by_xpath('//input[@name="password"]')
                username_input.click()
                username_input.send_keys(account)
                password_input.click()
                print(account)
                password_input.send_keys(accs[account])
                driver.find_element_by_xpath('//button[@name="submit"]').click()


                mainwindow = driver.current_window_handle
                button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Войти в WAX']")))
                button.click()

                flag = True
                while flag:
                    windows = driver.window_handles
                    for window in windows:
                        driver.switch_to.window(window)
                        element = driver.find_elements_by_xpath('//*[@name="userName"]')
                        time.sleep(0.2)
                        if element:
                            element[0].click()
                            element[0].clear()
                            element[0].send_keys(LOGIN)
                            element2 = driver.find_elements_by_xpath('//*[@name="password"]')
                            element2[0].click()
                            element2[0].clear()
                            element2[0].send_keys(PASSWORD)
                            time.sleep(0.5)
                            element = driver.find_elements_by_xpath('//button[text()="Login"]')
                            element[0].click()
                            #
                            flag = False
                            break
                        time.sleep(0.5)

                while True:
                    windows = driver.window_handles
                    if len(windows) == 1:
                        break
                driver.switch_to.window(mainwindow)
                time.sleep(1)

                wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()="WAX"]'))).click()
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='card']")))

                cards = driver.find_elements_by_xpath("//div[@class='card']")
                i = 0
                for card in cards:
                    try:
                        if i >=5:
                            break
                        if int(card.find_element_by_xpath(".//div[text()='Сила']/../div[2]").text) < 2000:
                            driver.execute_script("arguments[0].scrollIntoView();", card)
                            card.click()
                            i+=1
                        # card.find_element_by_xpath(".//div[@class='card__name']").click()
                        # ll = card.find_element_by_xpath(".//div[@class='hero-image__overlay']")
                    except Exception as e:
                        print(e)
                        # card.find_element_by_xpath(".//div[@class='card__name']").click()
                if i < 5:
                    stop_this = True
                    all_flag = False
                    break
                lalkok = driver.find_element_by_xpath('//button[text()="Перенести в игру"]')
                main_window = driver.current_window_handle
                while True:
                    try:
                        lalkok.click()
                        time.sleep(1)
                        if not lalkok.is_enabled():
                            break
                        time.sleep(5)
                        for window in driver.window_handles:
                            if window != main_window:
                                driver.switch_to.window(window)
                                driver.close()
                        driver.switch_to.window(mainwindow)
                    except:
                        pass
                with open('./common_accs.txt', 'a') as fe:
                    fe.write(account + " " + accs[account] + "\n")
                all_flag = False
            except Exception as e:
                print(e)
                driver.quit()
                driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
        print('закрываемчся')
        driver.quit()
        driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
    driver.quit()

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



def set_cards():
    new_accs = {}
    with open('./common_accs.txt', 'r') as fa:
        for line in fa:
            if line:
                line = line.split()
                try:
                    if line[2] == '+':
                        continue
                except:
                    pass
                new_accs[line[0]] = line[1]

    tokens_p = shelve.open('tokens', writeback=True)
    for acc in new_accs:
        tokens = get_token_pair(acc, new_accs[acc])
        tokens_p[acc] = tokens

        expeditionId = get_current_expeditionId(tokens['access_token'])
        if expeditionId:
            expeditionId = expeditionId['expeditionId']
            complete_expedition(tokens['access_token'], expeditionId, acc)

        response = requests.post('https://app.pagangods.io/api/v1/assets/list-server',
                                 headers={'Authorization': 'Bearer ' + tokens['access_token']})
        units = json.loads(response.text)['data']
        cards = []
        for unit in units:
            if unit['attributes']['multiplier'] == 1:
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
        if len(cards) == 5:
            if response.status_code == 200:

                f = open('./common_accs.txt').read()

                new_lines = f.replace(acc + ' ' + new_accs[acc] + '\n', acc + ' ' + new_accs[acc] + ' +\n')
                print('Аккаунт ' + acc + ' успешно добавлен')
                with open('./common_accs.txt', 'w') as F:
                    F.writelines(new_lines)
            else:
                print('Вышло недоразумение')
        else:
            print('карточки еще не дошли')
        # time.sleep(5)

# export_cards()
set_cards()