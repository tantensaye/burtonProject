# config_webdrivers.py
# CONFIGURATION FILE to manage webdrivers
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Configures the remote WebDriver using Selenium Grid 4.
def configure_remote_webdriver(grid_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")

    # Set the path to ChromeDriver
    os.environ['webdriver.chrome.driver'] = '/opt/atlassian/pipelines/agent/build/chromedriver-linux64/chromedriver'  # ChromeDriver path

    # Create the WebDriver instance using the options
    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )
    return driver


# Configures a local WebDriver for the Windows machine.
def configure_local_webdriver():
    # Assuming the chromedriver is in the system PATH
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    return driver
