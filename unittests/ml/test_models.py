import pandas
from ...src.modeling import feature_form, modeling
import numpy, pytest

def main_dataset() -> pandas.DataFrame:
    dataset = {
        'credit_window': numpy.random.choice(a=numpy.arange(start=1, stop=1000), size=6),
        'annual_income': numpy.random.choice(a=numpy.arange(40000, 1000000), size=6),
        'Male': numpy.random.choice(a=[True], size=6),
        'Female': numpy.random.choice(a=[False], size=6),
        'has_car': numpy.random.choice(a=[True, False], size=6),
        'has_realty': numpy.random.choice(a=[True, False], size=6),
    }
    return pandas.DataFrame(data=dataset)

def invalid_dataset() -> pandas.DataFrame:
    dataset = {
        'credit_window': numpy.random.choice(a=numpy.arange(start=1, stop=1000), size=6),
        'annual_income': numpy.random.choice(a=numpy.arange(40000, 1000000), size=6),
        'Male': numpy.random.choice(a=[True, False, pandas.NA], size=6),
        'Female': numpy.random.choice(a=[True, False, pandas.NA], size=6),
        'has_car': numpy.random.choice(a=[True, False, pandas.NA], size=6),
        'has_realty': numpy.random.choice(a=[True, False, pandas.NA], size=6),
    }
    return pandas.DataFrame(data=dataset)
    
dataset = main_dataset() 
inv_dataset = invalid_dataset()


@pytest.mark.parametrize(
    "test_dataset,status",
    [ 
        (dataset.iloc[0], True),
        (dataset.iloc[1], True),
        (dataset.iloc[2], True),
        (dataset.iloc[3], True),
        (dataset.iloc[4], True),
        (dataset.iloc[5], True),
    ]
)
def test_feature_numeric_encoders(test_dataset, status):

    allowed_range = numpy.arange(-2, 2).tolist()

    features = feature_form.CardApprovalFeatures(**test_dataset.to_dict())
    encoded_data = features.encoded_data()

    num_columns = encoded_data.select_dtypes(include='number').columns 
    print(num_columns)
    assert all(encoded_data[column][0] in allowed_range for column in num_columns) == status


def test_prediction_model(test_dataset):

    model = modeling.prediction_model
    features = feature_form.CardApprovalFeatures(**test_dataset.to_dict())
    predicted_status = model.predict_card_approval(features=features)
    assert isinstance(predicted_status, int)
    assert predicted_status is not None
    assert predicted_status in (0, 1)
