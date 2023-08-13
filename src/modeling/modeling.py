import logging
from . import constants
from . import feature_form
import numpy
from . import exceptions
import sklearn.exceptions
import xgboost
import os
import pickle
from calibration import calibrators
import typing 

if os.environ.get("TESTING_MODE", 0) == 0:
    Logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(filename="logs/modeling.log")
    Logger.addHandler(file_handler)
else:
    Logger = logging.getLogger(__name__)

class CreditCardApprover(object):

    """
    Class uses Machine Learning Model for predicting
    credit card approvals
    """

    def __init__(self):

        self.__model = xgboost.XGBClassifier()
        self.__calibrator: typing.Union[None, calibrators.PlattScaling] = None

        self.__decision_threshold = constants.DECISION_THRESHOLD
        self.__load_model()
        self.__load_calibrator()

    def __load_model(self):
        """
        Function loads XgBoost Classifier model from the File Path 
        specified at 'constants' module 
        """
        self.__model.load_model(fname=constants.MODEL_CLASSIFIER_URL)

    def __load_calibrator(self):
        """
        Function loads Calibrator Classifier model form File Path 
        specified at 'constants' module
        """
        self.__calibrator = pickle.load(open(constants.CALIBRATOR_CLASSIFIER_URL, mode="rb"))

    def predict_card_approval(self, features: feature_form.CardApprovalFeatures):
        """
        Function, that predicts client's card approval status, based 
        on the credit window they want to apply for, their age and job

        Args:
            features: features used for prediction process

        Returns:
            0 - if the client more likely would be rejected 
            1 - if the client has a high chance of being accepted
        """
        try:
            enc_data = features.get_dataframe()
            pos_prob = numpy.array(self.__model.predict_proba(enc_data))[0, 1]
     
            calibrated_prob = self.__calibrator.get_calibrated_prob(
                decision_scores=[pos_prob]
            )

            predicted_status = (
                calibrated_prob >= self.__decision_threshold
            ).astype(int)
            
            return predicted_status

        except (ValueError, AttributeError,
                TypeError, sklearn.exceptions.NotFittedError) as err:
            Logger.error(err)
            raise exceptions.PredictionFailed(msg=err.args)

prediction_model = CreditCardApprover()