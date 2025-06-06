# pages/registration_page.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, base_url):
        self.driver.get(base_url)
        # Wait for the page to load and the Sign up link to be clickable
        sign_up_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//a[normalize-space()="Sign up"]')
            )
        )
        # Use JavaScript click for better reliability
        self.driver.execute_script("arguments[0].click();", sign_up_link)
        # Wait for registration form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//input[@placeholder="Username"]')
            )
        )

    def register(self, username, email, password):
        # Fill in registration form
        self.driver.find_element(
            AppiumBy.XPATH, '//input[@placeholder="Username"]'
        ).send_keys(username)
        self.driver.find_element(
            AppiumBy.XPATH, '//input[@placeholder="Email"]'
        ).send_keys(email)
        self.driver.find_element(
            AppiumBy.XPATH, '//input[@placeholder="Password"]'
        ).send_keys(password)

        # Click Sign up button
        sign_up_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//button[normalize-space()="Sign up"]')
            )
        )
        self.driver.execute_script("arguments[0].click();", sign_up_button)

    def get_error_messages(self):
        error_elements = self.driver.find_elements(
            AppiumBy.CSS_SELECTOR, ".error-messages li"
        )
        return [el.text for el in error_elements]
