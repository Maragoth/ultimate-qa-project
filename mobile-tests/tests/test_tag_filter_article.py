import pytest
from appium.webdriver.common.appiumby import AppiumBy
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.auth import setup_user_session
from helpers.waits import wait_for_element, wait_for_element_clickable
from helpers.test_data import random_number, generate_article
import os


@pytest.mark.mobile
@pytest.mark.xfail(
    reason="Known issue: Tag click redirects to article instead of filtering by tag"
)
def test_tag_filter_article(driver):
    """Test filtering articles by clicking a tag below an article.

    Known Issue:
    - When clicking a tag below an article, it redirects to the article preview
    - Instead, it should filter articles by that tag (like Popular Tags feature)
    - Bug documented in docs/bug-tag-click-redirect/
    """

    # Create test user and set up session
    user = create_random_user_via_api()
    setup_user_session(driver, user["token"], user["username"])

    # Generate unique tag
    tag = f"Tag-{random_number()}"

    # Create two articles with the same tag via API
    article1_data = generate_article("Tagged-Article-A", tag)
    article2_data = generate_article("Tagged-Article-B", tag)

    article1 = create_article_via_api(user["token"], article1_data)
    article2 = create_article_via_api(user["token"], article2_data)

    # Navigate to Global Feed
    frontend_url = f"http://{os.environ['FRONTEND_HOST']}:{os.environ['FRONTEND_PORT']}"
    driver.get(frontend_url)

    global_feed = wait_for_element_clickable(
        driver, (AppiumBy.XPATH, "//a[contains(text(), 'Global Feed')]")
    )
    global_feed.click()

    # Find article and click its tag
    article_preview = wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//div[contains(@class, 'article-preview') and contains(., '{article1['title']}')]",
        ),
    )

    # Click the tag using the exact HTML structure
    tag_element = wait_for_element_clickable(
        driver,
        (
            AppiumBy.XPATH,
            f"//*[@id='root']//li[contains(@class, 'tag-default') and text()='{tag}']",
        ),
    )
    tag_element.click()

    # What should happen (but currently doesn't due to the bug):
    # The page should show the tag filter view with:
    # 1. Active nav link showing the tag
    tag_nav = wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//a[contains(@class, 'nav-link') and contains(@class, 'active') and contains(., '{tag}')]",
        ),
    )

    # 2. Article previews section should show both articles with this tag
    article_previews = driver.find_elements(AppiumBy.CLASS_NAME, "article-preview")

    # These assertions will fail due to the known bug
    assert tag_nav.is_displayed(), "Tag should be shown as active filter in nav"
    assert len(article_previews) == 2, "Should show both articles with the tag"

    # 3. Verify the specific articles are shown
    article1_element = wait_for_element(
        driver, (AppiumBy.XPATH, f"//h1[contains(text(), '{article1['title']}')]")
    )
    article2_element = wait_for_element(
        driver, (AppiumBy.XPATH, f"//h1[contains(text(), '{article2['title']}')]")
    )

    assert article1_element.is_displayed(), "First tagged article should be visible"
    assert article2_element.is_displayed(), "Second tagged article should be visible"
