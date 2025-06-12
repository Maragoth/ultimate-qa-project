import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pages.login_page import LoginPage
from helpers.test_data import generate_random_user
from helpers.config import BASE_URL


@pytest.mark.mobile
def test_login_shows_error_for_invalid_credentials(driver):
    """Test that login form shows appropriate error message for non-existent user"""

    # Generate test user data (not creating in database - should fail)
    user = generate_random_user()

    # Navigate to login page and attempt login
    login_page = LoginPage(driver)
    login_page.navigate(BASE_URL)
    login_page.login(user["email"], user["password"])

    # Verify error message appears
    error_messages = login_page.get_error_messages()
    assert "email or password" in error_messages[0].lower()
