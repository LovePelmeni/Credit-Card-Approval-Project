import pydantic
import pandas 
import typing
from sklearn.linear_model import LogisticRegression
import logging 
import sklearn.exceptions
import numpy 

Logger = logging.getLogger("calibration_logger")

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

    def get_dataframe(self) -> pandas.DataFrame:
        return pandas.DataFrame({
            "decision_scores": self.decision_scores,
            "true_classes": self.true_classes
        })

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
            df = train_dataset.get_dataframe()
            indep = df.drop(columns=['true_classes'])
            dep = df['true_classes']
            self.log_scaler.fit(
                indep,
                dep,
            )
            self.trained = True

        except (
            sklearn.exceptions.DataConversionWarning,
            sklearn.exceptions.DataDimensionalityWarning,
        ) as training_err:
            Logger.warn(training_err)

        except (
            sklearn.exceptions.NotFittedError,
        ) as err:
            Logger.error(err)
            raise err

    def get_calibrated_prob(self, decision_scores: typing.List[float]) -> numpy.ndarray:
        """
        Function predict calibrated values 
        using trained Logistic Regression Scaler function

        Args:
            decision_scores: typing.List[float] - training

        Returns:
            predicted probability of the calibrated function
        """
        try:
            if self.trained == False: 
                raise ValueError('You need to train Platt Scaling before predicting values.')
            df = pandas.DataFrame({'decision_scores': decision_scores})
            predicted_probs = self.log_scaler.predict_proba(df)[:, 1]
            return predicted_probs
        except Exception as pred_err:
            Logger.error(pred_err)
            raise CalibrationError(msg=pred_err)

def get_calibration_error(
        y_true: pandas.Series,
        y_pred: pandas.Series,
        num_bins: int = 1000):
    """
    Function calculates Expected Calibraiton Error (ECE) 
    for a given set of probabilities and true classes
    using Multiclass Classification Approach

    Args:
        true_classes: numpy.ndarray - true binary classes 
        preds: numpy.ndarray - predicted binary classes
        bins: int - number of bins to split the data

    Returns:
        - predicted_bins - (bins with their predicted values)
        - actual_bins - (bins with their actual values)
        - sample_counts - (number of samples in each bin)
    """
    if y_true.shape[0] != y_pred.shape[0]:
        raise ValueError("Args does not have equal lengths")

    if y_true.shape[0] == 0: 
        raise ValueError("Passed empty dataset")

    ece = 0.0

    pred_probs = []
    actual_probs = [] 
    samples = [] 

    sorted_preds = numpy.argsort(y_pred)
    bin_indices = numpy.array_split(sorted_preds, num_bins)
    total_samples = y_true.shape[0]

    pred_classes = (y_pred >= 0.5).astype(int).to_numpy()
    predictions = y_pred.to_numpy()
    accuracies = (y_true == pred_classes).astype(int).to_numpy()

    for indices in bin_indices:

        pred_bins = sorted_preds[indices]
        pred_probs.append(numpy.mean(predictions[pred_bins]))
        actual_probs.append(numpy.mean(accuracies[pred_bins]))
        samples.append(indices.shape[0])

        ece += (
            (samples[-1] / total_samples) * numpy.abs(pred_probs[-1] - actual_probs[-1])
        )

    return pred_probs, actual_probs, ece