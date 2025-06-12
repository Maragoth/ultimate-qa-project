import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pages.registration_page import RegistrationPage
from helpers.test_data import generate_random_user
from helpers.config import BASE_URL
from helpers.assertions import verify_logged_in


@pytest.mark.mobile
def test_user_can_register_via_ui(driver):
    """Test that a new user can successfully register through the UI"""

    # Generate random user data
    user = generate_random_user()

    # Initialize registration page and perform registration
    registration_page = RegistrationPage(driver)
    registration_page.navigate(BASE_URL)
    registration_page.register(user["username"], user["email"], user["password"])

    # Verify successful registration
    verify_logged_in(driver)
