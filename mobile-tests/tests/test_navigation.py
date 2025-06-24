import pytest
from appium.webdriver.common.appiumby import AppiumBy
import time

from helpers.api_helpers import create_random_user_via_api
from helpers.auth import login_via_api_and_set_token
from helpers.waits import wait_for_element, wait_for_element_clickable
from env import HOST_CONFIG


@pytest.mark.mobile
def test_navigation(driver):
    """Test that verifies the visibility of navigation links before and after login on mobile"""

    # Step 1: Visit home page and verify public navigation links
    start = time.time()
    driver.get(f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/")
    wait_for_element(driver, (AppiumBy.XPATH, "//a[normalize-space()='Home']"))
    wait_for_element(
        driver, (AppiumBy.XPATH, "//a[@href='/login' and normalize-space()='Sign in']")
    )
    wait_for_element(
        driver,
        (AppiumBy.XPATH, "//a[@href='/register' and normalize-space()='Sign up']"),
    )
    print(f"Step 1: Navigation links before login – {time.time() - start:.2f}s")

    # Step 2: Create a user and perform login via token injection
    start = time.time()
    user = create_random_user_via_api()
    login_via_api_and_set_token(driver, user)
    driver.get(f"http://{HOST_CONFIG['FRONTEND_HOST']}:{HOST_CONFIG['FRONTEND_PORT']}/")
    print(f"Step 2: Create user and login – {time.time() - start:.2f}s")

    # Step 3: Verify that authenticated navigation links are visible
    start = time.time()
    wait_for_element(
        driver, (AppiumBy.XPATH, "//a[@href='/' and normalize-space()='Home']")
    )
    wait_for_element(
        driver, (AppiumBy.XPATH, "//a[@href='/editor' and contains(., 'New Post')]")
    )
    wait_for_element(
        driver,
        (AppiumBy.XPATH, "//a[@href='/settings' and contains(., 'Settings')]"),
    )
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//a[@href='/@{user['username']}' and normalize-space()='{user['username']}']",
        ),
    )
    print(f"Step 3: Navigation links after login – {time.time() - start:.2f}s")
