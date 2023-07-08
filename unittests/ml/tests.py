import pytest
import pandas
from ...src.modeling import feature_form, modeling
import numpy
from ...src.modeling import exceptions

def main_dataset() -> pandas.DataFrame:
    dataset = {
        'credit_window': numpy.random.choice(a=numpy.arange(start=1, stop=1000)),
        'annual_income': numpy.random.choice(a=numpy.arange(40000, 1000000)),
        'Male': numpy.random.choice(a=[True, False]),
        'Female': numpy.random.choice(a=[True, False]),
        'has_car': numpy.random.choice(a=[True, False]),
        'has_realty': numpy.random.choice(a=[True, False]),
    }

    return pandas.DataFrame(dataset, columns=dataset.keys())

def invalid_dataset() -> pandas.DataFrame:
    dataset = {
        'credit_window': numpy.random.choice(a=numpy.arange(start=1, stop=1000)),
        'annual_income': numpy.random.choice(a=numpy.arange(40000, 1000000)),
        'Male': numpy.random.choice(a=[True, False, pandas.NA]),
        'Female': numpy.random.choice(a=[True, False, pandas.NA]),
        'has_car': numpy.random.choice(a=[True, False, pandas.NA]),
        'has_realty': numpy.random.choice(a=[True, False, pandas.NA]),
    }
    return pandas.DataFrame(dataset, columns=dataset.keys())

dataset = main_dataset() 
inv_dataset = invalid_dataset()

@pytest.mark.parametrize(
    [ 
        dataset.iloc[:, 1],
        dataset.iloc[:, 2],
        dataset.iloc[:, 3],
        dataset.iloc[:, 4],
        dataset.iloc[:, 5],
        dataset.iloc[:, 6],
    ]
)
def test_feature_numeric_encoders(test_dataset):

    allowed_range = numpy.arange(-1, 1)

    features = modeling.CardApprovalFeatures(**test_dataset.to_dict())
    encoded_data = features.encoded_data()
    num_columns = encoded_data.select_dtypes(include='number').columns 
    for column in num_columns:
        assert encoded_data[column][0] in allowed_range 


@pytest.mark.parametrize(
    [ 
        dataset.iloc[:, 1],
        dataset.iloc[:, 2],
        dataset.iloc[:, 3],
        dataset.iloc[:, 4],
        dataset.iloc[:, 5],
        dataset.iloc[:, 6],
    ]
)
def test_prediction_model(test_dataset):

    model = modeling.prediction_model
    features = modeling.CardApprovalFeatures(**test_dataset.to_dict())
    predicted_status = model.predict_card_approval(features=features)
    assert isinstance(predicted_status, int)
    assert predicted_status is not None
    assert predicted_status in (0, 1)

@pytest.mark.parametrize([
    inv_dataset.iloc[:, 1],
    inv_dataset.iloc[:, 2],
    inv_dataset.iloc[:, 3],
    inv_dataset.iloc[:, 4],
    inv_dataset.iloc[:, 5],
    inv_dataset.iloc[:, 6]
])
def test_fail_prediction_model(invalid_dataset):
    with pytest.raises(expected_exception=exceptions.PredictionFailed):
        feature_form = feature_form.CardApprovalFeatures(**invalid_dataset.to_dict())
