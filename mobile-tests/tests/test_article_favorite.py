import pytest
from appium.webdriver.common.appiumby import AppiumBy
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.test_data import generate_article
from helpers.waits import wait_for_element
from helpers.assertions import assert_element_present, assert_element_not_present
from helpers.auth import login_via_api_and_set_token
from env import HOST_CONFIG
import time


@pytest.mark.mobile
def test_article_favorite_flow(driver):
    """Test favoriting and unfavoriting an article from profile"""

    # Step 1: Create a test user and article using API
    user = create_random_user_via_api()
    article = generate_article("Favorite", f"Tag-{int(time.time())}")
    create_article_via_api(user["token"], article)

    # Step 2: Log in as the test user and navigate to the frontend
    login_via_api_and_set_token(driver, user)
    driver.get(f'http://{HOST_CONFIG["FRONTEND_HOST"]}:{HOST_CONFIG["FRONTEND_PORT"]}')

    # Step 3: Click on 'Global Feed' tab to load public articles
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            "//ul[contains(@class, 'nav-pills')]//a[normalize-space(text())='Global Feed']",
        ),
        timeout=3,
    ).click()

    # Step 4: Locate the created article and click the heart icon to favorite it
    article_preview = wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//div[contains(@class, 'article-preview') and .//h1[contains(text(), '{article['title']}')]]",
        ),
        timeout=3,
    )
    article_preview.find_element(
        AppiumBy.XPATH, ".//button[.//i[contains(@class, 'ion-heart')]]"
    ).click()

    # Step 5: Navigate to user's profile and open 'Favorited Articles' tab
    wait_for_element(
        driver, (AppiumBy.XPATH, f"//a[contains(@href, '@{user['username']}')]")
    ).click()
    wait_for_element(
        driver, (AppiumBy.XPATH, "//a[contains(text(), 'Favorited Articles')]")
    ).click()

    # Step 6: Assert that the favorited article appears in the list
    assert_element_present(
        driver,
        AppiumBy.XPATH,
        f"//div[contains(@class, 'article-preview') and .//h1[contains(text(), '{article['title']}')]]",
        timeout=3,
    )

    # Step 7: Click the heart icon again to unfavorite the article
    wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//div[contains(@class, 'article-preview') and .//h1[contains(text(), '{article['title']}')]]",
        ),
        timeout=3,
    ).find_element(
        AppiumBy.XPATH, ".//button[.//i[contains(@class, 'ion-heart')]]"
    ).click()

    # Step 8: Refresh the page and confirm the article is no longer in favorites
    driver.refresh()
    assert_element_not_present(
        driver,
        AppiumBy.XPATH,
        f"//div[contains(@class, 'article-preview') and .//h1[contains(text(), '{article['title']}')]]",
        timeout=3,
    )
