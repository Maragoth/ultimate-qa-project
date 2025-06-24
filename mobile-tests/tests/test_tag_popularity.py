import pytest
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.assertions import assert_element_present, assert_element_count
from helpers.auth import login_via_api_and_set_token
from appium.webdriver.common.appiumby import AppiumBy
from env import HOST_CONFIG
from helpers.waits import wait_for_element, wait_for_element_clickable
from pages.home_page import HomePage
from selenium.common.exceptions import TimeoutException
import time


@pytest.mark.mobile
def test_tag_popularity_feature(driver):
    """Test that verifies the tag popularity feature on mobile"""

    # Step 1: Create a user using the API
    start = time.time()
    user = create_random_user_via_api()
    print(f"Step 1: Create user via API – {time.time() - start:.2f}s")

    # Step 2: Create two articles with the same tag to increase its popularity
    tag = "PopularTagXYZ"
    start = time.time()
    create_article_via_api(
        user["token"],
        {"title": "Title1", "description": "Desc1", "body": "Body1", "tagList": [tag]},
    )
    create_article_via_api(
        user["token"],
        {"title": "Title2", "description": "Desc2", "body": "Body2", "tagList": [tag]},
    )
    print(f"Step 2: Create articles via API – {time.time() - start:.2f}s")

    # Step 3: Log in and navigate to the homepage
    start = time.time()
    login_via_api_and_set_token(driver, user)
    driver.get(f'http://{HOST_CONFIG["FRONTEND_HOST"]}:{HOST_CONFIG["FRONTEND_PORT"]}')
    print(f"Step 3: Login and navigate – {time.time() - start:.2f}s")

    # Step 4: Click the Global Feed tab to load articles
    start = time.time()
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            "//ul[contains(@class, 'nav-pills')]//a[normalize-space(text())='Global Feed']",
        ),
        timeout=3,
    ).click()
    print(f"Step 4: Click Global Feed – {time.time() - start:.2f}s")

    home_page = HomePage(driver)

    # Step 5: Scroll until the Popular Tags section becomes visible
    start = time.time()
    found = False
    for i in range(8):
        try:
            print(f"Scroll attempt {i+1}")
            home_page.wait_for_element(
                AppiumBy.XPATH, "//a[contains(@class, 'tag-pill')]", timeout=3
            )
            found = True
            break
        except TimeoutException:
            driver.execute_script("window.scrollBy(0, 1800)")
            time.sleep(0.5)
    print(f"Step 5: Scroll to Popular Tags – {time.time() - start:.2f}s")

    assert found, "Popular Tags section not found after scrolling"

    # Step 6: Click the tag from the Popular Tags section
    start = time.time()
    tag_element = wait_for_element_clickable(
        driver,
        (
            AppiumBy.XPATH,
            f"//a[contains(@class, 'tag-pill') and normalize-space(text())='{tag}']",
        ),
        timeout=5,
    )
    tag_element.click()
    print(f"Step 6: Click tag – {time.time() - start:.2f}s")

    # Step 7: Verify that the selected tag is active in the feed toggle nav
    start = time.time()
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//a[contains(@class, 'nav-link') and contains(@class, 'active') and contains(., '{tag}')]",
        ),
        timeout=5,
    )
    print(f"Step 7: Tag is active in nav – {time.time() - start:.2f}s")

    # Step 8: Assert that article previews are visible
    start = time.time()
    assert_element_present(
        driver, AppiumBy.XPATH, "//div[contains(@class, 'article-preview')]"
    )
    print(f"Step 8: Assert articles visible – {time.time() - start:.2f}s")

    # Step 9: Assert exactly 2 articles are shown for the selected tag
    start = time.time()
    assert_element_count(
        driver, AppiumBy.XPATH, "//div[contains(@class, 'article-preview')]", 2
    )
    print(f"Step 9: Assert article count – {time.time() - start:.2f}s")
