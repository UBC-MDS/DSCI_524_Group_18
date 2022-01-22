from collinearity_tool import collinearity_tool
from collinearity_tool.collinearity_tool vif_bar_plot

import altair as alt
import numpy as np
import pandas as pd

def test_corr_matrix():
    """
    Test if the correlation matrix returns the correct value and if it works
    in some edge cases where the inputs only have one or no numeric variables.
    3 tests in total.
    
    Examples
    --------
    >>> test_corr_matrix()
    """
    
    data_1 = {'A': [1,2,3,4,5],
        'B': [2,4,6,8,10],
        'C': [10,8,6,4,2],
        "D":['abc','322', '324', '32', '23']
        }

    df_1 = pd.DataFrame(data_1,columns=['A','B','C', 'D'])
    
    result = {"variable1": ["A","A","A", "B","B","B", "C", "C","C"],
          "variable2": ["A", "B", "C","A", "B", "C","A", "B", "C"],
          "correlation": [1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, -1.0, 1.0],
          "rounded_corr": [1.00, 1.00, -1.00, 1.00, 1.00, -1.00, -1.00, -1.00, 1.00]
             }
    expected = pd.DataFrame(result, columns=["variable1","variable2","correlation", "rounded_corr"])
    actual = corr_matrix(df_1, decimals = 2)[0]
    assert actual.equals(expected) == True, "The correlation coefficient matrix is incorrect."
    
    data_2 = {'A': [1, 2],
              'B': ['2', '2']
             }
    df_2 = pd.DataFrame(data_2,columns=['A','B'])
    
    result = {"variable1": ["A"],
          "variable2": ["A"],
          "correlation": [1.0],
          "rounded_corr": [1.00]
             }
    expected = pd.DataFrame(result, columns=["variable1","variable2","correlation", "rounded_corr"])
    actual = corr_matrix(df_2, decimals = 2)[0]
    assert actual.equals(expected) == True, "The correlation coefficient matrix should only return 1 row."
    
    data_3 = {'A': ['1', '2'],
              'B': ['2', '2']
             }
    df_3 = pd.DataFrame(data_2,columns=['A','B'])
    
    actual = corr_matrix(df_3, decimals = 2)[0]
    assert actual == None, "The correlation coefficient matrix should only return None."

def test_corr_heatmap():
    """Test corr_heatmap function
    
    Parameters
    ----------
    
    Examples
    --------
    >>> test_corr_heatmap(heatmap)
    """

    data = {'A': [1,2,3,4,5],
        'B': [2,4,6,8,10],
        'C': [10,8,6,4,2],
        "D":['abc','322', '324', '32', '23']
        }
    
    df = pd.DataFrame(data, columns=['A','B','C', 'D'])
    
    heatmap = corr_heatmap(df, scheme='purplegreen')
    
    assert isinstance(heatmap, alt.LayerChart)
    assert len(heatmap.layer) == 2, 'the heatmap does not have base and label on it'
    assert heatmap.layer[0].mark == 'rect', 'mark of base should be a rectangle'
    assert heatmap.layer[0].encoding.x.shorthand == 'variable1', 'x_axis should be mapped to the variable1'
    assert heatmap.layer[0].encoding.y.shorthand == 'variable2', 'y_axis should be mapped to the variable2'
    assert heatmap.layer[0].encoding.color.shorthand == 'correlation', 'y_axis should be mapped to the correlation'
    assert heatmap.layer[0].encoding.color.scale.domain == [-1, 1], "correlation should has domain to be [-1, 1]"
    assert heatmap.layer[0].encoding.x.type == 'nominal', "x-axis should be ordinal"
    assert heatmap.layer[0].encoding.y.type == 'nominal', "y-axis should be ordinal"
    assert heatmap.layer[0].encoding.color.type == 'quantitative', "color should be quantitative"
    assert heatmap.layer[1].mark == 'text', 'mark of label should be a text'
    assert heatmap.layer[1].encoding.text.shorthand == 'rounded_corr', 'text should be mapped to the rounded correlation'

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
