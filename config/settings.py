import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
FIRST_POSTS_OUTPUT = os.getenv("FIRST_POSTS_OUTPUT", "data/first_5_posts.json")
REQUIRED_POST_KEYS = {"userId", "id", "title", "body"}

