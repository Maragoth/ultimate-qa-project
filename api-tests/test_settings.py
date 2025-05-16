import pytest
import json
from pathlib import Path
from utils.helpers import authorized_put_request, authorized_get_request, validate_schema, log_response

@pytest.mark.settings
def test_update_user_settings(base_url, auth_token):
    url = f"{base_url}/user"

    update_payload = {
        "user": {
            "bio": "Updated bio from API test",
            "image": "https://api.realworld.io/images/demo-avatar.png"
        }
    }

    response = authorized_put_request(url, auth_token, json_data=update_payload)
    log_response(response)
    assert response.status_code == 200

    schema_path = Path(__file__).parent / "schemas" / "user.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validate_schema(response.json(), schema)
    updated_user = response.json()["user"]
    assert updated_user["bio"] == update_payload["user"]["bio"]
    assert updated_user["image"] == update_payload["user"]["image"]

    # Verify GET /user (optional)
    response = authorized_get_request(url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.json()["user"]["bio"] == update_payload["user"]["bio"]
