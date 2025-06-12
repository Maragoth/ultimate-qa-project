import pytest
from appium.webdriver.common.appiumby import AppiumBy
import time

from helpers.api_helpers import create_random_user_via_api
from helpers.auth import login_via_api_and_set_token
from helpers.waits import (
    wait_for_element,
    wait_for_element_clickable,
    wait_for_url_contains,
)
from env import HOST_CONFIG


@pytest.mark.mobile
def test_update_profile_info(driver):
    """Test that verifies updating user profile info from mobile"""

    # Step 1: Create user via API
    start = time.time()
    user = create_random_user_via_api()
    print(f"Step 1: Create user via API – {time.time() - start:.2f}s")

    # Step 2: Login via API and navigate to settings
    start = time.time()
    login_via_api_and_set_token(driver, user)
    driver.get(
        f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/settings"
    )
    print(f"Step 2: Login and navigate to settings – {time.time() - start:.2f}s")

    # Step 3: Update username, bio and email
    start = time.time()
    new_username = f"{user['username']}_upd"
    new_bio = "This is my updated bio"
    new_email = f"upd_{user['email']}"

    username_field = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='Username']")
    )
    bio_field = wait_for_element(driver, (AppiumBy.XPATH, "//textarea"))
    email_field = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='Email']")
    )

    username_field.clear()
    username_field.send_keys(new_username)
    time.sleep(0.1)
    bio_field.clear()
    bio_field.send_keys(new_bio)
    time.sleep(0.1)
    email_field.clear()
    email_field.send_keys(new_email)
    time.sleep(0.1)

    # Trigger blur events to ensure frontend registers the change
    driver.execute_script("arguments[0].blur()", username_field)
    driver.execute_script("arguments[0].blur()", bio_field)
    driver.execute_script("arguments[0].blur()", email_field)

    update_button = wait_for_element_clickable(
        driver, (AppiumBy.XPATH, "//button[normalize-space()='Update Settings']")
    )
    update_button.click()

    wait_for_url_contains(driver, "/")  # Wait for redirect after update

    print(f"Step 3: Submit updated settings – {time.time() - start:.2f}s")

    # Step 4: Navigate again to settings page to force DOM update
    start = time.time()
    driver.get(
        f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/settings"
    )
    print(f"Step 4: Revisit settings – {time.time() - start:.2f}s")

    # Step 5: Verify updated values are displayed
    start = time.time()
    username_value = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='Username']")
    ).get_attribute("value")
    email_value = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='Email']")
    ).get_attribute("value")
    bio_element = wait_for_element(driver, (AppiumBy.XPATH, "//textarea"))
    bio_value = bio_element.get_attribute("value") or bio_element.text

    assert (
        username_value == new_username
    ), f"Username mismatch: expected {new_username}, got {username_value}"
    assert (
        email_value == new_email
    ), f"Email mismatch: expected {new_email}, got {email_value}"
    assert bio_value == new_bio, f"Bio mismatch: expected {new_bio}, got {bio_value}"

    print(f"Step 5: Verify updated values – {time.time() - start:.2f}s")
