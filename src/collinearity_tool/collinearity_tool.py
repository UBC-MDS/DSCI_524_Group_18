def corr_matrix(df):
    """Select all numeric variables and calculate 
    Pearson correlation coefficient pairwise.
    
    Parameters
    ----------
    df : The input data frame.

    Returns
    -------
    pandas.dataframe
        A correlation matrix.
    
    Examples
    --------
    >>> from collinearity_tool.corr_matrix import corr_matrix
    >>> corr_df = corr_matrix(df)
    """