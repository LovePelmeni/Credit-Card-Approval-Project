import typing
import numpy
from sklearn.model_selection import cross_validate, StratifiedKFold
import pandas


def cross_validate_new_model(

    model,
    metrics: typing.List[typing.Callable],
    error_scorer: typing.Callable,
    X_data: pandas.DataFrame,
    Y_data: typing.Union[pandas.DataFrame, pandas.Series]

) -> typing.Dict[str, float]:
    """
    Functions, used for Cross-Validating new model with updated 
    hyperparameters to ensure it's prediction accuracy

    Args:
        model - Machine Learning Classifier with new hyperparameters 
        metrics: list of scorers (aka. metrics - precision, recall or custom metric) 
        for evaluating model's performance 

        error_scorer: loss function for classifier
        X_data: pandas.DataFrame object, containing Training Set for the model 
        Y_data: pandas.Series object, containing target feature for training the model

    Returns:
        hashmap, containing metric scores, specified at `metrics` argument 
        example:
            from sklearn.model_selection import make_scorer
            result_metrics = cross_validate_new_model(.......)
            print(result_metrics)

            Output: 
                {
                    "precision_score": 0.84245156003113,
                    "recall_score": 0.56789256841845329
                }
    """

    cv = StratifiedKFold(n_splits=5)
    cv_scores = cross_validate(
        X=X_data,
        y=Y_data,
        cv=cv,
        estimator=model,
        scoring=metrics,
        error_score=error_scorer,
        n_jobs=-1
    )

    metric_hashmap = {}

    for metric in metrics:
        if "train_%s" % metric in cv_scores:
            metric_hashmap[metric] = numpy.mean(cv_scores["train_%s" % metric])
    return metric_hashmap
