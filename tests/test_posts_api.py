import pytest

from config.settings import REQUIRED_POST_KEYS
from utils.file_writer import save_json_file


@pytest.mark.smoke
def test_get_posts_status_code_is_200(posts_response):
    assert posts_response.status_code == 200


@pytest.mark.contract
def test_get_posts_response_is_list(posts):
    assert isinstance(posts, list)
    assert posts, "Expected posts API to return at least one post."


@pytest.mark.contract
@pytest.mark.parametrize("required_key", sorted(REQUIRED_POST_KEYS))
def test_each_post_contains_required_key(posts, required_key):
    missing_post_ids = [post.get("id", f"index-{index}") for index, post in enumerate(posts) if required_key not in post]
    assert not missing_post_ids, f"Missing key '{required_key}' in posts: {missing_post_ids}"


@pytest.mark.contract
def test_each_post_contains_all_required_keys(posts):
    for index, post in enumerate(posts, start=1):
        missing_keys = REQUIRED_POST_KEYS - set(post)
        assert not missing_keys, f"Post at position {index} is missing keys: {sorted(missing_keys)}"


def test_save_first_five_posts_to_json_file(posts, tmp_path):
    output_file = tmp_path / "first_5_posts.json"
    saved_path = save_json_file(posts[:5], str(output_file))

    assert saved_path.exists()
    assert saved_path.read_text(encoding="utf-8").strip().startswith("[")

