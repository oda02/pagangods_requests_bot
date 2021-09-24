import time
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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

banned_accounts = {}
f = open('./banned_accs.txt')
for line in f:
    if line:
        line = line.split()
        banned_accounts.update({line[0]: line[1]})
f.close()

deleted_mails = {}
f = open('./deleted_mails.txt')
for line in f:
    if line:
        line = line.split()
        deleted_mails.update({line[0]: line[1]})
f.close()



options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--window-size=1600,450000")

driver = uc.Chrome(executable_path='./chromedriver.exe',chrome_options=options)
driver.get("https://server197.hosting.reg.ru:1500/ispmgr#/list/email/3?p_num=1")



username_input = driver.find_element_by_xpath('//input[@name="username"]')
password_input = driver.find_element_by_xpath('//input[@name="password"]')
username_input.click()
username_input.send_keys(server197_USERNAME)
password_input.click()
password_input.send_keys(server197_PASSWORD)

driver.find_element_by_xpath('//button[text()="Войти"]').click()

driver.get("https://server197.hosting.reg.ru:1500/ispmgr#/list/email/2?p_num=1")
time.sleep(1)
wait = WebDriverWait(driver, 800)


for acc in banned_accounts:
    if acc not in deleted_mails:
        el = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="' + acc + '"]')))
        print('нашел')
        el.click()
        input()

        driver.find_elements_by_xpath('//button[@aria-description="Создать"]')[1].click()
        username =wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="name"]')))
        username.click()
        username.send_keys(USERNAME+ str(i))

        passwd = driver.find_element_by_xpath('//input[@name="passwd"]')
        passwd.click()
        passwd.send_keys(PASSWORD)

        confirm = driver.find_element_by_xpath('//input[@name="confirm"]')
        confirm.click()
        confirm.send_keys(PASSWORD)


        driver.find_element_by_xpath('//button[text()]').click()

        f = open('./mails.txt', "a")
        f.write(USERNAME + str(i) + "@monkos.ru " + PASSWORD + "\n")
        f.close()
        time.sleep(1)


driver.close()
