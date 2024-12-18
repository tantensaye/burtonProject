import time
import pytest
import allure
import configparser
import os
import logging
from config_webdrivers import configure_local_webdriver, configure_remote_webdriver
from config import staging_credentials, locale_test_data
from config_utils import AssertionHelper
##################################################################
from _Giftcards import GiftCardsPurchasePage
from _Cart_Page import SecureCheckout
from _Billing_Page import GiftcardsBillingPage
from _Order_Review_Page import OrderReview
from _Order_Confirmation_Page import GiftcardsOrderConfirmation

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the config.ini file
config_path = os.path.join(script_dir, '../config.ini')

# Read the configuration from the file
config = configparser.ConfigParser()
config.read(config_path)

execution_mode = config.get('Execution', 'mode')
grid_url = config.get('Execution', 'grid_url')

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module", params=["us/en"])  # params = locale_test_data or ["us/en"]
def driver(request):
    logger.info("Starting the test...")
    locale = request.param
    test_data = locale_test_data[locale]

    # Determine execution mode based on config.ini execution mode
    try:
        if execution_mode == "remote":
            driver = configure_remote_webdriver(grid_url)
        else:
            driver = configure_local_webdriver()

        # Maximize the browser window
        driver.maximize_window()

        # Navigate to burton.com SIGN IN page with environment credentials and locale
        url = f"https://{staging_credentials}@dw-staging.burton.com/{locale}/giftcards-purchase?automationSession=true"
        logger.info("Navigating to: %s", url)
        driver.get(url)

        # Assign test_data and locale to the driver object
        driver.test_data = test_data
        driver.locale = locale

        yield driver
    except Exception as e:
        pytest.fail(f"Driver setup failed for locale {locale}: {e}")
    finally:
        driver.quit()


@pytest.mark.regression
@allure.title('EGC only Secure Checkout')
@allure.feature('EGC Checkout')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag('CHECKOUT','EGC')
def test_egc_only_secure_checkout(driver):
    try:
        # Access locale-specific test data
        test_data = driver.test_data
        locale = driver.locale  # Retrieve the locale from the driver

        # Instantiate page objects
        _giftcards = GiftCardsPurchasePage(driver, locale)
        _cart_page = SecureCheckout(driver, locale)
        _billing_page = GiftcardsBillingPage(driver, locale)
        _order_review_page = OrderReview(driver, locale)
        _order_confirmation_page = GiftcardsOrderConfirmation(driver, test_data)

        # TEST STEPS
        _giftcards.select_amount()
        _giftcards.enter_egc_details()
        _giftcards.schedule_send_date()
        _giftcards.enter_sender_details()
        _giftcards.preview_egc()
        _giftcards.check_terms_and_conditions()
        _giftcards.egc_add_to_cart()
        _giftcards.checkout_now()

        _cart_page.dynamic_secure_checkout()

        _billing_page.fill_contact_details()
        _billing_page.fill_credit_card_details()
        _billing_page.fill_billing_details()
        _billing_page.review_order()

        _order_review_page.place_order()
        time.sleep(10)

        # Retrieve the order details from the order confirmation page
        order_data = _order_confirmation_page.get_giftcards_order_data()  # Get all order data

        # Retrieve the Order Number
        order_number = order_data.get('order_number')  # Assuming 'order_number' is in extracted_data

        # Log a success message with the ORDER NUMBER
        logger.info(f"Assertion passed for locale: {locale}. ORDER NUMBER: {order_number}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # This will catch any other kinds of errors
        # Capture screenshot on error ONLY during remote execution
        if execution_mode == "remote" and driver:
            allure.attach(driver.get_screenshot_as_png(), name="Screenshot on Failure", attachment_type=allure.attachment_type.PNG)
        raise
