import pydantic
import pandas 
from sklearn.preprocessing import StandardScaler
import numpy

FEATURE_ORDER  =  ['Male', 'has_car', 'Married', 'Female', 'has_realty',
       'credit_window', 'annual_income', 'total_children']
class CardApprovalFeatures(pydantic.BaseModel):

    """
    Class Form represents set of features for predicting card approval status

    NOTE:
        does not change the format of the features (uppercase to lowercase and vice-versa)
        example: 
            Male -> male 

        features has their own strict form, which in case 
        of violation, can lead to potential issues at model fitting process
    """

    annual_income: float
    credit_window: int

    Male: bool = False # one of these fields 'Male' or 'Female' should be filled
    Female: bool = False

    total_children: int = 0

    has_realty: bool = False
    has_car: bool = False
    Married: bool = False

    def set_datatypes(self, dataframe: pandas.DataFrame) -> None:
        
        """
        Function sets datatypes for dataset features, according to it's possible range 

        Args:
            dataframe: target pandas.DataFrame object
        """

        dataframe['annual_income'] = dataframe['annual_income'].astype(numpy.float32)
        dataframe['credit_window'] = dataframe['credit_window'].astype(numpy.float64)

        dataframe['Male'] = dataframe['Male'].astype(numpy.bool_)
        dataframe['Female'] = dataframe['Female'].astype(numpy.bool_)

        dataframe["total_children"] = dataframe["total_children"].astype(numpy.int8)

        dataframe["has_realty"] = dataframe["has_realty"].astype(numpy.bool_)
        dataframe["has_car"] = dataframe["has_car"].astype(numpy.bool_)
        dataframe["Married"] = dataframe["Married"].astype(numpy.bool_)
    
    def get_dataframe(self) -> pandas.DataFrame:
        """
        Function converts model to pandas.DataFrame object
        """
        df = pandas.DataFrame() 
        for feature, value in self.__dict__.items():
            df[feature] = [value]

        self.set_datatypes(df)
        return df
    
    def encoded_data(self) -> pandas.DataFrame:
        """
        Function encodes feature data 
        into suitable format for the model 

        For data:
            categorical: applies encodings 
            numeric: applies standardization and normalization
        
        Returns:
            pandas.DataFrame object, containing encoded data
        """
        if all([self.Male, self.Female]): 
            raise ValueError("You need to choose one of the genders, Male or Female")

        if not self.Male and not self.Female:
            raise ValueError("Field Male and Female are required, please, fill one of them")

        df = self.get_dataframe()
        enc_numeric = self.__standardize_numeric_features()
        
        boolean_features = df[df.select_dtypes(include="boolean").columns]
        enc_data = pandas.concat([enc_numeric, boolean_features], axis=1)
        return enc_data[FEATURE_ORDER]
        
    def __standardize_numeric_features(self) -> pandas.DataFrame:
        """
        Function standardize numeric features from the feature dataset 
        Applies `StandardScaler` Class from sklearn library 
        for data standardization

        Returns:
            pandas.DataFrame object, containing standardized data
        """
        df = self.get_dataframe()
        numeric_features = df[df.select_dtypes(include="number").columns]
        
        values = numeric_features.values.reshape(-1, 1)
        scaler = StandardScaler()

        data = scaler.fit_transform(values)
        scaled_data = pandas.DataFrame(data.reshape(1, -1), columns=numeric_features.columns)
        return scaled_data

