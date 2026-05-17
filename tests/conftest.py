import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.client import JsonPlaceholderClient
from config.settings import BASE_URL, REQUEST_TIMEOUT
from utils.api_reporter import ApiExecutionReporter
from utils.logger import get_logger


api_reporter = ApiExecutionReporter()
logger = get_logger()


@pytest.fixture(scope="session")
def api_client() -> JsonPlaceholderClient:
    return JsonPlaceholderClient(BASE_URL, REQUEST_TIMEOUT)


@pytest.fixture(scope="session")
def posts_response(api_client):
    return api_client.get_posts_response()


@pytest.fixture(scope="session")
def posts(posts_response):
    posts_response.raise_for_status()
    return posts_response.json()


@pytest.fixture
def api_recorder():
    def record(name, method, response, request_body=None, validation_status="Passed"):
        try:
            response_body = response.json()
        except ValueError:
            response_body = response.text

        log_lines = [
            f"API Name: {name}",
            f"Method: {method}",
            f"URL: {response.url}",
            f"Status Code: {response.status_code}",
            f"Response Time: {response.elapsed.total_seconds():.3f} seconds",
            f"Validation: {validation_status}",
        ]

        if request_body is not None:
            log_lines.append(f"Request Body: {request_body}")

        for line in log_lines:
            logger.info(line)

        api_reporter.record(
            name=name,
            method=method,
            url=response.url,
            status_code=response.status_code,
            response_time_seconds=response.elapsed.total_seconds(),
            request_body=request_body,
            response_body=response_body,
            logs=log_lines,
        )

    return record


def pytest_sessionfinish(session, exitstatus):
    api_reporter.write_reports("reports")