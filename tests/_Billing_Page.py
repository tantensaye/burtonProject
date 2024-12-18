from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config import get_locale_test_data
from config_utils import retry_on_exception
import time
import logging


# Set up logger
logger = logging.getLogger(__name__)


class CreditCard:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale
        self.test_data = get_locale_test_data(str(locale))  # Retrieve locale-specific test data based on the driver's locale
        self.wait = WebDriverWait(self.driver, 30)

    @retry_on_exception(retries=3, delay=2)
    def fill_credit_card_details(self):
        try:
            logger.info("Starting to fill credit card details...")
            time.sleep(4)  # Small delay to ensure payment form is fully loaded

            # Longer initial wait and explicitly wait for iframe container
            self.wait.until(
                ec.presence_of_element_located((By.XPATH, "(//div[@class='payment-methods'])[1]"))
            )

            # Wait for iframes container to be present
            self.wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, "adyen-checkout__card__form"))
            )

            # Wait for CARD NUMBER iframe
            logger.info("Filling card number")
            self.wait.until(
                ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='Iframe for secured card number']"))
            )
            card_number_field = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, "//input[@data-fieldtype='encryptedCardNumber']"))
            )
            self.wait.until(ec.visibility_of(card_number_field))
            card_number_field.clear()
            card_number_field.send_keys("4111111111111111")
            self.driver.switch_to.default_content()

            # Wait for EXPIRY DATE iframe
            logger.info("Filling expiry date")
            self.wait.until(
                ec.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, "//iframe[@title='Iframe for secured card expiry date']"))
            )
            expiry_field = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, "//input[@data-fieldtype='encryptedExpiryDate']"))
            )
            self.wait.until(ec.visibility_of(expiry_field))
            expiry_field.clear()
            expiry_field.send_keys("0330")
            self.driver.switch_to.default_content()

            # Wait for CVV iframe
            logger.info("Filling CVV")
            self.wait.until(
                ec.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, "//iframe[@title='Iframe for secured card security code']"))
            )
            cvv_field = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, "//input[@data-fieldtype='encryptedSecurityCode']"))
            )
            self.wait.until(ec.visibility_of(cvv_field))
            cvv_field.clear()
            cvv_field.send_keys("737")
            self.driver.switch_to.default_content()

            # Wait for CARDHOLDER iframe
            logger.info("Filling cardholder name")
            holder_name_field = self.wait.until(
                ec.presence_of_element_located((By.NAME, "holderName"))
            )
            # Fill CARDHOLDER NAME
            self.wait.until(ec.visibility_of(holder_name_field))
            holder_name_field.clear()
            holder_name_field.send_keys(self.test_data["customer_name"])

            logger.info("Successfully filled all credit card details")
            time.sleep(2)

        except Exception as e:
            logger.error(f"Error filling credit card details: {str(e)}")
            logger.error(f"Current URL: {self.driver.current_url}")  # Log the current URL and page source for debugging
            self.driver.switch_to.default_content()  # Ensure we're back to the main content
            raise

    def review_order(self):
        try:
            # Make sure we're back to the main content
            self.driver.switch_to.default_content()

            # Updated selector for the Review Order button
            review_order_button = self.wait.until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-payment[aria-label='Review Order']"))
            )
            review_order_button.click()

        except Exception as e:
            logger.error(f"Error clicking review order button: {str(e)}")
            raise


class GiftcardsBillingPage:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale
        self.test_data = get_locale_test_data(str(locale))  # Retrieve locale-specific test data based on the driver's locale

    def fill_contact_details(self):
        shippingemail_field = self.driver.find_element(By.ID, "dwfrm_shipping_email")
        shippingemail_field.send_keys(self.test_data["email"])

    def fill_credit_card_details(self):
        WebDriverWait(self.driver, 15).until(
            ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='Iframe for secured card number']")))
        WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(
            (By.XPATH, "//input[@data-fieldtype='encryptedCardNumber' and @aria-label='Card number']"))).send_keys(
            "4111111111111111")
        self.driver.switch_to.default_content()

        WebDriverWait(self.driver, 15).until(
            ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[@title='Iframe for secured card expiry date']")))
        WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(
            (By.XPATH, "//input[@data-fieldtype='encryptedExpiryDate' and @aria-label='Expiry date']"))).send_keys(
            "0330")
        self.driver.switch_to.default_content()

        WebDriverWait(self.driver, 15).until(ec.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "//iframe[@title='Iframe for secured card security code']")))
        WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(
            (By.XPATH, "//input[@data-fieldtype='encryptedSecurityCode' and @aria-label='Security code']"))).send_keys(
            "737")
        self.driver.switch_to.default_content()

        ccholdername = self.driver.find_element(By.NAME, "holderName")
        ccholdername.send_keys(self.test_data["customer_name"])
        self.driver.implicitly_wait(10)

    def fill_billing_details(self):
        # test_data = locale_test_data[self.locale]  # Retrieve locale-specific test data based on the driver's locale

        firstname_field = self.driver.find_element(By.ID, "dwfrm_billing_addressFields_firstName")
        firstname_field.send_keys(self.test_data["first_name"])

        lastname_field = self.driver.find_element(By.ID, "dwfrm_billing_addressFields_lastName")
        lastname_field.send_keys(self.test_data["last_name"])

        address1_field = self.driver.find_element(By.ID, "dwfrm_billing_addressFields_address1")
        address1_field.send_keys(self.test_data["billing_address1"])

        postalcode_field = self.driver.find_element(By.ID, "dwfrm_billing_addressFields_postalCode")
        postalcode_field.send_keys(self.test_data["billing_postal_code"])

        phonenumber_field = self.driver.find_element(By.ID, "dwfrm_billing_addressFields_phone")
        phonenumber_field.send_keys(self.test_data["phone_number"])
        time.sleep(5)

    def review_order(self):
        revieworder = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Review Order'])[1]")))
        revieworder.click()
        self.driver.implicitly_wait(10)
