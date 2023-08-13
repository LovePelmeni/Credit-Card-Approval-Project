from ...src.modeling import feature_form, exceptions
from ...settings import application

import pytest
from fastapi.testclient import TestClient
import unittest.mock


def load_valid_dataset() -> feature_form.CardApprovalFeatures:
    """
    Function returns example of mocked feature form 
    for testing ML Algorithm
    """
    return feature_form.CardApprovalFeatures(
        annual_income=1000000,
        credit_window=10,
        family_size=3,
        income_category="Working",
        has_car=True,
        has_realty=True,
        has_children=False,
        has_email=True,
        education_category="Higher education",
        age=25,
        working_years=6,
        living_place="Office apartment",
    )


@pytest.fixture(scope='module')
def test_client():
    return TestClient(application)


def test_prediction_controller(test_client):
    dataset = load_valid_dataset()
    response = test_client.post("/predict/card/approval/", json=dataset.model_dump())
    assert hasattr(response, 'status_code')
    assert response.status_code in (200, 201)


def test_fail_prediction_controller(test_client):
    with unittest.mock.patch(
        target="src.modeling.modeling.CreditCardApprover.predict_card_approval",
        side_effect=exceptions.PredictionFailed,
    ):
        dataset = load_valid_dataset()
        response = test_client.post("/predict/card/approval/", content=dataset)
        assert hasattr(response, 'status_code')
        assert response.status_code == 400
