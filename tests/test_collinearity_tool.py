from collinearity_tool import collinearity_tool
import altair as alt
import numpy as np
import pandas as pd

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