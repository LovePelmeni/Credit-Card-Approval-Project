import logging
import constants
import pickle
import feature_form, numpy

logger = logging.getLogger(__name__)
class CreditCardApprover(object):
    
    """
    Class uses Machine Learning Model for predicting
    credit card approvals
    """
    
    def __init__(self, model, decision_threshold: float = 0.5):
        self.__model = model
        self.__decision_threshold = decision_threshold
    
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
        enc_data = features.encoded_data()
        pos_prob = numpy.array(self.__model.predict_proba(enc_data))[0][1] # predicted prob of positive class
        predicted_status = (pos_prob >= self.__decision_threshold).astype(int)
        return predicted_status

classifier_file = open(constants.MODEL_CLASSIFIER_URL, mode='rb')
classifier = pickle.load(classifier_file)

prediction_model = CreditCardApprover(model=classifier)