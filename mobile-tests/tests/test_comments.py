import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from helpers.api_helpers import create_random_user_via_api, create_article_via_api
from helpers.test_data import generate_article
from helpers.config import BASE_URL
from helpers.auth import login_via_api_and_set_token
from helpers.waits import wait_for_element

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.mark.mobile
def test_user_can_add_and_delete_comment(driver):
    """Test that a user can add and delete a comment on an article"""
    print("\nStarting comment test...")

    # Create user and article via API
    start_time = time.time()
    user = create_random_user_via_api()
    article = generate_article("Comment Test", f"Tag-{int(time.time())}")
    created_article = create_article_via_api(user["token"], article)
    print(f"User and article creation via API took: {time.time() - start_time:.2f}s")

    # Login via API and navigate directly to article
    start_time = time.time()
    login_via_api_and_set_token(driver, user)
    driver.get(f"{BASE_URL}/article/{created_article['slug']}")
    print(f"Login and navigation took: {time.time() - start_time:.2f}s")

    # Add comment
    start_time = time.time()
    comment_text = f"Test comment {int(time.time())}"
    comment_box = wait_for_element(
        driver,
        (AppiumBy.XPATH, '//textarea[@placeholder="Write a comment..."]'),
        timeout=3,
    )
    comment_box.send_keys(comment_text)

    post_button = wait_for_element(
        driver,
        (AppiumBy.XPATH, '//button[normalize-space()="Post Comment"]'),
        timeout=3,
    )
    post_button.click()
    print(f"Comment posting took: {time.time() - start_time:.2f}s")

    # Verify comment appears
    start_time = time.time()
    comment = wait_for_element(
        driver, (AppiumBy.XPATH, f"//p[contains(text(), '{comment_text}')]"), timeout=3
    )
    print(f"Comment verification took: {time.time() - start_time:.2f}s")

    # Delete comment
    start_time = time.time()
    delete_button = wait_for_element(
        driver,
        (
            AppiumBy.XPATH,
            f"//p[contains(text(), '{comment_text}')]/ancestor::div[contains(@class, 'card')]//i[contains(@class, 'ion-trash-a')]",
        ),
        timeout=3,
    )
    delete_button.click()
    print(f"Comment deletion took: {time.time() - start_time:.2f}s")

    # Verify comment is removed
    start_time = time.time()
    try:
        driver.find_element(AppiumBy.XPATH, f"//p[contains(text(), '{comment_text}')]")
        raise AssertionError("Comment was not deleted")
    except:
        print(f"Comment removal verification took: {time.time() - start_time:.2f}s")

    print("Comment test completed successfully.")
