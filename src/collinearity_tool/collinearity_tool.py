import pandas as pd

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
    
    if df.select_dtypes(include=numerics).columns.tolist() == []:
        print("The input dataframe should contain at least one numeric variable.")
        return None
    elif isinstance(df, pd.DataFrame) == True:
        corr_matrix = df.corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})
        corr_matrix["rounded_corr"] =  round(corr_matrix['correlation'], decimals)
        return (corr_matrix, df.corr())
    else:
        print("Please check if the input is a pandas dataframe!")
        
    
    

    
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