import pytest
from utils.helpers import post_request, validate_schema

@pytest.mark.auth
def test_login_success(base_url):
    url = f"{base_url}/users/login"
    payload = {
"user": {
    "email": "qa@tester.com",
    "password": "Test123!"
}

    }
    response = post_request(url, json_data=payload)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    response_json = response.json()
    assert "user" in response_json
    assert "token" in response_json["user"]

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

    validate_schema(response_json, schema)


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
    assert response.status_code == 403
    assert response.elapsed.total_seconds() < 1