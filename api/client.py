from typing import Any, Dict, List, Optional

import requests
from requests import Response, Session


class JsonPlaceholderClient:
    """Requests-based API client for JSONPlaceholder."""

    def __init__(self, base_url: str, timeout: int = 10, session: Optional[Session] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def get(self, endpoint: str) -> Response:
        url = f"{self.base_url}{endpoint}"
        try:
            return self.session.get(url, timeout=self.timeout)
        except requests.RequestException as exc:
            raise RuntimeError(f"GET request failed for {url}: {exc}") from exc

    def get_posts_response(self) -> Response:
        from api.endpoints import POSTS

        return self.get(POSTS)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Response:
        url = f"{self.base_url}{endpoint}"
        try:
            return self.session.post(url, json=json, timeout=self.timeout)
        except requests.RequestException as exc:
            raise RuntimeError(f"POST request failed for {url}: {exc}") from exc

    def delete(self, endpoint: str) -> Response:
        url = f"{self.base_url}{endpoint}"
        try:
            return self.session.delete(url, timeout=self.timeout)
        except requests.RequestException as exc:
            raise RuntimeError(f"DELETE request failed for {url}: {exc}") from exc

    def get_posts(self) -> List[Dict[str, Any]]:
        response = self.get_posts_response()
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("Expected posts API to return a list.")
        return payload
