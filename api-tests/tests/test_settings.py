import pytest
import json
from pathlib import Path
from utils.helpers import (
    authorized_put_request,
    authorized_get_request,
    validate_schema,
    log_response,
)


@pytest.mark.settings
def test_update_user_settings(base_url, auth_token):
    url = f"{base_url}/user"

    # === PUT: Update user bio and image ===
    update_payload = {
        "user": {
            "bio": "Updated bio from API test",
            "image": "https://api.realworld.io/images/demo-avatar.png",
        }
    }

    response = authorized_put_request(url, auth_token, json_data=update_payload)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # === GET: Fetch updated user profile ===
    response = authorized_get_request(url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    user = response.json()["user"]
    assert user["bio"] == update_payload["user"]["bio"]
    assert user["image"] == update_payload["user"]["image"]

    # Validate schema
    schema_path = Path(__file__).parent / "schemas" / "user.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)
