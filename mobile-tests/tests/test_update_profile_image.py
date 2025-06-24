import pytest
from appium.webdriver.common.appiumby import AppiumBy
import time

from helpers.api_helpers import create_random_user_via_api
from helpers.auth import login_via_api_and_set_token
from helpers.waits import wait_for_element, wait_for_element_clickable
from env import HOST_CONFIG


@pytest.mark.mobile
def test_update_profile_image(driver):
    """Test that verifies updating user profile image from mobile"""

    # Step 1: Create a user using the API
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

    # Step 3: Update the profile image URL in the settings form
    start = time.time()
    image_url = "https://evek.one/4432-large_default/test.jpg"
    image_field = wait_for_element(
        driver, (AppiumBy.XPATH, "//input[@placeholder='URL of profile picture']")
    )
    image_field.clear()
    image_field.send_keys(image_url)

    update_button = wait_for_element_clickable(
        driver, (AppiumBy.XPATH, "//button[normalize-space()='Update Settings']")
    )
    update_button.click()
    print(f"Step 3: Submit updated image URL – {time.time() - start:.2f}s")

    # Step 4: Navigate to the user's public profile page
    start = time.time()
    profile_url = f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/@{user['username']}"
    driver.get(profile_url)
    print(f"Step 4: Navigate to profile – {time.time() - start:.2f}s")

    # Step 5: Verify that the updated image is visible on the profile
    start = time.time()
    profile_image = wait_for_element(
        driver, (AppiumBy.XPATH, f"//img[@src='{image_url}']")
    )
    assert profile_image is not None, "Updated profile image not found"
    print(f"Step 5: Verify image updated – {time.time() - start:.2f}s")
