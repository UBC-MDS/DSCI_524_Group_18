import altair as alt
import numpy as np
import pandas as pd

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

    
def corr_heatmap(df, scheme='blueorange'):
    """Plot rectangular data as a color-encoded Pearson correlaiton matrix.

    The rows and the columns contain variable names, while the heatmap tiles 
    contain Pearson correlation coefficient and corresponding colours.
    
    Parameters
    ----------
    df : pandas.DataFrame 
        2D dataset that can be coerced into an ndarray.
    scheme : str
        the diverging vega scheme from https://vega.github.io/vega/docs/schemes/#diverging
        the default is 'blueorange'

    Returns
    -------
    altair.LayerChart
        A aitair chart with text layer
    
    Examples
    --------
    >>> from collinearity_tool.collinearity_tool import corr_heatmap
    >>> corr_heatmap(df)
    """

    corr_matrix_longer, corr_mat = corr_matrix(df)

    heatmap = alt.Chart(corr_matrix_longer).mark_rect().encode(
        x=alt.X('variable1:O', title=''),
        y=alt.Y('variable2:O', title=''),
        color=alt.Color('correlation:Q', scale=alt.Scale(
            scheme='blueorange', domain=[-1, 1]))
    ).properties(
        width=400,
        height=400)

    text = heatmap.mark_text().encode(
        text='rounded_corr',
        color=alt.condition(
            alt.datum.correlation > 0.5,
            alt.value('black'),
            alt.value('white')
        )
    )
    
    return heatmap + text
    
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

    
def col_identify(corr_df, output_viff, corr_limit = 0.8, vif_limit = 4):
    """Multicollinearity identification function highly correlated pairs 
    (Pearson coefficient) with VIF values exceeding the threshold.

    This function takes in correlated pairs from the correlation matrix pairs,
    (for example, using corr_matrix()) function from this package.
    It selects pairs with values exceeding a pre-determined value
    (e.g. Pearson coefficient of 0.8). The user will be able to choose thresholds
    or use the default thresholds.
    It then checks VIF values from the VIF function output and suggests to 
    remove the variable with the highest value from the correlated pair.

    Parameters
    ----------
    corr_df : Pandas DataFrame
        A dataframe containing correlated pairs with variable names
        as column and row names and values as Pearson coefficient.
        This dataframe comes from the matrix correlation function.
    output_viff: Pandas Dataframe
        A dataframe containing variable names and VIF values.
    corr_limit : numeric (float), optional
        A decimal number that serves as a threshold for selecting
        a pair. This is a Pearson coefficient value. Default set at 0.8.
    vif_limit: numeric (float), optional
        A decimal number that serves as a threshold for selecting
        a pair. This is a VIF value. Default set at 4.

    Returns
    -------
    Pandas DataFrame
        A dataframe containing the following columns:
        VIF, Pearson coefficient, Elimination (value showing
        which variable should be eliminated).
        Index as variable pairs (e.g. var1/var2).

    Examples
    --------
    >>> from collinearity_tool.collinearity_tool import co_identify
    >>> col_identify(corr_df, 0.9, 5)
    Index: var1/var2
    VIF var 1: 6.50
    VIF var 2: 5.50
    Pearson coefficient: 0.90
    Elimination: var 1

    """