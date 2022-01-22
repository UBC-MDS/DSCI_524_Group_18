from collinearity_tool import collinearity_tool
import pandas as pd


def test_corr_matrix():
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
    actual = corr_matrix(df_1, decimals = 2)
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
    actual = corr_matrix(df_2, decimals = 2)
    assert actual.equals(expected) == True, "The correlation coefficient matrix should only return 1 row."
    
    data_3 = {'A': ['1', '2'],
              'B': ['2', '2']
             }
    df_3 = pd.DataFrame(data_2,columns=['A','B'])
    
    actual = corr_matrix(df_3, decimals = 2)
    assert actual == None, "The correlation coefficient matrix should only return None."