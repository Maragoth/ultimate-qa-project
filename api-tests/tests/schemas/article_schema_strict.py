schema = {
    "type": "object",
    "properties": {
        "article": {
            "type": "object",
            "properties": {
                "slug": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "body": {"type": "string"},
                "tagList": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "createdAt": {"type": "string", "format": "date-time"},
                "updatedAt": {"type": "string", "format": "date-time"},
                "favorited": {"type": "boolean"},
                "favoritesCount": {"type": "integer"},
                "author": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "bio": {"type": "string"},
                        "image": {"type": "string"},
                        "following": {"type": "boolean"},
                    },
                    "required": ["username", "bio", "image", "following"],
                    "additionalProperties": False,
                },
            },
            "required": [
                "slug",
                "title",
                "description",
                "body",
                "tagList",
                "createdAt",
                "updatedAt",
                "favorited",
                "favoritesCount",
                "author",
            ],
            "additionalProperties": False,
        }
    },
    "required": ["article"],
    "additionalProperties": False,
}
