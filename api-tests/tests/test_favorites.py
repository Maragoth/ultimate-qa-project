import pytest
import json
from pathlib import Path
from uuid import uuid4
from utils.helpers import (
    authorized_post_request,
    authorized_delete_request,
    authorized_get_request,
    validate_schema,
    log_response,
    create_test_article,
)


@pytest.mark.favorites
def test_favorite_unfavorite_article(base_url, auth_token):
    # Create a new article to test favoriting
    article = create_test_article(base_url, auth_token)
    slug = article["slug"]
    favorite_url = f"{base_url}/articles/{slug}/favorite"
    article_url = f"{base_url}/articles/{slug}"

    # === POST: Favorite the article ===
    response = authorized_post_request(favorite_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Validate response schema
    schema_path = Path(__file__).parent / "schemas" / "article.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    # === DELETE: Unfavorite the article ===
    response = authorized_delete_request(favorite_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Validate schema again after unfavoriting
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    # === GET: Confirm article is not favorited ===
    response = authorized_get_request(article_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1
    assert not response.json()["article"]["favorited"]
