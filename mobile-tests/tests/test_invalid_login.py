import sys
import os

# Add parent directory to path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pages.login_page import LoginPage
from helpers.test_data import generate_random_user
from helpers.config import BASE_URL


@pytest.mark.mobile
def test_login_shows_error_for_invalid_credentials(driver):
    """Test that login form shows appropriate error message for non-existent user"""

    # Step 1: Generate random user data (not created in backend, so login should fail)
    user = generate_random_user()

    # Step 2: Navigate to the login page and try to log in with invalid credentials
    login_page = LoginPage(driver)
    login_page.navigate(BASE_URL)
    login_page.login(user["email"], user["password"])

    # Step 3: Verify that the error message for invalid credentials is shown
    error_messages = login_page.get_error_messages()
    assert "email or password" in error_messages[0].lower()
