# helpers/test_data.py

import time
import random


def generate_random_user():
    user_id = f"{int(time.time())}-{random.randint(0, 999999)}"
    return {
        "username": f"user{user_id}",
        "email": f"user{user_id}@example.com",
        "password": "Test123!@#",
    }


def generate_article(base_name, tag):
    article_id = random.randint(0, 999999)
    return {
        "title": f"Test Title - {base_name} - {article_id}",
        "description": "Test description",
        "body": "This is the body of the test article.",
        "tagList": [tag],
    }


def random_number():
    """Generate a random number for unique identifiers"""
    return int(time.time() * 1000) + random.randint(0, 999999)
