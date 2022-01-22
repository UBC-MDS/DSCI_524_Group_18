import pandas as pd
import numpy as np
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor
import altair as alt

def corr_matrix(df, decimals = 2):
    """Select all numeric variables and calculate
    Pearson correlation coefficient pairwise. User can
    choose the generic matrix as output or the longer
    form one.
    
    Parameters
    ----------
    df : pandas.DataFrame 
        The input data frame.
    decimals: int
        The number of decimals in the output dataframe.

    Returns
    -------
    tuple
        The first element in the tuple is the longer form
        of the correlation matrix and the second one is a 
        generic correlation matrix.
    
    Examples
    --------
    >>> from collinearity_tool.collinearity_tool import corr_matrix
    >>> corr_longer = corr_matrix(df, decimals = 3)[0]
    >>> corr_matrix = corr_matrix(df, decimals = 3)[1]
    """
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    if type(df) is not pd.DataFrame:
        raise ValueError("Please check if the input is a pandas dataframe!")
    if df.select_dtypes(include=numerics).columns.tolist() == []:
        raise ValueError("The input dataframe should contain at least one numeric variable.")
    if type(decimals) is not int or decimals < 0:
        raise ValueError("The number of decimals should be a positive integer.")
    if df.shape[0] <= 1:
        raise ValueError("The input dataframe should contain at least two observations.")
        
    corr_matrix_longer = df.corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})
    corr_matrix_longer["rounded_corr"] =  round(corr_matrix_longer['correlation'], decimals)
    return (corr_matrix_longer, df.corr())
    

    
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
        x=alt.X('variable1', type='nominal', title=''),
        y=alt.Y('variable2', type='nominal', title=''),
        color=alt.Color('correlation', type='quantitative', scale=alt.Scale(
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
    Returns a list containing a dataframe that includes Variance Inflation Factor (VIF) score and 
    a bar chart for the VIF scores alongside the specified threshold for each explanatory variable
    in a linear regression model.
   
    Parameters
    ----------
    x : list
        A list of the names of the explanatory variables.
    y : str
        The response variable.
    df : pandas.DataFrame
        A dataframe containing the data.
    thresh : int, float
        An integer specifying the threshold.

    Returns
    -------
    list
        A list containing a dataframe for VIFs and a bar chart of the VIFs for each explanatory variable alongside the threshold.
    
    Examples
    --------
    >>> from collinearity_tool.collinearity_tool vif_bar_plot
    >>> vif_bar_plot(["exp1", "exp2", "exp3"], "response", data, 5)
    """
    if type(x) is not list:
        raise ValueError("x must be a list of explanatory variables!")
    if type(y) is not str:
        raise ValueError("y must be a string!")
    if type(df) is not pd.DataFrame:
        raise ValueError("df must be a pandas data frame!")
    if type(thresh) is not int and type(thresh) is not float:
        raise ValueError("thresh must be an integer or a float!")
    
    # Data frame containing VIF scores
    explanatory_var = "+".join(set(x))
    
    y, X = dmatrices(y + " ~" + explanatory_var, df, return_type = "dataframe")
    
    vif_list = []
    for i in range(X.shape[1]):
        vif_list.append(variance_inflation_factor(X.values, i))
        
    vif_df = pd.DataFrame(vif_list, 
                          columns = ["vif_score"])
    vif_df["explanatory_var"] = X.columns
    
    
    # Plotting the VIF scores
    hbar_plot = alt.Chart(vif_df).mark_bar(
        ).encode(
            x = alt.X("vif_score", 
              title = "VIF Score"),
            y = alt.Y("explanatory_var",
              title = "Explanatory Variable")
    ).properties(
        width = 400,
        height = 300,
        title = "VIF Scores for Each Explanatory Variable in Linear Regression"
    )
    thresh_plot = alt.Chart(pd.DataFrame({"x": [thresh]})).mark_rule(
        color = "red"
    ).encode(
        x = "x")
    vif_plot = hbar_plot + thresh_plot
    
    return [vif_df, vif_plot]

    
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
