import numpy 
import pandas
import matplotlib.pyplot as plt 
from calibration import calibrators


def calibration_plot(
    y_true: pandas.Series,
    y_pred: pandas.Series,
    bins=5,
):
    """
    Function plot Reliability Curve using matplotlib module 

    Args:
        y_true - true classes (observations from the dataset)
        y_pred - predicted probabilities
    """
    ideal_curve = numpy.linspace(0, 1, 10)
    plt.plot(ideal_curve, linestyle='--', color="gray")

    pred_probs, actual_probs, ece = calibrators.get_calibration_error(
        y_true=y_true,
        y_pred=y_pred,
        num_bins=bins
    )

    # building scatter dependency plot
    plt.scatter(
        x=pred_probs,
        y=actual_probs,
        color="blue",
    )

    # setting ticks for the plot
    plt.xticks(numpy.linspace(0, 1, 10))
    plt.yticks(numpy.linspace(0, 1, 10))

    plt.title("Expected Calibration Error (ECE) - %s" % str(ece))
    plt.xlabel("Probability Score of the Model")
    plt.ylabel("Actual Probability")
    plt.show()
