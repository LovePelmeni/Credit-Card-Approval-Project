import numpy 
import pandas
import matplotlib.pyplot as plt 
import calibrators

def calibration_plot(
    y_true: pandas.Series,
    y_pred: pandas.Series,
):
    """
    Function plot Reliability Curve using matplotlib module 
    
    Args:
        y_true - true classes (observations from the dataset)
        y_pred - predicted classes
    """
    ideal_curve = numpy.linspace(0, y_true.shape[0], y_true.shape[0])
    plt.plot(ideal_curve, marker='o')

    predicted_probs, actual_probs, sample_counts = calibrators.get_calibration_error(
        true_classes=y_true,
        preds=y_pred
    )
    ece = 0
    # calculating predicted probs 
    for idx in range(len(predicted_probs)):
        ece += sample_counts[idx] * numpy.abs(predicted_probs[idx] - actual_probs[idx])

    plt.scatter(
        x=predicted_probs,
        y=actual_probs,
        marker='--'
    )
    plt.title("Expected Calibration Error (ECE) - %s" % ece)
    plt.show()