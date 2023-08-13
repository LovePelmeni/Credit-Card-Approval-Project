import pandas
from ...src.modeling import feature_form, modeling
from ...src.offline_training import feature_constants
import numpy


def main_dataset() -> pandas.DataFrame:
    dataset = {
        'credit_window': numpy.random.choice(a=numpy.arange(start=1, stop=1000), size=6),
        'annual_income': numpy.random.choice(a=numpy.arange(40000, 1000000), size=6),
        'has_car': numpy.random.choice(a=[True, False], size=6),
        'has_realty': numpy.random.choice(a=[True, False], size=6),
        'has_email': numpy.random.choice(a=[True, False], size=6),
        'has_phone_number': numpy.random.choice(a=[True, False], size=6),
        'working_years': numpy.random.choice(a=[True, False], size=6),
        'income_category': numpy.random.choice(a=feature_constants.INCOME_CATEGORIES, size=6),
        'education_category': numpy.random.choice(a=feature_constants.EDUCATION_CATEGORIES, size=6),
        'total_children': numpy.random.choice(a=numpy.arange(start=1, stop=20), size=6),
        'living_place': numpy.random.choice(a=feature_constants.LIVING_PLACES, size=6),
        'family_size': numpy.random.choice(a=list(range(1, 6)), size=6),
        'age': numpy.random.choice(list(range(18, 100)), size=6)
    }

    return pandas.DataFrame(data=dataset)


def invalid_dataset() -> pandas.DataFrame:
    dataset = {
        'credit_window': numpy.random.choice(a=numpy.arange(start=1, stop=1000), size=6),
        'annual_income': numpy.random.choice(a=numpy.arange(40000, 1000000), size=6),
        'has_car': numpy.random.choice(a=[True, False], size=6),
        'has_realty': numpy.random.choice(a=[True, False], size=6),
        'has_email': numpy.random.choice(a=[True, False], size=6),
        'has_phone_number': numpy.random.choice(a=[True, False], size=6),
        'working_years': numpy.random.choice(a=[True, False], size=6),
        'income_category': numpy.random.choice(a=feature_constants.INCOME_CATEGORIES, size=6),
        'education_category': numpy.random.choice(a=feature_constants.EDUCATION_CATEGORIES, size=6),
        'total_children': numpy.random.choice(a=numpy.arange(start=1, stop=20), size=6),
        'living_place': numpy.random.choice(a=feature_constants.LIVING_PLACES, size=6),
        'family_size': numpy.random.choice(a=list(range(1, 6)), size=6),
        'age': numpy.random.choice(list(range(18, 100)), size=6)
    }
    return pandas.DataFrame(data=dataset)


dataset = main_dataset()
inv_dataset = invalid_dataset()


def test_prediction_model():

    model = modeling.prediction_model
    for record in range(len(dataset)):

        test_dataset = dataset.iloc[record]
        features = feature_form.CardApprovalFeatures(**test_dataset.to_dict())
        predicted_status = model.predict_card_approval(features=features)

        assert predicted_status is not None
        assert predicted_status in (0, 1)
