# helpers/waits.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, by_locator, timeout=10):
    """Wait until element is visible and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(by_locator)
    )

def wait_for_url_contains(driver, text, timeout=10):
    """Wait until current URL contains given text."""
    return WebDriverWait(driver, timeout).until(
        EC.url_contains(text)
    )
