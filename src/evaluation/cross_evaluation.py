from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import make_scorer, precision_score
import typing, logging, pandas
import dataclasses
from sklearn.ensemble import RandomForestClassifier
from ..cleansing import constants
import sklearn.exceptions

from sklearn.model_selection import cross_val_score
from sklearn.base import BaseEstimator

BASE_SCORING = make_scorer(precision_score)

Logger = logging.getLogger(__name__)

@dataclasses.dataclass
class BestCrossValidatedModel(object):
    """
    Class represents output model of 'precision_cross_validate_models' function

    Attributes:
        1. model: Machine Learning Model (Algorithm), which is the most suitable for the dataset
        (has the highest precision score across all other options)
    """
    model: BaseEstimator 
    precision_score: float

def precision_cross_validate_models(
    
    x_train_dataset: pandas.DataFrame,
    y_train_dataset: pandas.DataFrame,
    selected_models: typing.List[BaseEstimator]

) -> typing.Union[BestCrossValidatedModel, None]:
    """
    Applies cross validation to each model from set: "K-Neighbors, Logistic Regressor, Decision Tree, Random Forest" 
    and picks up the best one, which has the highest precision metric score
    In case of this project, False Positives are costly and we'd like to avoid them as much as possible 

    Args:
        1. train_dataset: training dataset for cross-validating models
        2. test_dataset: test dataset for cross-validating models
    
    Returns: 
        blob of hashmap with following params
    """
    try:
        model_scores = sorted([
            (
                model, 
                cross_val_score(model, 
                X=x_train_dataset,
                y=y_train_dataset,
                cv=constants.NUMBER_OF_EXPS, scoring="precision").mean()
            )
            for model in selected_models
        ], key=lambda modelObj: modelObj[1], reverse=False)
        
        bestModel = BestCrossValidatedModel(
            model=model_scores[0][0],
            precision_score=model_scores[0][1],
        )
        return bestModel
    except(
        sklearn.exceptions.FitFailedWarning, 
        sklearn.exceptions.NotFittedError
    ): 
        Logger.debug("Invalid data has been passed to classifier")
        return None