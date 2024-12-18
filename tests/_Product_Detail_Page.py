from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


class SoftgoodsPDP:
    def __init__(self, driver):
        self.driver = driver

    def select_color_variant(self):
        variationcolor = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, "(//img[@alt='True Black'])[1]")))
        variationcolor.click()
        time.sleep(2)

    def select_size_variant(self):
        sizevariation = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, "(//span[normalize-space()='L'])[1]")))
        sizevariation.click()

    def add_to_cart(self):
        addtocart = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Add to Cart'])[1]")))
        addtocart.click()

    def view_cart(self):
        viewcart = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='View Cart and Checkout'])[1]")))
        viewcart.click()

    # Methods to get the product details from the PDP Add to Cart modal
    def get_product_name(self):
        product_name_xpath = "//p[contains(@class, 'product-title')]"
        name_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, product_name_xpath)))
        return name_element.text.strip()

    def get_product_price(self):
        product_price_xpath = "//p[contains(@class, 'product-price')]//span[contains(@class, 'standard-price')]"
        price_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, product_price_xpath)))

        # Extract the raw price text
        raw_price = price_element.text.strip()

        # If the price string contains additional text, we need to extract only the relevant part
        if '¥' in raw_price:
            final_price = raw_price.split('(')[0].strip()  # Get the part before any tax info
        else:
            final_price = raw_price  # Fallback in case structure changes

        return final_price

    def get_product_color(self):
        product_color_xpath = "//p[contains(@class, 'product-attribute') and contains(text(), 'Color:')]"
        color_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, product_color_xpath)))
        return color_element.text.strip()

    def get_product_size(self):
        product_size_xpath = "//p[contains(@class, 'product-attribute') and contains(text(), 'Size:')]"
        size_element = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.XPATH, product_size_xpath)))
        return size_element.text.strip()
