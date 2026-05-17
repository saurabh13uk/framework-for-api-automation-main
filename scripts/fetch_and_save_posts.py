from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.client import JsonPlaceholderClient
from config.settings import BASE_URL, FIRST_POSTS_OUTPUT, REQUEST_TIMEOUT, REQUIRED_POST_KEYS
from utils.file_writer import save_json_file


def validate_posts(posts: list[dict]) -> None:
    for index, post in enumerate(posts, start=1):
        missing_keys = REQUIRED_POST_KEYS - set(post)
        if missing_keys:
            raise AssertionError(f"Post at position {index} is missing keys: {sorted(missing_keys)}")


def main() -> None:
    client = JsonPlaceholderClient(BASE_URL, REQUEST_TIMEOUT)
    response = client.get_posts_response()

    if response.status_code != 200:
        raise AssertionError(f"Expected status code 200, got {response.status_code}")

    posts = response.json()
    if not isinstance(posts, list):
        raise AssertionError("Expected API response body to be a list of posts.")

    validate_posts(posts)
    saved_path = save_json_file(posts[:5], FIRST_POSTS_OUTPUT)
    print(f"Saved first 5 posts to {saved_path}")


if __name__ == "__main__":
    main()

