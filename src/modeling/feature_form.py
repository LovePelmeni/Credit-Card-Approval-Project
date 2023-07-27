import pydantic
import pandas
import numpy
import pandas.errors 

from src.offline_training import encoders 
from src.offline_training import feature_constants
from src.offline_training import features
import logging 
import os

if os.environ.get("TESTING_MODE", 1) == 0:
    Logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(filename="../../logs/db_settings.log")
    Logger.addHandler(file_handler)
else:
    Logger = logging.getLogger(__name__)

class CardApprovalFeatures(pydantic.BaseModel):

    """
    Class Form represents set of features for predicting card approval status
    """

    # Required Fields

    annual_income: float
    credit_window: int
    family_size: int
    working_years: int
    age: int

    income_category: str
    education_category: str
    living_place: str

    # Optional Fields

    has_car: bool = False
    has_realty: bool = False 
    has_phone_number: bool = False 
    has_email: bool = False
    has_children: bool = False

    # Field Validators

    @pydantic.field_validator("income_category")
    def validate_income_category(cls, income_category):
        if income_category not in feature_constants.INCOME_CATEGORIES:
            raise ValueError("Invalid Income Category")
        return income_category
    
    @pydantic.field_validator("education_category", check_fields=True)
    def validate_education_category(cls, education_category):
        if education_category not in feature_constants.EDUCATION_CATEGORIES:
            raise ValueError("Invalid Education Category")
        return education_category

    @pydantic.field_validator("living_place", check_fields=True)
    def validate_living_place(cls, living_place):
        if living_place not in feature_constants.LIVING_PLACES:
            raise ValueError("Invalid Living Place")
        return living_place

    
    def set_datatypes(self, dataframe: pandas.DataFrame) -> None:
        """
        Function sets datatypes for dataset features, according to it's possible range 

        Args:
            dataframe: target pandas.DataFrame object
        """
        try:
            dataframe['annual_income'] = dataframe['annual_income'].astype(numpy.float32)
            dataframe['credit_window'] = dataframe['credit_window'].astype(numpy.float64)
            dataframe['family_size'] = dataframe['family_size'].astype(numpy.int8)
            dataframe['working_years'] = dataframe['working_years'].astype(numpy.int8)
            dataframe['living_place'] = dataframe['living_place'].astype(numpy.int8)
            dataframe['education_category'] = dataframe['education_category'].astype(numpy.int8)

            dataframe["age"] = dataframe["age"].astype(numpy.int8)

            # boolean fields
            dataframe['has_contact_information'] = dataframe['has_contact_information'].astype(numpy.bool_)
            dataframe['has_children'] = dataframe['has_children'].astype(numpy.bool_)
            dataframe['owns_realty_and_car'] = dataframe['owns_realty_and_car'].astype(numpy.bool_)

        except Exception as err:
            Logger.error(err)

    def get_dataframe(self) -> pandas.DataFrame:
        """
        Function converts model to pandas.DataFrame object
        """
        df = pandas.DataFrame()
        for feature, value in self.__dict__.items():
            df[feature] = [value]

        self.__create_features(df) 
        df = self.encoded_data(df)
        self.set_datatypes(df)
        
        # sorting dataset to the original orderdsf
        df = df[list(feature_constants.FEATURE_ORDER)]
        return df

    @staticmethod
    def __create_features(dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Function creates additional features, based on the provided dataset
        """
        try:
            dataset['emp_stability'] = [features.create_emp_stability(
                number_of_years=dataset['working_years'].iloc[0]
            )]

            dataset['owns_realty_and_car'] = [features.create_owns_realty_and_car(
                has_car=dataset['has_car'].iloc[0],
                has_realty=dataset['has_realty'].iloc[0]
            )]
    
            dataset['has_contact_information'] = [features.create_contact_information(
                has_phone_number=dataset["has_phone_number"].iloc[0],
                has_email=dataset['has_email'].iloc[0]
            )]
            
        except Exception as err:
            Logger.error(err)

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
        try:
            enc_data = encoders.encode_dataset(dataset)
            return enc_data
        except Exception as err:
            Logger.error(err)
            raise ValueError("Failed to encode dataset")
    

