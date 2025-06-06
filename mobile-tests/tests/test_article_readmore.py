import pytest
import random
import logging
from pages.article_page import ArticlePage
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.test_data import generate_article
from helpers.config import BASE_URL
from helpers.auth import login_via_api_and_set_token
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.mark.mobile
def test_user_can_open_article_using_read_more(driver):
    """Test that a user can open an article using the Read more link"""

    # Create user and article via API
    user = create_random_user_via_api()
    tag = f"TestTag-{random.randint(0, 999999)}"
    article = generate_article("ReadMore", tag)

    # Create article via API
    created_article = create_article_via_api(user["token"], article)

    # Login via API and set token
    login_via_api_and_set_token(driver, user)

    # Initialize article page
    article_page = ArticlePage(driver)

    # Go to home page
    driver.get(BASE_URL)

    # Wait for feed toggle and click Global Feed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, "//div[contains(@class, 'feed-toggle')]")
        )
    )
    global_feed = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, "//a[contains(text(), 'Global Feed')]")
        )
    )
    global_feed.click()
    logging.info("Clicked on Global Feed tab")

    # Find and click Read more on the correct article
    article_page.click_read_more_for_article(article["title"])

    # Verify we're on the correct article page
    assert article_page.get_article_title() == article["title"]
