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
        self.delay = 5  # seconds

        self.logged_in = False

    def __export__(self, view, file_type):
        url = f'https://registration.ueab.ac.ke/ueab/grid_export?view={view}'

        print('exporting as ' + file_type)
        if file_type == 'pdf':
            self.driver.get(f'{url}&action={file_type}_export')
        elif file_type == 'csv':
            # csv doesn't specify file type in url
            self.driver.get(f'{url}&action=export')
        elif file_type == 'excel':
            self.driver.get(f'{url}&action={file_type}_export')
        else:
            print('File type not supported')

    def __confirm_login__(self):
        if self.logged_in:
            return True
        else:
            self.login()
            return True

    def get_login_credentials(self):
        login_credentials = {
            'STUDENT_ID': os.environ.get('STUDENT_ID'),
            'PASSWORD': os.environ.get('PASSWORD')
        }
        return login_credentials

    def login(self):
        login_credentials = self.get_login_credentials()

        self.driver.get(
            'https://registration.ueab.ac.ke/ueab/a_students.jsp?view=1:0')
        try:
            wait_for_username_field = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.ID, 'j_username')))
            form_username_field = self.driver.find_element(By.ID, 'j_username')
            form_password_field = self.driver.find_element(By.ID, 'j_password')

            # print("Page is ready!")
            self.driver.get_screenshot_as_file('login_page.png')
            form_username_field.send_keys(login_credentials['STUDENT_ID'])

            form_password_field.send_keys(login_credentials['PASSWORD'])

            # wait until submit button is clickable
            #
            WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="count-down-part"]/div/div/div/div/div[2]/form/div[6]/button'))).click()

            # wait for login
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div')))
            self.driver.get_screenshot_as_file('login_success.png')

            # verify login success
            if self.driver.current_url == 'https://registration.ueab.ac.ke/ueab/j_security_check':
                print('Login failed')
                self.logged_in = False

            else:
                self.driver.get_screenshot_as_file('user_page.png')
                print('Logged in')
                self.logged_in = True

        except TimeoutException:
            print("Loading took too much time!")

    def get_finance_statement(self, file_type='png'):
        # only png screenshot is supported
        if self.__confirm_login__():
            self.driver.get(
                'https://registration.ueab.ac.ke/ueab/a_statement.jsp?view=22:0')
            # implicitly wait for table to load
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[2]/div/div/table')))
            self.driver.get_screenshot_as_file('finance_statement.png')

    def get_student_details(self, file_type='png'):
        if self.__confirm_login__():
            url = "https://registration.ueab.ac.ke/ueab/a_students.jsp?view=2:0"
            view = "2:0"
            self.driver.get(url)

            # implicitly wait for table to load
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="portletBody"]/div/table/tbody')))
            if file_type == 'png':
                self.driver.get_screenshot_as_file('student_details.png')

            else:
                self.__export__(view, file_type)

    def get_student_courses(self, file_type='png'):
        pass

    def get_selected_time_table(self, file_type='png'):
        if self.__confirm_login__():
            url = 'https://registration.ueab.ac.ke/ueab/a_students.jsp?view=28:0'
            view = '28:0'
            self.driver.get(url)
            # implicitly wait for table to load
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="portletBody"]')))
            if file_type == 'png':
                self.driver.get_screenshot_as_file('selected_time_table.png')
            else:
                self.__export__(view, file_type)


scrapper = MyBot()

# scrapper.login()
scrapper.get_student_details('csv')
