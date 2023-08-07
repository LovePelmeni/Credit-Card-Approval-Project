import pandas

def calibrate_using_isotonic_regression(probs: pandas.Series):
    """
    Function calibrates probabilities of the model output 
    using Isotonic Regression
    Args:
        probs: pandas.Series - given model probabilities
    """
    if probs.shape[0] == 0: return probs

def calibrate_using_platt_scaling(probs: pandas.Series):
    """
    Function calibrates given probabilities of the model output 
    using platt_scaling algorithm
    """ 
    if probs.shape[0] == 0: return probs

def calibrate_using_prob_cat(probs: pandas.Series):
    """
    Function calibrates given probabilities of the model output 
    using Probability Calibration Tree (Prob CAT)
    """
    if probs.shape[0] == 0: return probs
    