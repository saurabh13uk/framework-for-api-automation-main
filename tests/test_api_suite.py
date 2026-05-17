import pytest
from jsonschema import validate

from api.endpoints import READ_ENDPOINTS
from tests.schemas import ENDPOINT_SCHEMAS


@pytest.mark.smoke
@pytest.mark.parametrize("endpoint", READ_ENDPOINTS)
def test_multiple_endpoints_return_200(api_client, endpoint):
    response = api_client.get(endpoint)

    assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.parametrize("endpoint", READ_ENDPOINTS)
def test_response_time_is_less_than_two_seconds(api_client, endpoint):
    response = api_client.get(endpoint)

    assert response.elapsed.total_seconds() < 2, (
        f"{endpoint} response time was {response.elapsed.total_seconds():.3f} seconds"
    )


@pytest.mark.contract
@pytest.mark.parametrize("endpoint", READ_ENDPOINTS)
def test_endpoint_schema_validation(api_client, endpoint):
    response = api_client.get(endpoint)
    response.raise_for_status()
    payload = response.json()

    assert isinstance(payload, list)
    assert payload, f"Expected {endpoint} to return at least one item."
    validate(instance=payload[0], schema=ENDPOINT_SCHEMAS[endpoint])
