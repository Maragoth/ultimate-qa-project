import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.api_helpers import create_random_user_via_api
from helpers.auth import login_via_api_and_set_token
from helpers.config import BASE_URL
from helpers.waits import wait_for_element


@pytest.mark.mobile
def test_click_tag_in_sidebar_and_verify_articles(driver):
    """Test clicking a tag in sidebar and verifying articles contain that tag"""

    # Step 1: Create a test user using the API
    user = create_random_user_via_api()

    # Step 2: Log in by injecting token into the browser session
    login_via_api_and_set_token(driver, user)

    # Step 3: Navigate to the homepage
    driver.get(BASE_URL)

    # Step 4: Locate and click the first tag from the Popular Tags sidebar
    popular_tag = wait_for_element(
        driver, (AppiumBy.CSS_SELECTOR, ".tag-list a"), timeout=10
    )
    tag_name = popular_tag.text.strip()
    popular_tag.click()

    # Step 5: Verify that the selected tag appears in the feed toggle area
    feed_toggle = wait_for_element(
        driver, (AppiumBy.CSS_SELECTOR, ".feed-toggle"), timeout=10
    )
    assert tag_name in feed_toggle.text

    # Step 6: Wait for article previews to load
    article_previews = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((AppiumBy.CSS_SELECTOR, ".article-preview"))
    )
    assert len(article_previews) > 0

    # Step 7: Check that each displayed article includes the selected tag
    for article in article_previews:
        tags = article.find_elements(AppiumBy.CSS_SELECTOR, "ul.tag-list li")
        tag_texts = [tag.text.strip() for tag in tags]
        assert (
            tag_name in tag_texts
        ), f"Tag {tag_name} not found in article tags: {tag_texts}"
