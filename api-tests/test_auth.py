import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def test_login_success():
    payload = {"user": {"email": "demo@demo.com", "password": "demo"}}
    response = requests.post(f"{BASE_URL}/users/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json()["user"]
