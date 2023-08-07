import numpy 
import seaborn as sns 
import pandas
import matplotlib.pyplot as plt 

def calibration_plot(
    y_true: pandas.Series,
    y_pred: pandas.Series,
):
    """
    Function plot Reliability Curve using matplotlib module 
    
    Args:
        y_true - true probabilities
        y_pred - predicted probabilities
    """
    ideal_curve = numpy.linspace(0, y_true.shape[0], y_true.shape[0])
    plt.plot(ideal_curve, marker='o')
    sns.scatterplot(x=y_pred, y=y_true, marker='-o')
    plt.show()