import pytest
import random
import logging
import time
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
    print("\nStarting article creation test...")

    # Create user and login via API
    start_time = time.time()
    user = create_random_user_via_api()
    print(f"User creation via API took: {time.time() - start_time:.2f}s")

    start_time = time.time()
    login_via_api_and_set_token(driver, user)
    print(f"Login via API and token setup took: {time.time() - start_time:.2f}s")

    # Initialize article page and generate test data
    start_time = time.time()
    article_page = ArticlePage(driver)
    tag = f"TestTag-{random.randint(0, 999999)}"
    article = generate_article("Create", tag)
    print(f"Test data generation took: {time.time() - start_time:.2f}s")

    # Navigate to editor and create article
    start_time = time.time()
    article_page.navigate_to_editor(BASE_URL)
    print(f"Navigation to editor took: {time.time() - start_time:.2f}s")

    start_time = time.time()
    article_page.create_article(
        article["title"], article["description"], article["body"], [tag]
    )
    print(f"Article creation took: {time.time() - start_time:.2f}s")

    # Verify article was created
    start_time = time.time()
    assert article_page.get_article_title() == article["title"]
    print(f"Article verification took: {time.time() - start_time:.2f}s")

    print("Article creation test completed.")
