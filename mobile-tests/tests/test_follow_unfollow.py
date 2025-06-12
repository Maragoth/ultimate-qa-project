import pytest
import random
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from helpers.api_helpers import (
    create_random_user_via_api,
    create_article_via_api,
    follow_user_via_api,
    unfollow_user_via_api,
    get_feed_articles,
)
from helpers.test_data import generate_article
from helpers.config import BASE_URL, API_URL
from helpers.auth import login_via_api_and_set_token
from helpers.waits import wait_for_element


@pytest.mark.mobile
def test_user_can_follow_unfollow_and_see_feed_changes(driver):
    """Test that a user can follow/unfollow another user and see feed changes"""
    print("\n=== Starting Follow/Unfollow Test ===")

    # Create author (userB) and their article
    print("\n1. Creating author and article...")
    start_time = time.time()
    author = create_random_user_via_api()
    print(f"   ✓ Created author: {author['username']}")

    article = generate_article("FollowFlow", f"FollowTag-{random.randint(0, 99999)}")
    created_article = create_article_via_api(author["token"], article)
    print(f"   ✓ Created article: '{article['title']}'")
    print(f"   ⏱️  Setup took: {time.time() - start_time:.2f}s")

    # Create follower (userA) and login
    print("\n2. Creating follower and logging in...")
    start_time = time.time()
    follower = create_random_user_via_api()
    print(f"   ✓ Created follower: {follower['username']}")

    login_via_api_and_set_token(driver, follower)
    print("   ✓ Logged in via API")
    print(f"   ⏱️  Setup took: {time.time() - start_time:.2f}s")

    # Follow author via API for stability
    print("\n3. Following author...")
    start_time = time.time()
    follow_user_via_api(follower["token"], author["username"])
    print(f"   ✓ Followed {author['username']}")
    print(f"   ⏱️  API call took: {time.time() - start_time:.2f}s")

    # Go to Your Feed and verify article appears
    print("\n4. Checking Your Feed for article...")
    start_time = time.time()
    driver.get(f"{BASE_URL}/")
    print("   ✓ Navigated to home page")

    your_feed = wait_for_element(
        driver, (AppiumBy.XPATH, "//a[normalize-space()='Your Feed']"), timeout=3
    )
    print("   ✓ Found Your Feed tab")
    your_feed.click()
    print("   ✓ Clicked Your Feed")

    # Poll feed until article appears (max 10 attempts)
    article_found = False
    attempts = 0
    print("\n   Polling feed for article...")
    for attempt in range(10):
        attempts += 1
        feed_articles = get_feed_articles(follower["token"])
        if any(a["title"] == article["title"] for a in feed_articles):
            article_found = True
            print(f"   ✓ Found article after {attempts} attempts")
            break
        print(f"   • Attempt {attempt + 1}: Article not found yet...")
        time.sleep(1)

    assert (
        article_found
    ), f"Article '{article['title']}' not found in feed after following author"
    print(f"   ⏱️  Verification took: {time.time() - start_time:.2f}s")

    # Unfollow author via API
    print("\n5. Unfollowing author...")
    start_time = time.time()
    unfollow_user_via_api(follower["token"], author["username"])
    print(f"   ✓ Unfollowed {author['username']}")
    print(f"   ⏱️  API call took: {time.time() - start_time:.2f}s")

    # Verify article disappears from Your Feed
    print("\n6. Verifying article is gone...")
    start_time = time.time()
    driver.get(f"{BASE_URL}/")
    print("   ✓ Navigated to home page")

    your_feed = wait_for_element(
        driver, (AppiumBy.XPATH, "//a[normalize-space()='Your Feed']"), timeout=1
    )
    print("   ✓ Found Your Feed tab")
    your_feed.click()
    print("   ✓ Clicked Your Feed")

    # Quick check that article is gone
    articles = driver.find_elements(
        AppiumBy.XPATH, f"//h1[contains(text(), '{article['title']}')]"
    )
    assert len(articles) == 0, "Article still visible in feed after unfollowing"
    print("   ✓ Confirmed article is not visible")
    print(f"   ⏱️  Final verification took: {time.time() - start_time:.2f}s")

    print("\n=== Test Completed Successfully! ===")
