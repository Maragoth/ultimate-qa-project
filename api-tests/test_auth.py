import pytest
import json
from uuid import uuid4
from utils.helpers import post_request, validate_schema, log_response

@pytest.mark.auth
def test_register_and_login(base_url):
    url = f"{base_url}/users"
    login_url = f"{base_url}/users/login"

    user_data = {
        "email": f"qa-tester-{uuid4()}@test.com",
        "username": f"qa-tester-{uuid4()}",
        "password": "Test123!"
    }

    # Rejestracja nowego użytkownika
    response = post_request(url, json_data={"user": user_data})
    log_response(response)

    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 1

    # Login nowego użytkownika
    response = post_request(login_url, json_data={"user": {
        "email": user_data["email"],
        "password": user_data["password"]
    }})
    log_response(response)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Walidacja schematu
    schema = {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "token": {"type": "string"},
                    "username": {"type": "string"}
                },
                "required": ["email", "token", "username"]
            }
        },
        "required": ["user"]
    }

    validate_schema(response.json(), schema)

    # Zapisanie danych do globalnej zmiennej testowej
    pytest.user_data = user_data


@pytest.mark.auth
def test_login_failure_wrong_password(base_url):
    url = f"{base_url}/users/login"

    payload = {
        "user": {
            "email": "qa@tester.com",
            "password": "WrongPass123!"
        }
    }

    response = post_request(url, json_data=payload)
    log_response(response)

    assert response.status_code == 403
    assert response.elapsed.total_seconds() < 1


@pytest.mark.auth
def test_register_duplicate_user(base_url):
    url = f"{base_url}/users"

    # Pobranie danych z poprzedniego testu
    user_data = getattr(pytest, "user_data", None)
    assert user_data is not None, "User data not found. Run test_register_and_login first."

    # Próba rejestracji z tymi samymi danymi
    response = post_request(url, json_data={"user": user_data})
    log_response(response)

    assert response.status_code == 422  # Expected Unprocessable Entity for duplicate
    assert response.elapsed.total_seconds() < 1
