from unicodedata import numeric
import pandas as pd
import numpy as np
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor
import altair as alt


def corr_matrix(df):
    """Select all numeric variables and calculate
    Pearson correlation coefficient pairwise. The output
    of this function has all numeric variables as
    columns and rows and correlation coefficient
    as each data point.
    
    Parameters
    ----------
    df : pandas.DataFrame 
        The input data frame.

    Returns
    -------
    pandas.DataFrame
        A correlation matrix.
    
    Examples
    --------
    >>> from collinearity_tool.collinearity_tool import corr_matrix
    >>> corr_df = corr_matrix(df)
    """

    
def corr_heatmap(df):
    """Plot rectangular data as a color-encoded Pearson correlaiton matrix.

    The rows and the columns contain variable names, while the heatmap tiles 
    contain Pearson correlation coefficient and corresponding colours.
    
    Parameters
    ----------
    df : pandas.DataFrame 
        2D dataset that can be coerced into an ndarray. The index/column information 
        will be used to label the columns and rows.

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the heatmap.
    
    Examples
    --------
    >>> from collinearity_tool.collinearity_tool import corr_heatmap
    >>> corr_heatmap(df)
    """
    
def vif_bar_plot(x, y, df, thresh):
    """
    Returns a list containing a dataframe that includes Variance Inflation Factor (VIF) for each explanatory variable and 
    a bar chart for the VIFs alongside the specified threshold in a multiple linear regression model.
   
    Parameters
    ----------
    x : list
        A list of the explanatory variables.
    y : str
        The response variable
    df : pandas.DataFrame
        A dataframe containing the data.
    thresh : int
        An integer specifying the threshold.

    Returns
    -------
    list
        A list containing a dataframe for VIFs and a bar chart of the VIFs for each explanatory variable alongside the threshold.
    
    Examples
    --------
    >>> from collinearity_tool.collinearity_tool vif_bar_plot
    >>> vif_bar_plot("response", ["exp1", "exp2", "exp3"], data, 5)
    """

    
def col_identify(df, X, y, corr_min = -0.8, corr_max = 0.8, vif_limit = 4):
    """Multicollinearity identification function highly correlated pairs 
    (Pearson coefficient) with VIF values exceeding the threshold.

    This function returns a DataFrame containing Pearson's coefficient,
    VIF, and the suggestion to eliminate or keep a variable based on 
    VIF and Pearson's coefficient thresholds.

    Parameters
    ----------
    df : Pandas DataFrame
        Dataframe for analysis
    X : list
        A list of explanatory variables
    y : str
        Response variable name
    corr_max : numeric(float or integer), optional
        A decimal number that serves as a threshold for selecting
        a pair. This is a Pearson coefficient value. Default set at 0.8.
    corr_min : numeric(float or integer), optional
        A decimal number that serves as a threshold for selecting
        a pair. This is a Pearson coefficient value. Default set at -0.8.
    vif_limit: numeric (float or integer), optional
        A decimal number that serves as a threshold for selecting
        a pair. This is a VIF value. Default set at 4.

    Returns
    -------
    Pandas DataFrame
        A dataframe containing the following columns:
        'variable', 'pair', 'correlation', 'rounded_corr',
        'vif_score', 'eliminate'

    Examples
    --------
    >>> from collinearity_tool.collinearity_tool import co_identify
    >>> col_identify(cars, exp_x, resp_y, -0.9, 0.9, 5)

    """

    if type(X) is not list:
        raise ValueError("x must be a list of explanatory variables!")
    if type(y) is not str:
        raise ValueError("y must be a string!")
    if type(df) is not pd.DataFrame:
        raise ValueError("df must be a pandas data frame!")
    if type(corr_max) is not float and type(corr_max) is not int:
        raise TypeError("corr_max must be an integer or a float!")
    if type(corr_min) is not float and type(corr_min) is not int:
        raise TypeError("corr_max must be an integer or a float!")
    if -1 >= corr_max <= 1:
        raise ValueError("corr_max must be between -1 and 1")
    if -1 >= corr_min <= 1:
        raise ValueError("corr_min must be between -1 and 1")
    if corr_max < corr_min:
        raise ValueError("corr_max must be larger than corr_min")

    col_names = X + [y]
    df = df[col_names]

    input_corr = corr_matrix(df)[0]

    corr_filtered = pd.DataFrame(
        input_corr[(
            input_corr.correlation <= (corr_min)) | (
            input_corr.correlation >= corr_max) & (
            input_corr.variable1 != input_corr.variable2)])

    def pair_maker(x, y):
        """
        Allows to create pairs from two columns
        """
        if type(x) is not str:
            x = str(x)
        if type(y) is not str:
            y = str(y)
        pairs = [x, y]
        pairs.sort()
        str_pairs = ' | '.join(pairs)
        return str_pairs

    corr_filtered['pair'] = corr_filtered.apply(
        lambda x: pair_maker(x['variable1'], x['variable2']), axis=1)

    vif_output = vif_bar_plot(X, y, df, 3)[0]
    vif_output = pd.DataFrame(
        vif_output[(vif_output.explanatory_var != 'Intercept')]).rename(
        columns={'explanatory_var': 'variable1'})

    results_df = corr_filtered.join(vif_output.set_index('variable1'), on='variable1', how='inner')
    results_df['eliminate'] = results_df['vif_score'].apply(lambda x: 'No' if x <= vif_limit else 'Yes')
    results_df = results_df.drop(columns=['variable2']).rename(columns={'variable1': 'variable'})
    results_df = results_df[['variable', 'pair', 'correlation', 'rounded_corr',
                             'vif_score', 'eliminate']]
    results_df = results_df.sort_values('pair').reset_index(drop='True')

    return results_df

