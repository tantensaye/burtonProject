from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config import get_locale_test_data
import time
import logging


# Set up logger
logger = logging.getLogger(__name__)


class Shipping:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale
        self.test_data = get_locale_test_data(str(locale))  # Retrieve locale-specific test data based on the driver's locale
        self.wait = WebDriverWait(self.driver, 30)

    def fill_contact_details(self):
        shippingemail_field = self.driver.find_element(By.ID, "dwfrm_shipping_email")
        shippingemail_field.send_keys(self.test_data["email"])

    def fill_shipping_details(self):
        try:
            logger.info("Starting to fill credit card details...")
            time.sleep(4)  # Small delay to ensure shipping form is fully loaded

            firstname_field = self.driver.find_element(By.ID, "dwfrm_shipping_shippingAddress_addressFields_firstName")
            firstname_field.send_keys(self.test_data["first_name"])

            lastname_field = self.driver.find_element(By.ID, "dwfrm_shipping_shippingAddress_addressFields_lastName")
            lastname_field.send_keys(self.test_data["last_name"])

            if self.locale == "jp/en":
                firstnamepronunciation_field = self.driver.find_element(By.ID,"dwfrm_shipping_shippingAddress_addressFields_firstNamePronunciation")
                firstnamepronunciation_field.send_keys(self.test_data["first_name_pronunciation"])

                lastnamepronunciation_field = self.driver.find_element(By.ID,"dwfrm_shipping_shippingAddress_addressFields_lastNamePronunciation")
                lastnamepronunciation_field.send_keys(self.test_data["last_name_pronunciation"])

            address1_field = self.driver.find_element(By.ID, "dwfrm_shipping_shippingAddress_addressFields_address1")
            address1_field.send_keys(self.test_data["shipping_address1"])

            postalcode_field = self.driver.find_element(By.ID, "dwfrm_shipping_shippingAddress_addressFields_postalCode")
            postalcode_field.send_keys(self.test_data["shipping_postal_code"])

            phonenumber_field = self.driver.find_element(By.ID, "dwfrm_shipping_shippingAddress_addressFields_phone")
            phonenumber_field.send_keys(self.test_data["phone_number"])
            time.sleep(5)

        except Exception as e:
            logger.error(f"Error filling credit card details: {str(e)}")
            logger.error(f"Current URL: {self.driver.current_url}")  # Log the current URL and page source for debugging
            raise

    # SHIPPING - Get the selected SHIPPING METHOD name & price
    def get_shipping_method(self):
        # Wait for the shipping method radio buttons to be present
        WebDriverWait(self.driver, 15).until(
            ec.presence_of_element_located((By.XPATH, "//div[@class='shipping-methods']"))
        )

        # Check if the locale is jp/en
        if self.locale == "jp/en":
            try:
                # Locate the selected shipping method for jp/en
                selected_shipping_method = self.driver.find_element(By.XPATH, "(//label[@for='JPGround_B1'])[1]")

                # Retrieve the shipping time without the contents in the content-asset-container
                shipping_price = selected_shipping_method.find_element(By.XPATH, "(//span[@id='JPGround_B1-option-label'])[1]").text

                # Set shipping name to "N/A" since it's not directly extracted from this element
                shipping_name = "N/A"

                return shipping_name, shipping_price  # Return shipping name & price
            except Exception as e:
                print(f"No shipping method selected for jp/en locale. Error: {e}")
                return "No shipping method selected", "N/A"  # Return appropriate defaults

        # For other locales(NA & EU), continue with the existing logic
        try:
            selected_shipping_method = self.driver.find_element(By.XPATH, "//label[contains(@class, 'radio-field--selected')]")

            # Retrieve the associated price & name from the selected shipping method
            shipping_name = selected_shipping_method.text
            shipping_price = selected_shipping_method.find_element(By.XPATH, ".//span[contains(@class, 'option-label__price')]").text

            return shipping_name, shipping_price
        except Exception as e:
            print(f"No shipping method selected. Error: {e}")
            return "No shipping method selected", "N/A"  # Return appropriate defaults

    # SHIPPING - Select the CONTINUE TO PAYMENT element and click
    def continue_to_payment(self):
        continuetopayment = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue To Payment']")))
        continuetopayment.click()
