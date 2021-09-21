import requests
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GiveMeMoney:

    def __init__(self, wallet):
        self.wallet = wallet
        f = open('./accs_to_withraw.txt')
        self.accounts = {}
        for line in f:
            if line:
                line = line.split()
                self.accounts.update({line[0]: line[1]})
        f.close()
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("--window-size=1600,900")
        # options.add_argument('headless')
        self.driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=self.options)
        self.main_cycle()

    def main_cycle(self):
        for acc in self.accounts:
            self.driver.close()
            self.driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=self.options)
            self.driver.get('https://app.pagangods.io/signin?ReturnUrl=%2F')
            self.wait = WebDriverWait(self.driver, 10)
            button = self.wait_for_element('.//span[@class="inanomo"]')
            button.click()
            login = self.wait_for_element('.//input[@name="login"]')
            login.click()
            login.send_keys(acc)
            psw = self.driver.find_element_by_xpath('.//input[@name="password"]')
            psw.click()
            psw.send_keys(self.accounts[acc])
            self.driver.find_element_by_xpath('.//button').click()
            profile = self.wait_for_element('.//a[@class="top-panel__userpic"]')
            profile.click()
            fur = self.wait_for_element('.//span[@class="text-yellow"]')
            fur = fur.text.split('.')[0]
            print(fur)
            withdrawal = self.wait_for_element('.//button[text()="Вывести"]')
            withdrawal.click()
            input_field = self.wait_for_element('.//input')
            input_field.send_keys(fur)
            try:
                print('типа жду')
                withdrawal = self.wait_for_element(
                    './/button[@class="button button--large button--primary button--fw"]')
                withdrawal.click()
            except:
                print(acc, ' лошара и не может нажать на кнпоку "вывести"')
            try:
                success = self.wait_for_element('.//div[text()="Успешная транзакция"]')
            except:
                print(acc, ' лошара и не отдает баблишко')
            self.driver.get('https://wallet.inanomo.com/master-account/transfer')
            cur_button = self.wait_for_element('.//div[@data-currency="FUR"]')
            cur_button.click()
            form = self.wait_for_element('.//div[@class="ma-forms__inner"]')
            inputs = form.find_elements_by_xpath('.//input')
            inputs[0].click()
            inputs[0].send_keys(self.wallet)
            self.driver.find_element_by_xpath('.//span[@class="pseudo-link pseudo-link--blue"]').click()
            self.driver.find_element_by_xpath('.//button[text()="Перевести"]').click()
            time.sleep(5)

    def wait_for_element(self, element):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, element)))

    def test_cycle(self):
        self.driver.get('https://app.pagangods.io/signin?ReturnUrl=%2F')
        button = self.wait_for_element('.//span[@class="inanomo"]')
        button.click()
        login = self.wait_for_element('.//input[@name="login"]')
        login.click()
        login.send_keys('kosyankov01@gmail.com')
        psw = self.driver.find_element_by_xpath('.//input[@name="password"]')
        psw.click()
        psw.send_keys('Kos@inanomo-2001')
        self.driver.find_element_by_xpath('.//button').click()
        profile = self.wait_for_element('.//a[@class="top-panel__userpic"]')
        profile.click()
        fur = self.wait_for_element('.//span[@class="text-yellow"]')
        fur = fur.text.split('.')[0]
        print(fur)
        withdrawal = self.wait_for_element('.//button[text()="Вывести"]')
        withdrawal.click()
        input_field = self.wait_for_element('.//input')
        input_field.send_keys(10)
        try:
            print('типа жду')
            withdrawal = self.wait_for_element('.//button[@class="button button--large button--primary button--fw"]')
            withdrawal.click()
        except:
            pass
        try:
            success = self.wait_for_element('.//div[text()="Успешная транзакция"]')
        except:
            pass
        self.driver.get('https://wallet.inanomo.com/master-account/transfer')
        cur_button = self.wait_for_element('.//div[@data-currency="FUR"]')
        cur_button.click()
        form = self.wait_for_element('.//div[@class="ma-forms__inner"]')
        inputs = form.find_elements_by_xpath('.//input')
        inputs[0].click()
        inputs[0].send_keys(self.wallet)
        inputs[1].click()
        inputs[1].send_keys(10)
        self.driver.find_element_by_xpath('.//button[text()="Перевести"]').click()

if __name__ == '__main__':
    GiveMeMoney('101799670376')