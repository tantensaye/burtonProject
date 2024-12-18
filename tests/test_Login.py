import pytest
import allure
import configparser
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config_webdrivers import configure_local_webdriver,configure_remote_webdriver
from config import staging_credentials, locale_test_data, get_locale_test_data
from config_utils import AssertionHelper
######################################################################################
from _Login_Page import LoginPage

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


@pytest.fixture(scope="module", params=["us/en", "at/en", "jp/en"])  # params = locale_test_data or ["us/en"]
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
        url = f"https://{staging_credentials}@dw-staging.burton.com/{locale}/sign-in?automationSession=true"
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
@allure.title('Login')
@allure.feature('Account Login')
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag('LOGIN')
def test_login_page(driver):
    try:
        # Access locale-specific test data
        locale = driver.locale

        # Instantiate page objects
        _login_page = LoginPage(driver, locale)

        # TEST STEPS
        _login_page.enter_login_credentials()
        _login_page.sign_in()

        # Get EXPECTED RESULTS via locale-specific test data
        test_data = get_locale_test_data(locale)
        expected_result = (
            f"Hi, {test_data['last_name']} {test_data['first_name']}"
            if locale == "jp/en"
            else f"Hi, {test_data['first_name']} {test_data['last_name']}"
        )

        # Get ACTUAL RESULTS
        account_welcome_element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.XPATH, "(//h2[contains(@class, 'mobile-account-welcome-text')])[2]"))
        )
        account_welcome_text = account_welcome_element.text

        # Perform assertion for EXPECTED RESULTS
        AssertionHelper.assert_equal(
            account_welcome_text,
            expected_result,
            f"Assertion failed for locale '{locale}' at welcome message verification. "
            f"Expected: '{expected_result}', but got: '{account_welcome_text}'."
        )

        # Log a success message if the assertion passes
        logger.info("Assertion passed for locale %s. Expected: '%s', got: '%s'.", locale, expected_result, account_welcome_text)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # This will catch any other kinds of errors
        # Capture screenshot on error ONLY during remote execution
        if execution_mode == "remote" and driver:
            allure.attach(driver.get_screenshot_as_png(), name="Screenshot on Failure", attachment_type=allure.attachment_type.PNG)
        raise
