import time
import pytest
import allure
import configparser
import os
import logging
from config_webdrivers import configure_local_webdriver, configure_remote_webdriver
from config import staging_credentials, locale_test_data, get_product_id
from config_utils import AssertionHelper, wait_for_page_load, PerformanceMetrics, retry_on_exception
################################################################################
from _Product_Detail_Page import SoftgoodsPDP
from _Cart_Page import SecureCheckout
from _Shipping_Page import Shipping
from _Billing_Page import CreditCard
from _Order_Review_Page import OrderReview
from _Order_Confirmation_Page import OrderConfirmation


# Set up logger
logger = logging.getLogger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
config_path = os.path.join(script_dir, '../config.ini')  # Construct the full path to the config.ini file
config = configparser.ConfigParser()  # Read the configuration from the file
config.read(config_path)

execution_mode = config.get('Execution', 'mode')
grid_url = config.get('Execution', 'grid_url')


@retry_on_exception(retries=3, delay=1)
@pytest.fixture(scope="module", params=locale_test_data)  # params = locale_test_data or ["us/en"]
def driver(request):
    logger.info("Starting the test...")
    locale = request.param
    test_data = locale_test_data[locale]

    try:
        # Determine execution mode based on config.ini execution mode
        if execution_mode == "remote":
            driver = configure_remote_webdriver(grid_url)
        else:
            driver = configure_local_webdriver()

        # Maximize the browser window
        driver.maximize_window()

        # Navigate to burton.com PDP with environment credentials and locale
        url = f"https://{staging_credentials}@dw-staging.burton.com/{locale}/p/burton-classic-short-sleeve-t-shirt/{get_product_id(locale)}.html?automationSession=true"
        logger.info("Navigating to: %s", url)
        driver.get(url)

        # Assign test_data and locale to the driver object
        driver.test_data = test_data
        driver.locale = locale

        return driver
    except Exception as e:
        pytest.fail(f"Driver setup failed for locale {locale}: {e}")


@pytest.mark.regression
@allure.title('Softgoods Secure Checkout')
@allure.feature('Checkout')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag('CHECKOUT','SOFTGOODS')
def test_softgoods_secure_checkout(driver):
    try:
        # Access locale-specific test data
        test_data = driver.test_data
        locale = driver.locale

        # Instantiate page objects
        _product_detail_page = SoftgoodsPDP(driver)
        _cart_page = SecureCheckout(driver, locale)
        _shipping_page = Shipping(driver, locale)
        _billing_page = CreditCard(driver, locale)
        _order_review_page = OrderReview(driver, locale)
        _order_confirmation_page = OrderConfirmation(driver, test_data)

        # TEST STEPS
        # Select product options and add to cart
        _product_detail_page.select_color_variant()
        _product_detail_page.select_size_variant()
        _product_detail_page.add_to_cart()

        # Retrieve product details from Add to Cart modal
        product_info = {
            "name": _product_detail_page.get_product_name(),
            "price": _product_detail_page.get_product_price(),
            "color": _product_detail_page.get_product_color(),
            "size": _product_detail_page.get_product_size(),
        }

        _product_detail_page.view_cart()
        wait_for_page_load(driver)  # WAIT FOR PAGE LOAD

        # Retrieve product details from the cart
        cart_info = {
            "name": _cart_page.get_cart_product_name(),
            "price": _cart_page.get_cart_product_price(),
            "color": _cart_page.get_cart_product_color(),
            "size": _cart_page.get_cart_product_size(),
        }

        # Assert product details match from PDP to Cart
        logger.info("\n----- CART ASSERTIONS -----")
        expected_keys = ['name', 'price', 'color', 'size']
        for key in expected_keys:
            expected_value = product_info[key]
            actual_value = cart_info[key]
            try:
                AssertionHelper.assert_equal(expected_value, actual_value,
                                             f"Expected {key.replace('_', ' ').title()}: {expected_value}, Actual: {actual_value}")
                logger.info(f"Assertion Success: {key.replace('_', ' ').title()} matches. Expected = {expected_value}, Actual = {actual_value}")
            except AssertionError as e:
                logger.error(f"Assertion Failure: {str(e)}")

        _cart_page.dynamic_secure_checkout()
        wait_for_page_load(driver)  # WAIT FOR PAGE LOAD
        metrics = PerformanceMetrics.capture_page_load_metrics(driver)

        _shipping_page.fill_contact_details()
        _shipping_page.fill_shipping_details()

        # Get the shipping name & price from the shipping page
        shipping_name, shipping_price = _shipping_page.get_shipping_method()

        _shipping_page.continue_to_payment()
        wait_for_page_load(driver)  # WAIT FOR PAGE LOAD
        time.sleep(4)

        _billing_page.fill_credit_card_details()
        _billing_page.review_order()
        wait_for_page_load(driver)  # WAIT FOR PAGE LOAD

        _order_review_page.place_order()
        wait_for_page_load(driver)  # WAIT FOR PAGE LOAD

        # Retrieve the order details from the order confirmation page
        order_data = _order_confirmation_page.get_order_data(shipping_price)  # Get all order data

        # Retrieve the Order Number
        order_number = order_data.get('order_number')  # Assuming 'order_number' is in extracted_data

        # Log a success message with the ORDER NUMBER
        logger.info(f"Assertion passed for locale: {locale}. ORDER NUMBER: {order_number}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # Log the unexpected error
        # Capture screenshot on error ONLY during remote execution
        if execution_mode == "remote" and driver is not None:
            allure.attach(driver.get_screenshot_as_png(), name="Screenshot on Failure", attachment_type=allure.attachment_type.PNG)
        raise
    finally:
        if driver is not None:
            driver.quit()
