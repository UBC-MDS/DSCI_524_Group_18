from collinearity_tool.collinearity_tool vif_bar_plot

import altair as alt
import numpy as np
import pandas as pd

def test_vif_bar_plot():
    """
    Tests the vif_bar_plot function. 
    The tests cover the output of the function including the VIF score dataframe and the bar plot for each explanatory variable.
    
    Examples
    --------
    >>> test_vif_bar_plot()
    """
    
    iris_df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    vif_scores_and_plot = vif_bar_plot(["sepal_length",  "sepal_width"], "petal_width", iris_df, 5)

    # data types of outputs
    assert type(vif_scores_and_plot) == list, "The output should be a list."
    assert type(vif_scores_and_plot[0]) == pd.DataFrame, "The first element of the list should be a data frame."
    assert type(vif_scores_and_plot[1]) == alt.LayerChart, "The second element of the list should be a layered Altair object."

    # dataframe tests
    pd.DataFrame.equals(round(vif_scores_and_plot[0], 3), 
                        pd.DataFrame([[113.940, "Intercept"], 
                                     [1.014, "sepal_length"], 
                                     [1.014, "sepal_width"]],
                                     columns = ["vif_score", "explanatory_var"]
                                    ) 
                       )
    assert vif_scores_and_plot[0].columns.tolist() == ['vif_score', 'explanatory_var'], "Wrong column names."
    assert vif_scores_and_plot[0].dtypes[0] == "float64", "Wrong data type for the VIF scores column."
    assert vif_scores_and_plot[0].dtypes[1] == "object", "Wrong data type for the explantory variable column."
    assert vif_scores_and_plot[0].shape == (len(["sepal_length",  "sepal_width"]) + 1, 2)

    # plot
    assert len(vif_scores_and_plot[1].layer) == 2, "The altair plot must have two layers."
    assert vif_scores_and_plot[1].layer[0].mark == "bar", "Mark should be a bar."
    assert vif_scores_and_plot[1].layer[0].encoding.x.shorthand == "vif_score", "x-axis should be mapped to vif_score."
    assert vif_scores_and_plot[1].layer[0].encoding.y.shorthand == "explanatory_var", "y-axis should be mapped to explanatory_var."
    assert vif_scores_and_plot[1].layer[1].mark.color == "red", "The threshold should be a red line."
    assert vif_scores_and_plot[1].layer[1].mark.type == "rule", "The threshold should be a line spanning the axis."
    assert vif_scores_and_plot[1] == vif_scores_and_plot[1].layer[0] + vif_scores_and_plot[1].layer[1], "The plot should be a layered plot (bar + line)."