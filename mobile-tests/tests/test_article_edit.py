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

    # Step 1: Create a user for authentication
    user = create_random_user_via_api()
    tag = f"TestTag-{random.randint(0, 999999)}"

    # Step 2: Generate original and updated article content
    original_article = generate_article("Edit-Original", tag)
    updated_article = generate_article("Edit-Updated", tag)

    # Step 3: Create the original article and authenticate the user in browser
    created_article = create_article_via_api(user["token"], original_article)
    login_via_api_and_set_token(driver, user)

    # Step 4: Initialize the article page object
    article_page = ArticlePage(driver)

    # Step 5: Navigate directly to the article page using its unique slug
    driver.get(f"{BASE_URL}/article/{created_article['slug']}")

    # Step 6: Enter article edit mode and update the content
    article_page.click_edit_button()
    article_page.edit_article(
        updated_article["title"],
        updated_article["description"],
        updated_article["body"],
    )

    # Step 7: Assert that the article title reflects the new changes
    assert article_page.get_article_title() == updated_article["title"]
