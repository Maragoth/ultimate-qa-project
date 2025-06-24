import pytest
from appium.webdriver.common.appiumby import AppiumBy
import time

from helpers.api_helpers import create_random_user_via_api
from helpers.auth import login_via_api_and_set_token
from helpers.waits import wait_for_element, wait_for_element_clickable
from env import HOST_CONFIG


@pytest.mark.mobile
def test_update_password(driver):
    """Test that verifies updating user password from mobile"""

    # Step 1: Create a test user via API
    start = time.time()
    user = create_random_user_via_api()
    print(f"Step 1: Create user via API – {time.time() - start:.2f}s")

    # Step 2: Log in and navigate to the settings page
    start = time.time()
    login_via_api_and_set_token(driver, user)
    driver.get(
        f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/settings"
    )
    print(f"Step 2: Login and navigate to settings – {time.time() - start:.2f}s")

    # Step 3: Update the password using the settings form
    start = time.time()
    new_password = "NewPass123!"
    password_field = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='New Password']")
    )
    password_field.clear()
    password_field.send_keys(new_password)

    update_button = wait_for_element_clickable(
        driver, (AppiumBy.XPATH, "//button[normalize-space()='Update Settings']")
    )
    update_button.click()
    print(f"Step 3: Submit updated password – {time.time() - start:.2f}s")

    # Step 4: Navigate again to the settings page after redirect
    start = time.time()
    driver.get(
        f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/settings"
    )
    print(f"Step 4: Revisit settings – {time.time() - start:.2f}s")

    # Step 5: Logout using the logout button
    start = time.time()
    logout_button = wait_for_element_clickable(
        driver,
        (AppiumBy.XPATH, "//button[contains(text(), 'Or click here to logout')]"),
    )
    logout_button.click()
    print(f"Step 5: Logout – {time.time() - start:.2f}s")

    # Step 6: Attempt login using the new password
    start = time.time()
    login_url = (
        f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/login"
    )
    driver.get(login_url)

    email_field = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='Email']")
    )
    password_field = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='Password']")
    )
    email_field.send_keys(user["email"])
    password_field.send_keys(new_password)

    sign_in_button = wait_for_element_clickable(
        driver, (AppiumBy.XPATH, "//button[normalize-space()='Sign in']")
    )
    sign_in_button.click()
    print(f"Step 6: Login with new password – {time.time() - start:.2f}s")

    # Step 7: Verify successful login by checking for profile link
    start = time.time()
    profile_link_xpath = (
        f"//a[contains(@href, '/@') and contains(text(), '{user['username']}')]"
    )
    wait_for_element(driver, (AppiumBy.XPATH, profile_link_xpath))
    print(f"Step 7: Verify login success – {time.time() - start:.2f}s")
