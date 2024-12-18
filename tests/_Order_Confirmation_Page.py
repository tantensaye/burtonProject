import logging
from selenium.webdriver.common.by import By
from config import europe
from config_utils import retry_on_exception


class AssertionHelper:
    @staticmethod
    def assert_equal(expected, actual, message):
        assert expected == actual, message


class OrderConfirmation:
    order_data = []  # List to store order confirmation data for each locale

    def __init__(self, driver, test_data):
        self.driver = driver
        self.test_data = test_data

    @retry_on_exception(retries=3, delay=2)
    def get_order_data(self, shipping_price):
        # Locate and retrieve text from order confirmation page
        # Check locale to adjust the shipping summary locator
        if self.driver.locale == "jp/en":
            shipping_summary = self.driver.find_element(By.XPATH, "//div[@class='jp-shipping-summary']")

            # Extract the required fields for APAC
            extracted_data = {
                'email': shipping_summary.find_element(By.XPATH, ".//div[@role='region' and @aria-labelledby='checkout-card__title--contact']/p").text,
                'customer_name': shipping_summary.find_element(By.XPATH, ".//div[@class='fullName']").text,
                'shipping_address1': shipping_summary.find_element(By.XPATH, ".//span[@class='address1']").text,
                'shipping_city': shipping_summary.find_element(By.XPATH, ".//span[@class='city']").text,
                'shipping_state': shipping_summary.find_element(By.XPATH, ".//span[@class='prefecture']").text,
                # 'shipping_postal_code': shipping_summary.find_element(By.XPATH, ".//span[@class='postalCode']").text,
                'phone_number': shipping_summary.find_element(By.XPATH, ".//div[contains(@class, 'shipping-phone')]").text,
                'order_number': shipping_summary.find_element(By.XPATH, "//div[@class='email-wrapper']//span[@class='email-wrapper__order-number']").text,
                'shipping_method_price': shipping_summary.find_element(By.XPATH, ".//div[@class='shipping-method-arrival-date']/span").text
            }
        else:
            shipping_summary = self.driver.find_element(By.XPATH, "(//div[@class='shipping-summary'])[1]")

            # Extract the required fields for NA & EU
            extracted_data = {
                'email': shipping_summary.find_element(By.XPATH, ".//div[@role='region' and @aria-labelledby='checkout-card__title--contact']/p").text,
                'customer_name': shipping_summary.find_element(By.XPATH, ".//span[@class='fullName']").text,
                'shipping_address1': shipping_summary.find_element(By.XPATH, ".//div[@class='address1']").text,
                'shipping_city': shipping_summary.find_element(By.XPATH, ".//span[@class='city']").text,
                'shipping_state': shipping_summary.find_element(By.XPATH, ".//span[@class='stateCode']").text,
                # 'shipping_postal_code': shipping_summary.find_element(By.XPATH, ".//span[@class='postalCode']").text,
                'phone_number': shipping_summary.find_element(By.XPATH, ".//div[contains(@class, 'shipping-phone')]").text,
                'shipping_method_price': shipping_summary.find_element(By.XPATH, ".//span[@class='shipping-method-price']").text,
                'order_number': shipping_summary.find_element(By.XPATH, "//div[@class='email-wrapper']//span[@class='email-wrapper__order-number']").text
            }

        # Prepare for collect errors
        errors = []

        # Assert that the retrieved text matches the STATIC TEST DATA for specific fields
        logging.info("\n----- ORDER CONFIRMATION ASSERTIONS -----")
        expected_keys = ['email', 'customer_name', 'shipping_address1', 'shipping_city', 'shipping_state', 'phone_number']

        # Add shipping state only if locale is not European
        if self.driver.locale not in europe:
            expected_keys.append('shipping_state')

        for key in expected_keys:
            expected_value = self.test_data.get(key)
            actual_value = extracted_data.get(key)

            # If the locale is European and we're checking for shipping state, set expected to None
            if key == 'shipping_state' and self.driver.locale in europe:
                expected_value = None  # Set expected value to None for European locales

            try:
                # Compare the expected and actual values, accounting for empty states
                if expected_value is None and actual_value == "":
                    actual_value = None  # Treat empty string as None for comparison

                AssertionHelper.assert_equal(expected_value, actual_value,
                                             f"Expected {key.replace('_', ' ').title()}: {expected_value}, Actual: {actual_value}")
                logging.info(f"Assertion Success: {key.replace('_', ' ').title()} matches. Expected = {expected_value}, Actual = {actual_value}")
            except AssertionError as e:
                logging.error(f"Assertion Failure: {str(e)}")
                errors.append(str(e))  # Collect the error message

        # Assert that the shipping method matches the expected shipping price
        try:
            shipping_method_price = extracted_data['shipping_method_price']

            AssertionHelper.assert_equal(shipping_price, shipping_method_price,
                                         f"Expected Shipping Price: {shipping_price}, Actual: {shipping_method_price}")
            logging.info(f"Assertion Success: Shipping Method Price matches. Expected = {shipping_price}, Actual = {shipping_method_price}")
        except AssertionError as e:
            logging.error(f"Assertion Failure: {str(e)}")
            errors.append(str(e))  # Collect the error message

        # Raise an exception if there are any errors
        if errors:
            raise AssertionError("\n".join(errors))

        return extracted_data  # Return the extracted data for further comparisons


