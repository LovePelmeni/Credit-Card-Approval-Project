from sklearn.preprocessing import OrdinalEncoder
import pandas
import numpy


def encode_living_place_feature(dataset: pandas.DataFrame):
    """
    Function encodes `living place` dataset using Ordinal Encoding 
    
    Args:
        dataset: pandas.DataFrame object, containing living_place feature
    """
    if not 'living_place' in dataset.columns: return 
    living_categories = [
        'Co-op apartment',
        'Office apartment',
        'Municipal apartment',
        'House / apartment',
        'Rented apartment', 
        'With parents',
    ]
    encoder = OrdinalEncoder(dtype=numpy.int8, categories=[living_categories])
    dataset['living_place'] = encoder.fit_transform(dataset[['living_place']])


def encode_education_category(feature_dataset: pandas.DataFrame):
    """
    Function encodes 'education category' feature using One-Hot Encoding

    Args:
        feature_dataset (pandas.DataFrame) object, containing education category feature 
    """
    if not 'education_category' in feature_dataset: return 
    cats = [
        'Academic degree',
        'Higher education',
        'Incomplete higher',
        'Secondary / secondary special',
        'Lower secondary',
    ]
    encoder = OrdinalEncoder(categories=[cats])
    feature_dataset['education_category'] = encoder.fit_transform(feature_dataset[['education_category']])

def encode_income_category(feature_dataset: pandas.DataFrame):
    """
    Function encodes 'income_category' feature using One-Hot Encoding 

    Args:
        feature_data (pandas.Series) - feature
    
    Returns:
        dataset, containing new encoded feature
    """
    if not 'income_category' in feature_dataset: return 
    cats = [
        "Working",
        "State servant",
        "Pensioner",
        "Commercial associate",
        "Student"
    ]
    encoder = OrdinalEncoder(categories=[cats])
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
