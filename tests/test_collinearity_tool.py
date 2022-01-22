from collinearity_tool.collinearity_tool col_identify

import pandas as pd
import numpy as np
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor
import altair as alt

def test_col_identify():
    """
    Tests outputs and other parameters of the col_identify()
    function.
    
    Examples
    --------
    >>> test_col_identify()
    """
    
    cars = pd.read_csv("https://raw.githubusercontent.com/tidyverse/ggplot2/main/data-raw/mpg.csv")
    exp_list = ["displ", "year", "cyl", "cty"]
    resp_y = "hwy"

    col_df = col_identify(cars, exp_list, resp_y)

    # output and its properties
    assert type(col_df) == pd.DataFrame, "The output should be a Pandas DataFrame"
    assert col_df.shape[1] == 6, "The output should contain 6 columns"
    assert col_df.columns.to_list() == ["variable", "pair", "correlation", "rounded_corr",
                             "vif_score", "eliminate"], "The following columns should be produced: variable, pair, correlation, rounded_corr, vif_score, eliminate"

    col_df = round(col_df, 5)

    data = {"variable": ["cyl", "cty", "cty", "displ", "cyl"],
        "pair": ["cty | cyl", "cty | cyl", "cty | hwy", "cyl | displ", "cyl | displ"],
        "correlation": [-0.8058, -0.8058, 0.9559, 0.9302, 0.9302],
        "rounded_corr": [-0.81, -0.81, 0.96, 0.93, 0.93],
        "vif_score": [8.0817, 3.0547, 3.0547, 7.9384, 8.0817],
        "eliminate": ["Yes", "No", "No", "Yes", "Yes"]}

    test_df = round(pd.DataFrame(data), 5)

    assert col_df.equals(test_df), "The test and real dataframes should be the same"
