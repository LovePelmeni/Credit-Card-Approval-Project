import pandas
from ...src.modeling import feature_form, modeling
import numpy, unittest
import pydantic

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



class DatasetValidatorTestCase(unittest.TestCase):

    def test_feature_numeric_encoders(self):

        for record in range(len(dataset)):
            test_dataset = dataset.iloc[record]

            features = feature_form.CardApprovalFeatures(**test_dataset.to_dict())
            encoded_data = features.encoded_data()

            num_columns = encoded_data.select_dtypes(include='number').columns 
            for column in num_columns:
                assert -2 <= encoded_data[column][0] <= 2

    def test_prediction_form_invalidate(self):
        
        for record in range(len(dataset)):
            test_dataset = inv_dataset.iloc[record]
            with self.assertRaises(
                expected_exception=pydantic.ValidationError,
                msg="Form should be invalidated",
            ):
                feature_form.CardApprovalFeatures(**test_dataset.to_dict())

def test_prediction_model():

    model = modeling.prediction_model
    for record in range(len(dataset)):

        test_dataset = dataset.iloc[record]
        features = feature_form.CardApprovalFeatures(**test_dataset.to_dict())
        predicted_status = model.predict_card_approval(features=features)

        assert predicted_status is not None
        assert predicted_status in (0, 1)
