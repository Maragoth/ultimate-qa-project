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

    # Step 1: Create test user and generate article content
    user = create_random_user_via_api()
    tag = f"TestTag-{random.randint(0, 999999)}"
    article = generate_article("ReadMore", tag)

    # Step 2: Create the article via API using the test user's token
    created_article = create_article_via_api(user["token"], article)

    # Step 3: Log in by injecting auth token into local storage
    login_via_api_and_set_token(driver, user)

    # Step 4: Initialize the article page object for UI interaction
    article_page = ArticlePage(driver)

    # Step 5: Navigate to the home page
    driver.get(BASE_URL)

    # Step 6: Wait for the feed toggle and click on 'Global Feed'
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

    # Step 7: Locate the article and click the 'Read more' link
    article_page.click_read_more_for_article(article["title"])

    # Step 8: Verify that the article detail page matches the expected title
    assert article_page.get_article_title() == article["title"]