class GiftcardsOrderConfirmation:
    order_data = []  # List to store order confirmation data for each locale

    def __init__(self, driver, test_data):
        self.driver = driver
        self.test_data = test_data

    def get_giftcards_order_data(self):
        billing_summary = self.driver.find_element(By.XPATH, "(//div[@class='summary-details billing'])[1]")

        # Extract the required fields EGC North America
        extracted_data = {
            'customer_name': billing_summary.find_element(By.XPATH, "(//div[@class='name-container'])[1]").text,
            'billing_address1': billing_summary.find_element(By.XPATH, "(//div[@class='address1'])[1]").text,
            'shipping_city': billing_summary.find_element(By.XPATH, ".//span[@class='city']").text,
            'shipping_state': billing_summary.find_element(By.XPATH, "(//span[@class='stateCode'])[1]").text,
            # 'shipping_postal_code': billing_summary.find_element(By.XPATH, ".//span[@class='postalCode']").text,
            'email': billing_summary.find_element(By.XPATH, "(//span[@class='order-summary-email'])[1]").text,
            'phone_number': billing_summary.find_element(By.XPATH, "(//span[@class='order-summary-phone'])[1]").text,
            'order_number': billing_summary.find_element(By.XPATH, "//div[@class='email-wrapper']//span[@class='email-wrapper__order-number']").text
        }

        # Prepare for collect errors
        errors = []

        # Assert that the retrieved text matches the STATIC TEST DATA for specific fields
        logging.info("\n----- ORDER CONFIRMATION ASSERTIONS -----")
        expected_keys = ['customer_name', 'billing_address1', 'shipping_city', 'shipping_state', 'email', 'phone_number']

        for key in expected_keys:
            expected_value = self.test_data.get(key)
            actual_value = extracted_data.get(key)

            try:
                AssertionHelper.assert_equal(expected_value, actual_value,
                                             f"Expected {key.replace('_', ' ').title()}: {expected_value}, Actual: {actual_value}")
                logging.info(f"Assertion Success: {key.replace('_', ' ').title()} matches. Expected = {expected_value}, Actual = {actual_value}")
            except AssertionError as e:
                logging.error(f"Assertion Failure: {str(e)}")
                errors.append(str(e))  # Collect the error message

        # Raise an exception if there are any errors
        if errors:
            raise AssertionError("\n".join(errors))

        return extracted_data  # Return the extracted data for further comparisons
