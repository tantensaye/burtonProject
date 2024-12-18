from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config import get_locale_test_data
import time


class LoginPage:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale
        self.test_data = get_locale_test_data(str(locale))  # Retrieve locale-specific test data based on the driver's locale

    def enter_login_credentials(self):
        login_email_field = self.driver.find_element(By.XPATH, "(//input[@id='dwfrm_login_username'])[1]")
        login_email_field.send_keys(self.test_data["login_email"])

        login_password_field = self.driver.find_element(By.XPATH, "(//input[@id='dwfrm_login_password'])[1]")
        login_password_field.send_keys(self.test_data["login_password"])
        time.sleep(3)

    def sign_in(self):
        signin = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//button[@id='dwfrm_login_login'])[1]")))
        signin.click()
        time.sleep(5)
