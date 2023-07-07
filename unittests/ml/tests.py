import pytest
import pandas
from ...src.modeling import modeling
import numpy

def main_dataset() -> pandas.DataFrame:
    dataset = {
        'age': [23, 45, 23, 21, 56, 64],
        'job': ["Staff Engineer", "Senior Engineer", "Chief Executive", "Product Manager", "ML Engineer"],
        'credit_window': [14, 32, 12, 18, 75, 56]
    }

    return pandas.DataFrame(dataset, columns=dataset.keys())

dataset = main_dataset() 

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
def test_feature_encoders(test_dataset):

    allowed_range = numpy.arange(-1, 1)

    features = modeling.CardApprovalFeatures(
        age=test_dataset['age'],
        job=test_dataset['job'],
        credit_window=test_dataset['credit_window']
    )
    enc_data = features.encoded_data()
    assert isinstance(enc_data['job'], numpy.int_)
    assert isinstance(enc_data['age'][0], numpy.int_) and (enc_data['credit_window'][0], numpy.int_)
    assert numpy.isin(enc_data['age'][0], allowed_range)
    assert numpy.isin(enc_data['credit_window'][0], allowed_range)


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
    features = modeling.CardApprovalFeatures(
        age=test_dataset['age'],
        job=test_dataset['job'],
        credit_window=test_dataset['credit_window']
    )
    enc_data = features.encoded_data()
    predicted_status = model.predict_card_approval(features=enc_data)
    assert isinstance(predicted_status)
    assert predicted_status is not None 