def col_identify(corr_df, output_vif, r_limit = 0.8, vif_limit = 4):
    """Collinearity identification function highly correlated pairs (R^2)
    with VIF values exceeding the threshold.

    This function takes in correlated pairs from the correlation matrix pairs.
    It selects pairs with values exceeding a pre-determined values 
    (e.g. Pearson coefficient of0.9). The user will be able to choose thresholds
    or use the default thresholds.
    It then checks VIF values from the VIF function output and suggests to 
    remove the variable with the highest value from the correlated pair.

    Parameters
    ----------
    corr_df : Pandas dataframe
        A dataframe containing correlated pairs with variable names
        as column and row names and values as Pearson coefficient.
        This dataframe comes from the matrix correlation function.
    output_vif : Pandas dataframe
        Variable names and their corresponding values from the VIF
        function.
    r_limit : numeric
        A decimal number that serves as a threshold for selecting
        a pair. This is a Pearson coefficient value. Default set at 0.8.
    vif_limit: numeric

    Returns
    -------
    Pandas dataframe
        A dataframe containing the following columns:
        VIF, Pearson coefficient, Elimination (value showing
        which variable should be eliminated).
        Index as variable pairs (e.g. var1/var2).

    Examples
    --------
    >>> col_identify(corr_df, output_vif, 0.9, 5)
    Index: var1/var2
    VIF var 1: 6.50
    VIF var 2: 5.50
    Pearson coefficient: 0.90
    Elimination: var 1

    """