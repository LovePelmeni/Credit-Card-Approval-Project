import typing, logging
from imblearn.over_sampling import RandomOverSampler, SMOTE
import pandas 
import constants 

Logger = logging.getLogger(__name__)

def get_sampling_precision_metric():
    # returns precision metric of the sampling
    pass

def rose_over_sampling(
    X_train: typing.Union[pandas.DataFrame, pandas.Series],
    Y_train: typing.pandas.Series
):
    if not len(X_train) or not len(Y_train): return None, None
    try:
        sampler  = RandomOverSampler(random_state=1, sampling_strategy="")
        X_resampled, Y_resampled = sampler.fit_resample(X=X_train, y=Y_train)
        return X_resampled, Y_resampled 
    except(TypeError, ValueError) as sampling_exception:
        Logger.debug("Failed to perform ROSE Over Sampling Technique, Exception Arised. [%s]"
        % sampling_exception)
        return None, None

def rose_under_sampling():
    pass

def smote_sampling(
    X_train: typing.Union[pandas.DataFrame, pandas.Series], 
    Y_train: typing.Union[pandas.DataFrame, pandas.Series]):

    if not len(X_train) or not len(Y_train): return None, None 
    try:
        smote_tech = SMOTE(random_state=1, k_neighbors=constants.K_SMOTE_NEIGHBORS)
        X_resampled, Y_resampled = smote_tech.fit_resample(X_train, Y_train)
        return X_resampled, Y_resampled
    except(TypeError, ValueError) as train_exception:
        Logger.debug("Failed to balance data using SMOTE Technique, exception raised. [%s]" % train_exception)
        return None, None 

def csl_sampling():
    pass 