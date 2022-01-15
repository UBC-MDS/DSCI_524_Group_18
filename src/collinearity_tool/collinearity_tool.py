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