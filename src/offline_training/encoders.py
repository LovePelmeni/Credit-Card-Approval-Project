from sklearn.preprocessing import OrdinalEncoder
import pandas
import numpy
from offline_training import feature_constants

def encode_living_place_feature(feature_dataset: pandas.DataFrame):
    """
    Function encodes `living place` dataset using Ordinal Encoding 
    
    Args:
        dataset: pandas.DataFrame object, containing living_place feature
    """
    if 'living_place' not in feature_dataset.columns: return 
    encoder = OrdinalEncoder(dtype=numpy.int8, categories=[feature_constants.LIVING_PLACES])
    feature_dataset['living_place'] = encoder.fit_transform(feature_dataset[['living_place']])


def encode_education_category(feature_dataset: pandas.DataFrame):
    """
    Function encodes 'education category' feature using One-Hot Encoding

    Args:
        feature_dataset (pandas.DataFrame) object, containing education category feature 
    """
    if 'education_category' not in feature_dataset.columns: return 
    encoder = OrdinalEncoder(categories=[feature_constants.EDUCATION_CATEGORIES])
    feature_dataset['education_category'] = encoder.fit_transform(feature_dataset[['education_category']])

def encode_income_category(feature_dataset: pandas.DataFrame):
    """
    Function encodes 'income_category' feature using One-Hot Encoding 

    Args:
        feature_data (pandas.Series) - feature
    
    Returns:
        dataset, containing new encoded feature
    """
    if 'income_category' not in feature_dataset.columns: return 
    encoder = OrdinalEncoder(categories=[feature_constants.INCOME_CATEGORIES])
    feature_dataset['income_category'] = encoder.fit_transform(feature_dataset[['income_category']])

def encode_dataset(merged_dataset: pandas.DataFrame):
    """
    Encodes all feature dataset using appropriate
    feature encoding techniques 
    """
    encode_living_place_feature(merged_dataset)
    encode_income_category(merged_dataset)
    encode_education_category(merged_dataset)
    return merged_dataset
    