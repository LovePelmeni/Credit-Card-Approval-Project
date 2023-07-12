import pytest
from ...src.modeling import feature_form, exceptions
from ...src import settings

import pytest
from fastapi.testclient import TestClient
import unittest.mock

def load_valid_dataset():
    return feature_form.CardApprovalFeatures(
        annual_income=45665311,
        credit_window=10,
        Male=True,
        total_children=0,
        has_car=True,
        has_realty=True,
        Married=False
    )

@pytest.fixture(scope='module')
def test_client():
    return TestClient(settings.application)

def test_prediction_controller(test_client):
    dataset = load_valid_dataset() 
    response = test_client.post("/predict/card/approval/", content=dataset)
    assert hasattr(response, 'status_code')
    assert response.status_code in (200, 201)
     
@unittest.mock.patch(
    target="...src.modeling.modeling.CreditCardApprover.predict_card_approval",
    side_effect=exceptions.PredictionFailed
)
def test_fail_prediction_controller(test_client):
    dataset = load_valid_dataset()
    response = test_client.post("/predict/card/approval/", content=dataset)
    assert hasattr(response, 'status_code')
    assert response.status_code == 405
