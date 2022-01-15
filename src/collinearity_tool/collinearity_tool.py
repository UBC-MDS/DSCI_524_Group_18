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