import pytest
from ...src.modeling import feature_form, exceptions
from ...src import settings

import pytest
from fastapi.testclient import TestClient
import unittest.mock
import pydantic

def load_valid_dataset() -> pydantic.BaseModel:

    return feature_form.CardApprovalFeatures()

@pytest.fixture(scope='module')
def test_client():
    return TestClient(settings.application)

def test_prediction_controller(test_client):
    dataset = load_valid_dataset()
    response = test_client.post("/predict/card/approval/", json=dataset.model_dump())
    assert hasattr(response, 'status_code')
    assert response.status_code in (200, 201)
     
def test_fail_prediction_controller(test_client):
    
    dataset = load_valid_dataset()

    with unittest.mock.patch(
    target="...src.modeling.modeling.CreditCardApprover.predict_card_approval",
    side_effect=exceptions.PredictionFailed,
    ) as mocked_response:

        response = test_client.post("/predict/card/approval/", content=dataset)
        assert hasattr(response, 'status_code')
        assert response.status_code == 405
        mocked_response.assert_called_once()