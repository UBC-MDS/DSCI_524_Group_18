from unicodedata import numeric
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

    
def col_identify(corr_output, vif_output, corr_min = -0.8, corr_max = 0.8, vif_limit = 4):
    """Multicollinearity identification function highly correlated pairs 
    (Pearson coefficient) with VIF values exceeding the threshold.

    This function returns a DataFrame containing Pearson's coefficient,
    VIFF, and the suggestion to eliminate or keep a variable based on 
    VIFF and Pearson's coefficient thresholds.

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

    # Test input variables
    assert type(corr_output) == pd.core.frame.DataFrame, "corr_output must be a matrix dataframe"
    assert type(vif_output) == pd.core.frame.DataFrame, "vid_output must be a dataframe"
    assert isinstance(corr_max, (int, float, complex)), "corr_max must be a number"
    assert isinstance(corr_min, (int, float, complex)), "corr_min must be a number"
    assert isinstance(vif_limit, (int, float, complex)), "vif_limit must be a number"
    assert -1 <= corr_max <= 1, "corr_max must be between -1 and 1"
    assert -1 <= corr_min <= 1, "corr_max must be between -1 and 1"
    assert corr_max > corr_min, "corr_max must be larger than corr_min"


    col_names = corr_output.columns.to_list()
    corr_long = corr_output.melt(
        id_vars=['variable'], value_vars=col_names, var_name='variable_2', value_name='pearsons_coeff')
    corr_filtered = pd.DataFrame(
        corr_long[(corr_long.pearsons_coeff <= (corr_min)) | (corr_long.pearsons_coeff >= corr_max) & (corr_long.pearsons_coeff != 1)])

    def pair_maker(x, y):
        pairs = []
        pairs.append(x)
        pairs.append(y)
        sorted_pairs = pairs.sort()
        return pairs

    corr_filtered['pairs'] = corr_filtered.apply(lambda x: pair_maker(x['variable'], x['variable_2']), axis=1)

    results_df = corr_filtered.join(vif_output.set_index('variable'), on='variable', how='left')
    results_df['eliminate'] = results_df['vif'].apply(lambda x: 'No' if x <= vif_limit else 'Yes')
    results_df.drop(columns=['variable_2'])
    
    # Test results dataframe
    assert type(results_df) == pd.core.frame.DataFrame, "results_df must be a dataframe"

    return results_df

# def my_test():
#     """
#     Test with toy_data
#     """
#     # test invalid handle
#     with raises(TypeError) as e:
#         col_identify(...)
#     assert  == 

