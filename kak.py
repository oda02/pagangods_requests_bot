import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def import_cards():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--window-size=1600,900")
    driver = uc.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    with open('./wax_data.txt', 'r') as fa:
        lines = fa.readlines()
    LOGIN = lines[0].split()[0]
    PASSWORD = lines[1].split()[0]


    accs = []
    with open('./cards_accs.txt', 'r') as fa:
        for line in fa:
            if line:
                line = line.split()
                accs.append(line[0])

    print(accs)
    accs_data = {}
    with open('./accs.txt', 'r') as fa:
        for line in fa:
            if line:
                line = line.split()
                accs_data.update({line[0]: line[1]})


    with open('./normal_accs.txt', 'r') as fa:
        for line in fa:
            if line:
                line = line.split()
                accs_data.update({line[0]: line[1]})

    print(accs_data)
    for account in accs:
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
                password_input.send_keys(accs_data[account])
                driver.find_element_by_xpath('//button[@name="submit"]').click()

                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='card']")))

                cards = driver.find_elements_by_xpath("//div[@class='card']")
                for card in cards:
                    try:
                        ll = card.find_element_by_xpath(".//div[@class='hero-image__overlay']")
                    except:

                        card.find_element_by_xpath(".//div[@class='card__name']").click()
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
                driver.find_element_by_xpath('//button[text()="Перенести в WAX"]').click()
                time.sleep(1)
                with open('./cards_accs.txt', 'r') as fe:
                    lines = fe.readlines()
                # запишем файл построчно пропустив первую строку
                with open('./cards_accs.txt', 'w') as fe:
                    fe.writelines(lines[1:])
                all_flag = False
            except Exception as e:
                print(e)
                driver.quit()
                driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
        driver.close()
    driver.quit()


import_cards()