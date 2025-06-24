import pytest
from utils.helpers import authorized_put_request, authorized_get_request, log_response
from uuid import uuid4


@pytest.mark.api
def test_put_user_partial_update(auth_token, base_url):
    # GIVEN: Unikalne wartości do aktualizacji
    new_bio = f"Updated bio {uuid4().hex[:4]}"
    url = f"{base_url}/user"
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }

    # WHEN: Wysyłamy tylko jedno pole do aktualizacji
    payload = {"user": {"bio": new_bio}}
    response = authorized_put_request(url, auth_token, json_data=payload)
    log_response(response)

    # THEN: Odpowiedź 200 OK i zmienione pole
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1.0
    assert response.json()["user"]["bio"] == new_bio

    # AND: Inne pola pozostają niezmienione
    get_response = authorized_get_request(url, auth_token)
    log_response(get_response)
    user_data = get_response.json()["user"]
    assert user_data["bio"] == new_bio
    assert "email" in user_data
    assert "username" in user_data
    assert user_data["email"].endswith("@mail.com") or user_data["email"].endswith(
        "@tester.com"
    )
