from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from config import get_locale_test_data
import time
import random


class GiftCardsPurchasePage:
    def __init__(self, driver, locale):
        self.driver = driver
        self.locale = locale
        self.test_data = get_locale_test_data(str(locale))  # Retrieve locale-specific test data based on the driver's locale
        self.selected_amount = None  # Initialize selected_amount attribute(store selected_amount)

    def select_amount(self):
        amount_dropdown = self.driver.find_element(By.ID, 'amount')

        # Initialize a Select object with the dropdown element
        dropdown = Select(amount_dropdown)

        # Get all the available options from the dropdown
        options = dropdown.options

        # Randomly select an option from the dropdown
        selected_option = random.choice(options)

        # Get the text of the selected option
        selected_amount = selected_option.text

        # Store the selected amount in the attribute
        self.selected_amount = selected_amount

        # Select the option in the dropdown
        dropdown.select_by_visible_text(selected_amount)
        time.sleep(2)

    def enter_egc_details(self):
        recipient_name_field = self.driver.find_element(By.ID, "recipient")
        recipient_name_field.send_keys(self.test_data["customer_name"])

        recipient_email_field = self.driver.find_element(By.ID, "recipientEmail")
        recipient_email_field.send_keys(self.test_data["email"])

        confirm_recipient_email_field = self.driver.find_element(By.ID, "confirmRecipientEmail")
        confirm_recipient_email_field.send_keys(self.test_data["email"])

        gift_message_field = self.driver.find_element(By.ID, "message")
        gift_message_field.send_keys(self.test_data["egc_gift_message"])

    def schedule_send_date(self):
        sendnow = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='Send Now'])[1]")))
        sendnow.click()

    def enter_sender_details(self):
        sender_name_field = self.driver.find_element(By.ID, "from")
        sender_name_field.send_keys(self.test_data["egc_sender_name"])

    def preview_egc(self):
        preview_egc = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='Preview'])[1]")))
        preview_egc.click()
        time.sleep(2)

        # Locate preview elements and extract the text values and assert they match expected values

        preview_recipient_name_element = self.driver.find_element(By.XPATH, "(//div[@class='gc-order-preview-recipient text-b1-standard-bold txt-body'])[1]")
        preview_recipient_name = preview_recipient_name_element.text
        expected_recipient_name = self.test_data.get("customer_name")
        assert preview_recipient_name == expected_recipient_name, f"Expected recipient name: {expected_recipient_name}, Actual recipient name: {preview_recipient_name}"

        preview_gift_message_element = self.driver.find_element(By.XPATH, "(//div[@class='gc-order-preview-message text-b1-standard txt-body'])[1]")
        preview_gift_message = preview_gift_message_element.text
        expected_gift_message = self.test_data.get("egc_gift_message")
        assert preview_gift_message == expected_gift_message, f"Expected gift message: {expected_gift_message}, Actual gift message: {preview_gift_message}"

        preview_sender_name_element = self.driver.find_element(By.XPATH, "(//div[@class='gc-order-preview-from text-b1-standard-bold txt-body'])[1]")
        preview_sender_name = preview_sender_name_element.text
        expected_sender_name = self.test_data.get("egc_sender_name")
        assert preview_sender_name == expected_sender_name, f"Expected sender name: {expected_sender_name}, Actual sender name: {preview_sender_name}"

        preview_selected_amount_element = self.driver.find_element(By.XPATH, "(//div[@class='gc-order-preview-amount text-h2-display txt-brand'])[1]")
        preview_selected_amount = preview_selected_amount_element.text
        expected_selected_amount = self.selected_amount  # Access the selected amount
        assert preview_selected_amount == expected_selected_amount, f"Expected amount: {expected_selected_amount}, Actual amount: {preview_selected_amount}"

        closepreviewmodal = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//button[@class='dialog-close'])[1]")))
        closepreviewmodal.click()

    def check_terms_and_conditions(self):
        egc_termsandconditions = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='check-svg'])[1]")))
        egc_termsandconditions.click()

    def egc_add_to_cart(self):
        addtocart = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//button[@id='save'])[1]")))
        addtocart.click()
        time.sleep(2)

    def checkout_now(self):
        checkoutnow = WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='View Cart and Checkout'])[1]")))
        checkoutnow.click()
        time.sleep(2)
