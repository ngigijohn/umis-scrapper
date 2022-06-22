import os
from time import sleep
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


load_dotenv()


class MyBot():
    def __init__(self) -> None:

        self.service = Service('./chromedriver')
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(
            service=self.service, options=self.options)

    def login(self):
        delay = 5  # seconds
        self.driver.get(
            'https://registration.ueab.ac.ke/ueab/a_students.jsp?view=1:0')
        try:
            wait_for_username_field = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.ID, 'j_username')))
            form_username_field = self.driver.find_element(By.ID, 'j_username')
            form_password_field = self.driver.find_element(By.ID, 'j_password')

            # print("Page is ready!")
            self.driver.get_screenshot_as_file('login_page.png')

            form_username_field.send_keys(os.environ.get('STUDENT_ID'))
            form_password_field.send_keys(os.environ.get('PASSWORD'))

            # wait until submit button is clickable
            #
            WebDriverWait(self.driver, delay).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="count-down-part"]/div/div/div/div/div[2]/form/div[6]/button'))).click()

            # wait for login
            sleep(5)
            self.driver.get_screenshot_as_file('user_page.png')

            # TODO
            # verify login success

        except TimeoutException:
            print("Loading took too much time!")


scrapper = MyBot()

scrapper.login()
