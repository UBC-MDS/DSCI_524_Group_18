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
    results_df = results_df.sort_values('vif_score', ascending=False).drop_duplicates(['pair'])


    return results_df
