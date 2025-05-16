import pytest
from utils.helpers import authorized_post_request, authorized_delete_request, authorized_get_request, log_response

@pytest.mark.favorites
def test_favorite_unfavorite_article(base_url, auth_token):
    slug = "Try-to-bypass-the-SCSI-sensor-maybe-it-will-generate-the-1080p-card!-1"
    favorite_url = f"{base_url}/articles/{slug}/favorite"
    article_url = f"{base_url}/articles/{slug}"

    # Favorite
    response = authorized_post_request(favorite_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.json()["article"]["favorited"] is True

    # Unfavorite
    response = authorized_delete_request(favorite_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.json()["article"]["favorited"] is False
