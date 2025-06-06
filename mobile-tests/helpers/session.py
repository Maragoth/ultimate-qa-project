# helpers/session.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_user(driver, base_url, email, password):
    driver.get(base_url + "/login")
    driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Email"]').send_keys(email)
    driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Password"]').send_keys(password)
    driver.find_element(AppiumBy.XPATH, '//button[normalize-space()="Sign in"]').click()

def setup_user_session(driver, base_url, token, username):
    driver.get(base_url)
    
    # Set localStorage using JS
    driver.execute_script(f"localStorage.setItem('jwt', '{token}');")

    # Reload to trigger app logic
    driver.execute_script("location.reload();")

    # Wait for user to be recognized (navbar with profile link)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((AppiumBy.XPATH, f'//a[@href="/@{username}"]'))
    )
