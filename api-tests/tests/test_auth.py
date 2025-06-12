import pytest
import json
from uuid import uuid4
from pathlib import Path
from utils.helpers import post_request, validate_schema, log_response


@pytest.mark.auth
def test_register_and_login(base_url):
    url = f"{base_url}/users"
    login_url = f"{base_url}/users/login"

    user_data = {
        "email": f"qa-tester-{uuid4()}@test.com",
        "username": f"qa-tester-{uuid4()}",
        "password": "Test123!",
    }

    # Register new user
    response = post_request(url, json_data={"user": user_data})
    log_response(response)
    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 1

    # Login with new user
    response = post_request(
        login_url,
        json_data={
            "user": {"email": user_data["email"], "password": user_data["password"]}
        },
    )
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Validate schema from file
    schema_path = Path(__file__).parent / "schemas" / "user.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    # Store user data for reuse
    pytest.user_data = user_data


@pytest.mark.auth
def test_login_failure_wrong_password(base_url):
    url = f"{base_url}/users/login"
    payload = {"user": {"email": "qa@tester.com", "password": "WrongPass123!"}}

    response = post_request(url, json_data=payload)
    log_response(response)
    assert response.status_code == 403
    assert response.elapsed.total_seconds() < 1


@pytest.mark.auth
def test_register_duplicate_user(base_url):
    url = f"{base_url}/users"
    user_data = getattr(pytest, "user_data", None)
    assert (
        user_data is not None
    ), "User data not found. Run test_register_and_login first."

    # Try registering the same user again
    response = post_request(url, json_data={"user": user_data})
    log_response(response)
    assert response.status_code == 422
    assert response.elapsed.total_seconds() < 1
