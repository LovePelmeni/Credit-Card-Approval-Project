import typing, numpy
from sklearn.model_selection import cross_validate, StratifiedKFold

def cross_validate_new_model(

    model, 
    metrics: typing.List[typing.Callable], 
    error_scorer: typing.Callable

    ) -> typing.Dict[str, float]:

    """
    """

    cv = StratifiedKFold(n_splits=5) 
    cv_scores = cross_validate(
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