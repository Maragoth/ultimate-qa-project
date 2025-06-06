# pages/registration_page.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, base_url):
        self.driver.get(base_url)
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//a[normalize-space()="Sign up"]'))
        ).click()

    def register(self, username, email, password):
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Username"]').send_keys(username)
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Email"]').send_keys(email)
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Password"]').send_keys(password)

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//button[normalize-space()="Sign up"]'))
        ).click()

        WebDriverWait(self.driver, 15).until(
            EC.url_contains('/')
        )

    def get_error_messages(self):
        error_elements = self.driver.find_elements(AppiumBy.CSS_SELECTOR, '.error-messages li')
        return [el.text for el in error_elements]
