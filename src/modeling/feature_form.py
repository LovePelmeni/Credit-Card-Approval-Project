import pydantic
import pandas
import numpy

from offline_training import encoders 
from offline_training import feature_constants
from offline_training import features

class CardApprovalFeatures(pydantic.BaseModel):

    """
    Class Form represents set of features for predicting card approval status
    """

    # Required Fields

    annual_income: float
    credit_window: int
    family_size: int
    working_years: int
    total_children: int

    income_category: feature_constants.INCOME_CATEGORIES
    education_category: feature_constants.EDUCATION_CATEGORIES
    living_place: feature_constants.LIVING_PLACES
    
    # Optional Fields

    has_car: bool = False
    has_realty: bool = False 
    has_phone_number: bool = False 
    has_email: bool = False



    def set_datatypes(self, dataframe: pandas.DataFrame) -> None:
        """
        Function sets datatypes for dataset features, according to it's possible range 

        Args:
            dataframe: target pandas.DataFrame object
        """

        dataframe['annual_income'] = dataframe['annual_income'].astype(numpy.float32)
        dataframe['credit_window'] = dataframe['credit_window'].astype(numpy.float64)
        dataframe['family_size'] = dataframe['family_size'].astype(numpy.int8)
        dataframe['working_years'] = dataframe['working_years'].astype(numpy.int8)
        dataframe['living_place'] = dataframe['living_place'].astype(numpy.int8)
        dataframe['education_category'] = dataframe['education_category'].astype(numpy.int8)

        dataframe["age"] = dataframe["age"].astype(numpy.int8)

        # boolean fields
        dataframe["has_realty_and_car"] = dataframe["has_realty_and_car"].astype(numpy.bool_)
        dataframe['has_contact_information'] = dataframe['has_contact_information'].astype(numpy.bool_)
        dataframe['has_children'] = dataframe['has_children'].astype(numpy.bool_)
        dataframe['owns_realty_and_car'] = dataframe['owns_realty_and_car'].astype(numpy.bool_)
 

    def get_dataframe(self) -> pandas.DataFrame:
        """
        Function converts model to pandas.DataFrame object
        """
        df = pandas.DataFrame()
        for feature, value in self.__dict__.items():
            df[feature] = [value]

        self.set_datatypes(df)

        df = self.__create_features(df) 
        df = self.encoded_data(df)
        df = df[feature_constants.FEATURE_ORDER]
        return df

    @staticmethod
    def __create_features(dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Function creates additional features, based on the provided dataset
        """

        dataset['emp_stability'] = features.create_emp_stability(
            number_of_years=dataset['working_years']
        )

        dataset['owns_realty_and_car'] = features.create_owns_realty_and_car(
            has_car=dataset['has_car'],
            has_realty=dataset['has_realty']
        )
 
        dataset['has_contact_information'] = features.create_contact_information(
            has_phone_number=dataset['has_phone_number'],
            has_email=dataset['has_email']
        )

    @staticmethod
    def encoded_data(dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Function encodes feature data 
        into suitable format for the model 

        For data:
            categorical: applies encodings 
            numeric: applies standardization and normalization

        Returns:
            pandas.DataFrame object, containing encoded data
        """
        enc_data = encoders.encode_dataset(dataset)
        return enc_data
    