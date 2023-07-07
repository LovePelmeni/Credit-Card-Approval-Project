import pydantic
import pandas 
from sklearn.preprocessing import StandardScaler 

class CardApprovalFeatures(pydantic.BaseModel):

    """
    Class Form represents set of features for predicting card approval status
    """
    
    def get_dataframe(self) -> pandas.DataFrame:
        """
        Function converts model to pandas.DataFrame object
        """
        return pandas.DataFrame(
            {
                feature: [value] for feature, value in self.__dict__().items()
            }
        )
    
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
        enc_numeric = self.__standardize_numeric_features()
        enc_categories = self.__encode_categorical_features()

        enc_data = pandas.concat([enc_categories, enc_numeric], axis=1)
        return enc_data
        
    def __standardize_numeric_features(self) -> pandas.DataFrame:
        """
        Function standardize numeric features from the feature dataset 
        Applies `StandardScaler` Class from sklearn library 
        for data standardization

        Returns:
            pandas.DataFrame object, containing standardized data
        """
        df = self.get_dataframe()
        numeric_features = df[df.select_dtypes(include="numeric").columns]
        scaler = StandardScaler() 

        scaled_data = pandas.DataFrame(
            scaler.fit_transform(numeric_features), 
            columns=numeric_features.columns
        )
        return scaled_data 

    def __encode_categorical_features(self) -> pandas.DataFrame:
        """
        """
