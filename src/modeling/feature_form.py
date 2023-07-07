import pydantic
import pandas 
from sklearn.preprocessing import StandardScaler, LabelEncoder 

class CardApprovalFeatures(pydantic.BaseModel):
    """
    Class Form represents set of features for predicting card approval status
    Args:
        age: feature, representing age of the client 
        job: feature, represening current job of the client 
        credit_window: feature, representing credit window of the client
    """
    age: float
    job: str
    credit_window: float
        
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
        enc_job = self.__encode_job()
        st_data = self.__standardize_numeric_features()
        enc_data = pandas.concat([enc_job, st_data], axis=1)
        return enc_data
        
    def __standardize_numeric_features(self) -> pandas.DataFrame:
        """
        Function standardize numeric features from the feature dataset 
        Applies `StandardScaler` Class from sklearn library 
        for data standardization

        Returns:
            pandas.DataFrame object, containing standardized data
        """
        df = pandas.DataFrame({'credit_window': [self.credit_window], 'age': [self.age]})
        scaler = StandardScaler() 

        scaled_data = pandas.DataFrame(scaler.fit_transform(df), columns=['credit_window', 'age'])
        return scaled_data 

    
    def __encode_job(self) -> pandas.DataFrame:
        """
        Functions implements K-Fold Target Encoding for Feature called 'Job'
        Returns:    
            pandas.DataFrame object, containing encoded job value
        """
        encoder = LabelEncoder()
        enc_data = pandas.DataFrame(encoder.fit_transform([self.job]), columns=['job'])
        return enc_data
