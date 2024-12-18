from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


class SecureCheckout:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale

    # CART - Select the SECURE CHECKOUT/PROCEED TO CHECKOUT element and click
    def dynamic_secure_checkout(self):
        if self.locale == "jp/en":
            secure_checkout_xpath = "(//button[normalize-space()='Secure Checkout'])[1]"  # XPath for "jp/en" locale
        else:
            secure_checkout_xpath = "(//button[normalize-space()='Secure Checkout'])[1]"  # XPath for all other locales
        securecheckout = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, secure_checkout_xpath)))
        time.sleep(2)  # Wait for element to be stable
        securecheckout.click()

    # Methods to get the product details from the cart
    def get_cart_product_name(self):
        cart_name_xpath = "//div[contains(@class, 'card-header')]//a[contains(@class, 'item-name')]"
        name_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, cart_name_xpath)))
        return name_element.text.strip()

    def get_cart_product_price(self):
        cart_price_xpath = "//span[contains(@class, 'item-price-value')]"
        price_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, cart_price_xpath)))
        return price_element.text.strip()

    def get_cart_product_color(self):
        cart_color_xpath = "//span[contains(text(), 'Color:')]"
        color_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, cart_color_xpath)))
        return color_element.text.strip()

    def get_cart_product_size(self):
        cart_size_xpath = "//span[contains(text(), 'Size:')]"
        size_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, cart_size_xpath)))
        return size_element.text.strip()
