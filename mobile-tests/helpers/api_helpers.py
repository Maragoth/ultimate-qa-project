# helpers/api_helpers.py

import requests
from helpers.test_data import generate_random_user
import os

# Get API host from environment variable, default to localhost for local development
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "3000")
API_URL = f"http://{API_HOST}:{API_PORT}/api"

def create_random_user_via_api():
    user = generate_random_user()

    response = requests.post(
        f"{API_URL}/users",
        json={"user": {
            "username": user["username"],
            "email": user["email"],
            "password": user["password"]
        }}
    )

    response.raise_for_status()
    data = response.json()

    return {
        "username": data["user"]["username"],
        "email": data["user"]["email"],
        "password": user["password"],
        "token": data["user"]["token"]
    }

def create_article_via_api(token, article):
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(
        f"{API_URL}/articles",
        json={"article": article},
        headers=headers
    )
    response.raise_for_status()
    data = response.json()

    return {
        **article,
        "slug": data["article"]["slug"]
    }

def add_comment_via_api(token, slug, comment_body):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}"
    }
    response = requests.post(
        f"{API_URL}/articles/{slug}/comments",
        json={"comment": {"body": comment_body}},
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Failed to add comment: {response.status_code} {response.text}")

    return response.json()
