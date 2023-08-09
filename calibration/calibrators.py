import pydantic
import pandas 
import typing
from sklearn.linear_model import LogisticRegression
import logging 
import sklearn.exceptions
from sklearn.metrics import roc_auc_score, f1_score

Logger = logging.getLogger("calibration_logger")
file_handler = logging.FileHandler(filename="/logs/calibrators.log")
Logger.addHandler(Logger)

class CalibrationError(Exception):
    """
    Exception, once calibration fails
    """
    def __init__(self, msg=None):
        self.msg = msg
class TrainingCalibrationDataset(pydantic.BaseModel):
    """
    Class reprensents Calibration Dataset for training Platt Scaling 
    algorithm 
    """
    decision_scores: typing.List[float]
    true_classes: typing.List[int]
class PlattScaling(object):
    """
    Platt Scaling Calibration Algorithm Implementation
    """
    def __init__(self):
        self.log_scaler = LogisticRegression()
        self.trained: bool = False
  
    def train(self, 
            train_decision_scores: pandas.Series,
            train_true_classes: pandas.Series, 
            test_decision_scores: pandas.Series,
            test_true_classes: pandas.Series
        ):
        """
        Function trains log scaler for calibrating probabilities
        
        Args:
            train_dataset: pandas.Series - training calibration dataset
            test_dataset: pandas.Series - testing calibration dataset

        NOTE:
            train and test arguments should be from 2 independent
            datasets, otherwise model can end up being overfitted
        
        Returns:
            predicted_values - predicted values from actual given probs
            roc_auc - ROC AUC score estimation of given values 
            f1_score - score estimation of given values
        """
        try:
            train_dataset = TrainingCalibrationDataset(
                decision_scores=train_decision_scores,
                true_classes=train_true_classes
            )

            test_dataset = TrainingCalibrationDataset(
                decision_scores=test_decision_scores,
                true_classes=test_true_classes
            )

            self.log_scaler.fit(
                pandas.Series(train_dataset.decision_scores),
                pandas.Series(train_dataset.true_classes),
            )

            predicted_values = self.log_scaler.predict(
                pandas.Series(test_dataset.decision_scores)
            )

            # Estimaing Performance of the model 
            roc_auc = roc_auc_score(
                test_dataset.true_classes,
                predicted_values
            )
            
            f1_scoring = f1_score(
                test_dataset.true_classes,
                predicted_values
            )
            self.trained = True
            return predicted_values, (roc_auc, f1_scoring)

        except(
            sklearn.exceptions.DataConversionWarning,
            sklearn.exceptions.DataDimensionalityWarning,
        ) as training_err:
            Logger.warn(training_err)

        except(
            sklearn.exceptions.NotFittedError,
        ) as err:
            Logger.error(err)
            raise err
        

    def predict(self, decision_scores: typing.List[float]):
        """
        Function predict calibrated values 
        using trained Logistic Regression Scaler function
        
        Args:
            decision_scores: typing.List[float] - training

        Returns:
            predicted binary classes of the decision scores
        """
        if self.trained == False: 
            raise ValueError('You need to train Platt Scaling before predicting values.')
        predicted_probs = self.log_scaler.predict(decision_scores)
        return predicted_probs
