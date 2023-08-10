import pydantic
import pandas 
import typing
from sklearn.linear_model import LogisticRegression
import logging 
import sklearn.exceptions
import numpy 

Logger = logging.getLogger("calibration_logger")
file_handler = logging.FileHandler(filename="/logs/calibrators.log")
Logger.addHandler(Logger)

class CalibrationError(Exception):
    """
    Exception, once calibration process fails
    """
    def __init__(self, msg=None):
        self.msg = msg
class CalibrationDataset(pydantic.BaseModel):
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
            train_dataset: CalibrationDataset,
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
            self.log_scaler.fit(
                pandas.Series(train_dataset.decision_scores),
                pandas.Series(train_dataset.true_classes),
            )
            self.trained = True

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
        

    def get_calibrated_prob(self, decision_scores: typing.List[float]):
        """
        Function predict calibrated values 
        using trained Logistic Regression Scaler function
        
        Args:
            decision_scores: typing.List[float] - training

        Returns:
            predicted probability of the calibrated function
        """
        if self.trained == False: 
            raise ValueError('You need to train Platt Scaling before predicting values.')
        predicted_probs = self.log_scaler.predict_proba(decision_scores)[:, 1].tolist()
        return predicted_probs


def get_calibration_error(
    true_classes: numpy.ndarray,
    preds: numpy.ndarray[numpy.ndarray[float]],
    bins: int = 1000):
    """
    Function calculates Expected Calibraiton Error (ECE) 
    for a given set of probabilities and true classes

    Args:
        true_classes: numpy.ndarray - true binary classes 
        preds: numpy.ndarray - predicted binary classes
        bins: int - number of bins to split the data

    Returns:
        - predicted_bins - (bins with their predicted values)
        - actual_bins - (bins with their actual values)
        - sample_counts - (number of samples in each bin)
    """
    if true_classes.shape[0] != preds.shape[0]:
        raise ValueError("Args does not have equal lengths")

    if true_classes.shape[0] == 0: 
        raise ValueError("Passed empty dataset")

    sorted_preds = numpy.argsort(preds)
    predicted_bins = [[] for _ in range(bins)]
    actual_bins = [[] for _ in range(bins)]
    bin_sample_counts = [[] for _ in range(bins)]
    step = 1.*true_classes.shape[0]/bins

    for index in range(bins):
        current = int(step*index)
        next_ = int(step*(index+1))
        predicted_bins[index] = numpy.mean(predicted_bins[sorted_preds[current:next_]])
        actual_bins[index] = numpy.mean(true_classes[sorted_preds[current:next_]])
        bin_sample_counts[index] = true_classes[sorted_preds[current:next_]].shape[0]
    return predicted_bins,actual_bins,bin_sample_counts

