import time
import logging
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config import get_locale_test_data, europe
from config_utils import retry_on_exception


class OrderReview:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale
        self.test_data = get_locale_test_data(str(locale))  # Retrieve locale-specific test data based on the driver's locale
        self.wait = WebDriverWait(self.driver, 30)

    @retry_on_exception(retries=3, delay=2)
    def place_order(self):
        time.sleep(2)
        if self.locale in europe:
            try:
                eu_termsandconditions = WebDriverWait(self.driver, 30).until(
                    ec.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='check-svg'])[1]")))
                eu_termsandconditions.click()
            except StaleElementReferenceException:
                eu_termsandconditions = WebDriverWait(self.driver, 30).until(
                    ec.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='check-svg'])[1]")))
                eu_termsandconditions.click()

        placeorder = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//button[@class='btn btn btn-primary btn-block place-order place-order--bottom'])[1]")))
        placeorder.click()
        self.driver.implicitly_wait(10)
