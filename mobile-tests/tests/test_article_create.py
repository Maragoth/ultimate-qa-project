import pytest
import random
import logging
from pages.article_page import ArticlePage
from helpers.api_helpers import create_random_user_via_api
from helpers.test_data import generate_article
from helpers.config import BASE_URL
from helpers.auth import login_via_api_and_set_token

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.mark.mobile
def test_user_can_create_article(driver):
    """Test that a logged-in user can create a new article"""

    # Create user and login via API
    user = create_random_user_via_api()
    login_via_api_and_set_token(driver, user)

    # Initialize article page and generate test data
    article_page = ArticlePage(driver)
    tag = f"TestTag-{random.randint(0, 999999)}"
    article = generate_article("Create", tag)

    # Navigate to editor and create article
    article_page.navigate_to_editor(BASE_URL)
    article_page.create_article(
        article["title"], article["description"], article["body"], [tag]
    )

    # Verify article was created
    assert article_page.get_article_title() == article["title"]
