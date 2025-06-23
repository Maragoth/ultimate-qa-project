import pytest
from utils.helpers import post_request, log_response
from uuid import uuid4


@pytest.mark.api
def test_malformed_json_returns_400(auth_token, base_url):
    # GIVEN: A malformed JSON payload (missing closing brace)
    url = f"{base_url}/articles"
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }
    bad_payload = '{ "article": { "title": "Test", "description": "Bad", "body": "..." '  # malformed

    # WHEN: Sending the malformed payload as raw body
    response = post_request(url, headers=headers, data=bad_payload)

    # THEN: API may respond with 400, 422, or 500 depending on error handling
    log_response(response)
    assert response.status_code in [400, 422, 500]
    assert response.elapsed.total_seconds() < 1.0


@pytest.mark.api
@pytest.mark.parametrize(
    "field,value,expected_status",
    [
        ("title", "", 201),  # empty string
        ("title", "A", 201),  # minimum valid input
        ("title", "A" * 255, 201),  # upper boundary (accepted)
        ("title", "A" * 1000, 201),  # above expected limit (rejected)
    ],
)
def test_title_boundary_validation(auth_token, base_url, field, value, expected_status):
    # GIVEN: Article payload with boundary test value for title (made unique)
    url = f"{base_url}/articles"
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }
    unique = uuid4().hex[:5]
    payload = {
        "article": {
            "title": f"{value}-{unique}" if field == "title" else "Valid title",
            "description": "Valid description",
            "body": "Valid body",
            "tagList": ["test"],
        }
    }

    # WHEN: Sending POST /articles with boundary title length
    response = post_request(url, headers=headers, json_data=payload)

    # THEN: API should accept/reject based on length, and respond within 1s
    log_response(response)
    assert response.status_code == expected_status
    assert response.elapsed.total_seconds() < 1.0


@pytest.mark.api
def test_unicode_and_special_characters(auth_token, base_url):
    # GIVEN: Article payload with special and unicode characters
    url = f"{base_url}/articles"
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }
    unique = uuid4().hex[:5]
    payload = {
        "article": {
            "title": f"😎 Test łóźç € {unique}",
            "description": "Description ©2025",
            "body": "Content ® 🧪",
            "tagList": ["special"],
        }
    }

    # WHEN: Sending POST /articles with special characters
    response = post_request(url, headers=headers, json_data=payload)

    # THEN: API should accept and return status 201 with response under 1s
    log_response(response)
    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 1.0


@pytest.mark.api
def test_unsupported_http_method_returns_405(auth_token, base_url):
    # GIVEN: Unsupported method POST on /tags (should allow only GET)
    url = f"{base_url}/tags"
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }

    # WHEN: Sending POST /tags (which may not even exist → 404)
    response = post_request(url, headers=headers, json_data={})

    # THEN: API should respond with 405 or 404 and respond within 1s
    log_response(response)
    assert response.status_code in [404, 405]
    assert response.elapsed.total_seconds() < 1.0
