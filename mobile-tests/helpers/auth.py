from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .config import BASE_URL
from .popup_handlers import handle_popups


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

    # Handle any popups that might appear
    handle_popups(driver)

    # Verify login was successful
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[normalize-space()="Your Feed"]'))
    )
