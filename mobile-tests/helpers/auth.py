from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .config import BASE_URL


def login_via_api_and_set_token(driver, user):
    """Login a user by setting their JWT token directly in localStorage

    Args:
        driver: The WebDriver instance
        user: User dict containing token from API login/registration
    """
    # Navigate to home page first to set token
    driver.get(BASE_URL)

    # Set the JWT token in localStorage
    token_script = f'localStorage.setItem("jwt", "{user["token"]}")'
    driver.execute_script(token_script)

    # Reload page to apply token
    driver.get(BASE_URL)

    # Verify login was successful
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[normalize-space()="Your Feed"]'))
    )


def setup_user_session(driver, token, username):
    """Set up a user session by setting their JWT token and verifying login

    Args:
        driver: The WebDriver instance
        token: JWT token from API login/registration
        username: Username to verify in the UI after login
    """
    # Navigate to home page first to set token
    driver.get(BASE_URL)

    # Set the JWT token in localStorage
    token_script = f'localStorage.setItem("jwt", "{token}")'
    driver.execute_script(token_script)

    # Reload page to apply token
    driver.get(BASE_URL)

    # Verify login was successful by checking for username in nav
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f'//a[contains(@class, "nav-link") and contains(text(), "{username}")]',
            )
        )
    )
