import pytest
from helpers.api_helpers import (
    create_random_user_via_api,
    create_article_via_api,
    add_comment_via_api as create_comment_via_api,
)
from helpers.assertions import assert_element_present
from helpers.auth import login_via_api_and_set_token
from appium.webdriver.common.appiumby import AppiumBy
from env import HOST_CONFIG
from helpers.waits import wait_for_element
from selenium.common.exceptions import TimeoutException
import time


@pytest.mark.mobile
def test_comment_author_profile(driver):
    """Test that verifies navigation to the comment author's profile and their articles on mobile"""

    # Step 1: Create a user via API for comment authorship
    start = time.time()
    user = create_random_user_via_api()
    print(f"Step 1: Create user via API – {time.time() - start:.2f}s")

    # Step 2: Create an article using the test user
    start = time.time()
    article = create_article_via_api(
        user["token"],
        {"title": "Title1", "description": "Desc1", "body": "Body1", "tagList": []},
    )
    print(f"Step 2: Create article via API – {time.time() - start:.2f}s")

    # Step 3: Add a comment to the article using the same user
    start = time.time()
    create_comment_via_api(user["token"], article["slug"], "Nice article!")
    print(f"Step 3: Create comment via API – {time.time() - start:.2f}s")

    # Step 4: Log in as the user and navigate to the article page
    start = time.time()
    login_via_api_and_set_token(driver, user)
    driver.get(
        f'http://{HOST_CONFIG["FRONTEND_HOST"]}:{HOST_CONFIG["FRONTEND_PORT"]}/article/{article["slug"]}'
    )
    print(f"Step 4: Login and navigate to article – {time.time() - start:.2f}s")

    # Step 5: Click on the comment author's username
    start = time.time()
    author_element = wait_for_element(
        driver,
        (AppiumBy.XPATH, "//a[contains(@class, 'comment-author')]"),
        timeout=5,
    )
    author_name = user["username"]
    print(f"Author name: {author_name}")
    author_element.click()
    print(f"Step 5: Click comment author – {time.time() - start:.2f}s")

    # Step 6: Verify profile page loads and author's name is visible
    start = time.time()
    wait_for_element(
        driver,
        (AppiumBy.XPATH, f"//h4[normalize-space(text())='{author_name}']"),
        timeout=5,
    )
    print(f"Step 6: Verify profile loaded – {time.time() - start:.2f}s")

    # Step 7: Ensure 'My Articles' tab is active
    start = time.time()
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            "//a[contains(@class, 'nav-link') and contains(@class, 'active') and normalize-space(text())='My Articles']",
        ),
        timeout=5,
    )
    print(f"Step 7: Verify 'My Articles' active – {time.time() - start:.2f}s")

    # Step 8: Check that at least one article preview is present
    start = time.time()
    assert_element_present(
        driver, AppiumBy.XPATH, "//div[contains(@class, 'article-preview')]"
    )
    print(f"Step 8: Assert articles visible – {time.time() - start:.2f}s")

    # Step 9: Validate that the author's name matches on the article preview
    start = time.time()
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//div[contains(@class, 'article-preview')]//a[contains(@class, 'author') and normalize-space(text())='{author_name}']",
        ),
        timeout=5,
    )
    print(f"Step 9: Verify article author – {time.time() - start:.2f}s")
