import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from view_map import VIEW_MAP

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

    def __export__(self, view_index, file_type):
        url = f'https://registration.ueab.ac.ke/ueab/grid_export?view={view_index}'

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
            # wait for page to load completely
            WebDriverWait(self.driver, self.delay).until(
                lambda driver:
                self.driver.execute_script(
                    'return document.readyState') == 'complete')
            form_username_field = self.driver.find_element(By.ID, 'j_username')
            form_password_field = self.driver.find_element(By.ID, 'j_password')

            # Enter login_credentials
            form_username_field.send_keys(login_credentials['STUDENT_ID'])
            form_password_field.send_keys(login_credentials['PASSWORD'])

            # wait until submit button is clickable and click it
            WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="count-down-part"]/div/div/div/div/div[2]/form/div[6]/button'))).click()

            # wait for login page to load completely
            WebDriverWait(self.driver, self.delay).until(
                lambda driver:
                self.driver.execute_script(
                    'return document.readyState') == 'complete')
            self.driver.get_screenshot_as_file('login_success.png')

            if self.driver.current_url == 'https://registration.ueab.ac.ke/ueab/a_students.jsp?view=1:0':
                self.logged_in = True
                print('Login successful')
                self.driver.get_screenshot_as_file(
                    './screenshots/login_success.png')

            # verify login success
            elif self.driver.current_url == 'https://registration.ueab.ac.ke/ueab/j_security_check':
                print('Login failed:   wrong credentials')
                self.logged_in = False

            else:
                print('Login failed: unknown error')

        except TimeoutException:
            print("Loading took too much time!")

    def get_view_data(self, account_type='a_students', view='dashboard', file_type='png'):
        view_index = VIEW_MAP[view]
        if self.__confirm_login__():
            url = f'https://registration.ueab.ac.ke/ueab/{account_type}.jsp?view={view_index}'
            self.driver.get(url)
            # wait for page to load completely
            WebDriverWait(self.driver, self.delay).until(
                lambda driver:
                self.driver.execute_script(
                    'return document.readyState') == 'complete')
            if file_type == 'png':
                self.driver.get_screenshot_as_file(
                    f'./screenshots/{view}.png')
            else:
                self.__export__(view_index, file_type)


scrapper = MyBot()

# available views ['schools_list','dashboard','student_details','finance_statement','current_timetable','semester_register','selected_courses','selected_timetable','unofficial_transcript','semester_gpa','check_listing',]
# available account types ['a_students','a_statement']
# use 'a_statement' for finance_statement

scrapper.get_view_data('a_students', 'semester_gpa', 'csv')
