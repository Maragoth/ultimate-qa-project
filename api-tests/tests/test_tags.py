import pytest
import json
from pathlib import Path
from utils.helpers import (
    authorized_get_request,
    validate_schema,
    log_response,
)


@pytest.mark.tags
def test_get_tags(base_url, auth_token):
    # === GET: Fetch available tags ===
    url = f"{base_url}/tags"
    response = authorized_get_request(url, auth_token)
    log_response(response)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Validate response schema
    schema_path = Path(__file__).parent / "schemas" / "tags.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)
