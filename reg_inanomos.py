import imaplib as il
import email
import email.message
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--window-size=1600,900")
options.add_argument('headless')
import requests


class MailParser:
    def __init__(self, login, psw, receiver):
        self.mail = il.IMAP4_SSL("imap.gmail.com")
        self.mail.login(login, psw)

        self.receiver = receiver

    def get_email_code(self):

        while True:
            code = ''
            status, select_data = self.mail.select('INBOX')
            messages = select_data[0].decode('utf-8')
            status, search_data = self.mail.search(None, 'ALL')
            status, messages = self.mail.select("INBOX")
            messages = int(messages[0])

            # fetch the email message by ID
            res, msg = self.mail.fetch(str(messages), "(RFC822)")
            for response in msg:

                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    content_type = msg.get_content_type()
                    print(msg["Delivered-To"], "-")
                    if msg["Delivered-To"] == self.receiver:
                        if msg.is_multipart():
                            for payload in msg.get_payload():

                                text = payload.get_payload(decode=True).decode()


                                text = text[text.find('<a'):text.find('</a')]
                                text = text[text.find('"') + 1:]
                                text = text[:text.find('"')]
                                return text

    def unlog(self):
        pass


f = open('./mails_data.txt')
for line in f:
    if line:
        line = line.split()
        PASSWORD = line[1]
        USERNAME = line[0]


for i in range(23, 501):
    username_i = USERNAME + "+{}@gmail.com".format(i)
    print(username_i, "start")
    while True:
        response = requests.post("https://my.inanomo.com/api/v1/users", json={"password":PASSWORD,"email": username_i})
        if response.json()["data"]:
            break
        time.sleep(10)
    kok = MailParser("**", "**", username_i)
    href = kok.get_email_code()
    driver = uc.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
    driver.get(href)
    wait = WebDriverWait(driver, 30)

    button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Продолжить"]')))
    time.sleep(0.2)
    button.click()
    try:
        button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@name="submit"]')))
    except:
        button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Продолжить"]')))
        time.sleep(0.2)
        button.click()
        button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@name="submit"]')))
    button.click()
    time.sleep(5)
    fa = open('./new_accs.txt', "a")
    fa.write(username_i + " " + PASSWORD + "\n")
    print(username_i)
    driver.quit()
    fa.close()

