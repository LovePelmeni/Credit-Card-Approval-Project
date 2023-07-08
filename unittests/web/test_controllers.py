import pytest, fastapi.testclient
from ...src.web import settings
import os.path

TEST_CLIENT_BASE_URL = "http://testserver"

@pytest.fixture(scope='module')
def client():
    new_client = fastapi.testclient.TestClient(
        app=settings.application,
        base_url=TEST_CLIENT_BASE_URL
    )
    return new_client

def get_client_url():
    return TEST_CLIENT_BASE_URL

def test_prediction_controller(client):
    client_base_url = os.path.join(
        get_client_url(),
        "/predict/card/approval/"
    )
    response = client.post(client_base_url)
    return response.status_code

def test_fail_predictioN_controller(client):
    pass

def test_fail_because_invalid_data(client):
    pass 