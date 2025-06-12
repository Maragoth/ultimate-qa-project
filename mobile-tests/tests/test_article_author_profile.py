import pytest
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.assertions import assert_element_present, assert_element_count
from helpers.auth import login_via_api_and_set_token
from appium.webdriver.common.appiumby import AppiumBy
from env import HOST_CONFIG
from helpers.waits import wait_for_element, wait_for_element_clickable
from pages.article_page import ArticlePage
import time


@pytest.mark.mobile
def test_article_author_profile(driver):
    """Test that verifies navigation to the author's profile and their articles on mobile"""

    # Step 1: Create user via API
    start = time.time()
    user = create_random_user_via_api()
    print(f"Step 1: Create user via API – {time.time() - start:.2f}s")

    # Step 2: Create article via API
    start = time.time()
    create_article_via_api(
        user["token"],
        {"title": "Title1", "description": "Desc1", "body": "Body1", "tagList": []},
    )
    print(f"Step 2: Create article via API – {time.time() - start:.2f}s")

    # Step 3: Login and navigate
    start = time.time()
    login_via_api_and_set_token(driver, user)
    driver.get(f'http://{HOST_CONFIG["FRONTEND_HOST"]}:{HOST_CONFIG["FRONTEND_PORT"]}')
    print(f"Step 3: Login and navigate – {time.time() - start:.2f}s")

    # Step 4: Click Global Feed
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

    # Step 5: Click first article title
    start = time.time()
    wait_for_element(driver, (AppiumBy.XPATH, "//h1"), timeout=5).click()
    print(f"Step 5: Click first article – {time.time() - start:.2f}s")

    # Step 6: Click author's name
    start = time.time()
    author_element = wait_for_element(
        driver,
        (AppiumBy.XPATH, "//a[contains(@class, 'author')]"),
        timeout=5,
    )
    author_name = author_element.text.strip()
    author_element.click()
    print(f"Step 6: Click author – {time.time() - start:.2f}s")

    # Step 7: Verify profile page loaded with correct author name
    start = time.time()
    wait_for_element(
        driver,
        (AppiumBy.XPATH, f"//h4[normalize-space(text())='{author_name}']"),
        timeout=5,
    )
    print(f"Step 7: Verify profile loaded – {time.time() - start:.2f}s")

    # Step 8: Verify 'My Articles' tab is active
    start = time.time()
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            "//a[contains(@class, 'nav-link') and contains(@class, 'active') and normalize-space(text())='My Articles']",
        ),
        timeout=5,
    )
    print(f"Step 8: Verify 'My Articles' active – {time.time() - start:.2f}s")

    # Step 9: Verify at least one article is visible
    start = time.time()
    assert_element_present(
        driver, AppiumBy.XPATH, "//div[contains(@class, 'article-preview')]"
    )
    print(f"Step 9: Assert articles visible – {time.time() - start:.2f}s")

    # Step 10: Verify article author matches
    start = time.time()
    author_in_list = wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//div[contains(@class, 'article-preview')]//a[contains(@class, 'author') and normalize-space(text())='{author_name}']",
        ),
        timeout=5,
    )
    assert author_in_list, "Expected author's article not found"
    print(f"Step 10: Verify article author – {time.time() - start:.2f}s")
