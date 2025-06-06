import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pages.login_page import LoginPage
from helpers.api_helpers import create_random_user_via_api
from helpers.waits import wait_for_element
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Get frontend host from environment variable, default to localhost for local development
FRONTEND_HOST = os.getenv("FRONTEND_HOST", "localhost")
FRONTEND_PORT = os.getenv("FRONTEND_PORT", "4100")
BASE_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

def dismiss_translation_popup(driver):
    """Dismiss the Chrome translation popup by selecting 'Never translate pages in English'"""
    try:
        # Wait for the translation popup to appear
        popup = WebDriverWait(driver, 3).until(  # Reduced from 10 to 3 seconds
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Przetłumaczyć")]'))
        )
        
        # Click the gear icon
        gear_icon = WebDriverWait(driver, 3).until(  # Reduced from 5 to 3 seconds
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Przetłumaczyć")]/ancestor::div[@role="dialog"]//button[@aria-label="Więcej opcji tłumaczenia"]'))
        )
        driver.execute_script("arguments[0].click();", gear_icon)
        
        # Click "Never translate pages in English"
        never_translate = WebDriverWait(driver, 3).until(  # Reduced from 5 to 3 seconds
            EC.element_to_be_clickable((By.XPATH, '//div[text()="Nigdy nie tłumacz stron, których językiem jest angielski"]'))
        )
        driver.execute_script("arguments[0].click();", never_translate)
        
        # Verify the popup is gone
        WebDriverWait(driver, 3).until_not(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Przetłumaczyć")]'))
        )
        print("Translation popup successfully dismissed")
    except Exception as e:
        print(f"Translation popup not found or already dismissed: {str(e)}")

def dismiss_cookie_popup(driver):
    """Dismiss the cookie consent popup"""
    try:
        # Try to find and click "Odrzuć wszystko" button
        button = WebDriverWait(driver, 3).until(  # Reduced from 10 to 3 seconds
            EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Odrzuć wszystko"]'))
        )
        driver.execute_script("arguments[0].click();", button)
    except Exception as e:
        print(f"Cookie popup not found or already dismissed: {str(e)}")

@pytest.mark.mobile
def test_user_can_login_successfully_using_dynamic_user(driver):
    # Create user first to minimize delay between creation and usage
    user = create_random_user_via_api()
    
    # Navigate directly to the login page instead of going through Google first
    login_page = LoginPage(driver)
    login_page.navigate(BASE_URL)
    
    # Handle translation popup if it appears (should be prevented by Chrome options)
    try:
        WebDriverWait(driver, 3).until(  # Reduced from 5 to 3 seconds
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Przetłumaczyć")]'))
        )
        dismiss_translation_popup(driver)
    except:
        print("No translation popup on frontend")
    
    # Perform login
    login_page.login(user["email"], user["password"])
    
    # Verify successful login
    wait_for_element(driver, (By.XPATH, '//a[normalize-space()="Your Feed"]'), timeout=5)  # Reduced from 10 to 5 seconds
