import pandas as pd
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt

def vif_bar_plot(x, y, df):
    """
    Plots the Variance Inflation Factor (VIF) for each explanatory variable 
    in a multiple linear regression model.
    
    Parameters
    ----------
    x : list
        A list of the exploratory variables.
    y : str
        The response variable
    df : pandas.DataFrame
        A dataframe containing the data
    
    Returns
    -------
    matplotlib.container.BarContainer
        Bar chart of the VIFs for each explanatory variable.
    
    Examples
    --------
    >>> from collinearity_tool.vif_bar_plot import vif_bar_plot
    >>> vif_bar_plot("response", ["exp1", "exp2", "exp3"], data)
    """
    
    