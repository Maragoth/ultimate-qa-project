import pytest
import random
import logging
from pages.article_page import ArticlePage
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.test_data import generate_article
from helpers.config import BASE_URL
from helpers.auth import login_via_api_and_set_token

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.mark.mobile
def test_user_can_edit_article(driver):
    """Test that a logged-in user can edit an existing article"""

    # Create user and article via API
    user = create_random_user_via_api()
    tag = f"TestTag-{random.randint(0, 999999)}"

    # Generate original and updated article data
    original_article = generate_article("Edit-Original", tag)
    updated_article = generate_article("Edit-Updated", tag)

    # Create article via API and login
    created_article = create_article_via_api(user["token"], original_article)
    login_via_api_and_set_token(driver, user)

    # Initialize article page
    article_page = ArticlePage(driver)

    # Navigate directly to the article using its slug
    driver.get(f"{BASE_URL}/article/{created_article['slug']}")

    # Edit the article
    article_page.click_edit_button()
    article_page.edit_article(
        updated_article["title"],
        updated_article["description"],
        updated_article["body"],
    )

    # Verify article was updated
    assert article_page.get_article_title() == updated_article["title"]
