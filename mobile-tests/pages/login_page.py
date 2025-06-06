# pages/login_page.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, base_url):
        self.driver.get(base_url)
        # Wait for the page to load and the Sign in link to be clickable
        sign_in_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//a[normalize-space()="Sign in"]'))
        )
        # Use JavaScript click for better reliability
        self.driver.execute_script("arguments[0].click();", sign_in_link)
        # Wait for login form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//input[@placeholder="Email"]'))
        )

    def login(self, email, password):
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Email"]').send_keys(email)
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Password"]').send_keys(password)
        sign_in_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//button[normalize-space()="Sign in"]'))
        )
        self.driver.execute_script("arguments[0].click();", sign_in_button)

    def get_error_messages(self):
        error_elements = self.driver.find_elements(AppiumBy.CSS_SELECTOR, '.error-messages li')
        return [el.text for el in error_elements]
