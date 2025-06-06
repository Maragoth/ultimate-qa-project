import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pages.login_page import LoginPage
from helpers.config import BASE_URL
from helpers.popup_handlers import handle_popups
from helpers.assertions import verify_error_message
from selenium.webdriver.common.by import By
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
        popup = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Przetłumaczyć")]')
            )
        )

        # Click the gear icon
        gear_icon = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[contains(text(), "Przetłumaczyć")]/ancestor::div[@role="dialog"]//button[@aria-label="Więcej opcji tłumaczenia"]',
                )
            )
        )
        driver.execute_script("arguments[0].click();", gear_icon)

        # Click "Never translate pages in English"
        never_translate = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[text()="Nigdy nie tłumacz stron, których językiem jest angielski"]',
                )
            )
        )
        driver.execute_script("arguments[0].click();", never_translate)

        # Verify the popup is gone
        WebDriverWait(driver, 3).until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Przetłumaczyć")]')
            )
        )
        print("Translation popup successfully dismissed")
    except Exception as e:
        print(f"Translation popup not found or already dismissed: {str(e)}")


def dismiss_cookie_popup(driver):
    """Dismiss the cookie consent popup"""
    try:
        # Try to find and click "Odrzuć wszystko" button
        button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[normalize-space()="Odrzuć wszystko"]')
            )
        )
        driver.execute_script("arguments[0].click();", button)
    except Exception as e:
        print(f"Cookie popup not found or already dismissed: {str(e)}")


@pytest.mark.mobile
def test_invalid_login_displays_error_message(driver):
    """Test that invalid login credentials show appropriate error message"""

    # Initialize login page
    login_page = LoginPage(driver)
    login_page.navigate(BASE_URL)

    # Handle any popups that might appear
    handle_popups(driver)

    # Attempt login with invalid credentials
    login_page.login("wrong@email.com", "wrongpass")

    # Verify error message appears
    error_messages = login_page.get_error_messages()
    verify_error_message(error_messages, "email or password is invalid")
