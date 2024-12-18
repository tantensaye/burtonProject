# config_utils.py
# CONFIGURATION FILE to manage important helper functions

import logging
import functools
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (StaleElementReferenceException,ElementClickInterceptedException)

# Set up logger
logger = logging.getLogger(__name__)


class AssertionHelper:
    @staticmethod
    def assert_equal(expected, actual, message):
        """Assert that two values are equal."""
        assert expected == actual, message


def wait_for_page_load(driver, timeout=30):
    """Wait for page load to complete."""
    def page_has_loaded(driver):
        return driver.execute_script("return document.readyState") == "complete"

    try:
        WebDriverWait(driver, timeout).until(page_has_loaded)
    except Exception as e:
        logging.error(f"Page load timeout: {str(e)}")
        raise


def retry_on_exception(retries=3, delay=2):
    """Decorator to retry flaky operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                    logger.warning(f"Retrying {func.__name__} due to: {e}")
                    time.sleep(delay)
            raise
        return wrapper
    return decorator


class PerformanceMetrics:
    @staticmethod
    def capture_page_load_metrics(driver):
        """Capture page load performance metrics."""
        try:
            navigation_timing = driver.execute_script("""
                let performance = window.performance;     // Access browser's performance API 
                let timing = performance.timing;          // Get timing interface
                return {
                    'page_load_time': timing.loadEventEnd - timing.navigationStart,
                    'dns_time': timing.domainLookupEnd - timing.domainLookupStart,
                    'server_response_time': timing.responseEnd - timing.requestStart,
                    'dom_content_loaded': timing.domContentLoadedEventEnd - timing.navigationStart
                }
            """)
            logger.info(f"Performance metrics: {navigation_timing}")
            return navigation_timing
        except Exception as e:
            logger.error(f"Failed to capture performance metrics: {str(e)}")
            return None
