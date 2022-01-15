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