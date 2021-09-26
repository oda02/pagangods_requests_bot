import time
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



f = open('./mails_data.txt')
i = 0
for line in f:
    if line:
        line = line.split()
        if i == 0:
            PASSWORD = line[1]
            USERNAME = line[0]
        else:
            server197_PASSWORD = line[1]
            server197_USERNAME = line[0]
        i+=1
f.close()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--window-size=1600,900")
options.add_argument('headless')
driver = uc.Chrome(executable_path='./chromedriver.exe',chrome_options=options)
f = open('./banned_accs.txt')
accounts = {}
for line in f:
    if line:
        line = line.split()
        accounts.update({line[0]: line[1]})
f.close()
for acc in accounts:
    driver.get("https://server197.hosting.reg.ru:1500/ispmgr#/list/email/2?p_num=1")
    time.sleep(1)
    username_input = driver.find_element_by_xpath('//input[@name="username"]')
    password_input = driver.find_element_by_xpath('//input[@name="password"]')
    username_input.click()
    username_input.send_keys(server197_USERNAME)
    password_input.click()
    password_input.send_keys(server197_PASSWORD)
    driver.find_element_by_xpath('//button[text()="Войти"]').click()
    driver.get("https://server197.hosting.reg.ru:1500/ispmgr#/list/email/3?p_num=1")
    wait = WebDriverWait(driver, 800)
    actionChains = ActionChains(driver)
    wait.until(EC.presence_of_element_located((By.XPATH, './/input[@placeholder="Ctrl + Shift + F"]')))
    print(acc)
    searcher = driver.find_element_by_xpath('.//input[@placeholder="Ctrl + Shift + F"]')
    searcher.send_keys(acc)
    acc_el = wait.until(EC.presence_of_element_located((By.XPATH, '(.//mark)[2]')))
    actionChains.double_click(acc_el).perform()
    ok = wait.until(EC.presence_of_element_located((By.XPATH, './/button[text()="    Ok    "]')))
    ok.click()
    with open('./banned_accs.txt', 'r') as fe:
        lines = fe.readlines()
    with open('./banned_accs.txt', 'w') as fe:
        fe.writelines(lines[1:])
    with open('./deleted.txt', 'a') as fe:
        fe.writelines(lines[0])
    driver.quit()
    driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
    print('Аккаунт ' + acc + ' успешно добавлен')
