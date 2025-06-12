import pytest
import random
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.article_page import ArticlePage
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.test_data import generate_article
from helpers.config import BASE_URL
from helpers.auth import login_via_api_and_set_token
from helpers.waits import wait_for_element
from appium.webdriver.common.appiumby import AppiumBy

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.mark.mobile
def test_user_can_delete_article(driver):
    """Test that a logged-in user can delete their article"""
    # Create user and article via API
    user = create_random_user_via_api()
    article = generate_article("Delete-Test", f"TestTag-{random.randint(0, 999999)}")
    created_article = create_article_via_api(user["token"], article)

    # Login and navigate to article
    login_via_api_and_set_token(driver, user)
    driver.get(f"{BASE_URL}/article/{created_article['slug']}")

    # Verify we're on the correct article page
    article_title = wait_for_element(driver, (AppiumBy.TAG_NAME, "h1"), timeout=3).text
    assert (
        article_title == article["title"]
    ), f"Wrong article page. Expected '{article['title']}', got '{article_title}'"

    # Delete the article
    article_page = ArticlePage(driver)
    article_page.delete_article()

    # Quick check that article is gone from feed
    wait_for_element(
        driver, (AppiumBy.XPATH, "//a[normalize-space()='Global Feed']"), timeout=1
    ).click()

    assert (
        len(
            driver.find_elements(
                AppiumBy.XPATH, f"//h1[contains(text(), '{article['title']}')]"
            )
        )
        == 0
    ), "Article still visible after deletion"
