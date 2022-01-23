# collinearity_tool
Identify multicollinearity issues by correlation, VIF, and visualizations. This package is designed for beginners of Python who want to identify multicollinearity issues by applying a simple function. It automates the process of building a proper correlation matrix, creating correlation heat map and identifying pairwise highly correlated variables. An R version of package is also in the progress of development.


## 1. Description

## Functions 

The following four functions are in the collinearity_tool package:
- `corr_matrix`: A function that returns a generic correlation matrix and a longer form one for all numerical variables in a data frame.
- `corr_heatmap`: A function that returns a correlation heatmap given a dataframe.
- `vif_bar_plot`: A function that returns a list containing a data frame for Variable Inflation Factors (VIF) and a bar chart of the VIFs for each explanatory variable in a multiple linear regression model.
- `col_identify`: A function that identifies multicollinearity based on highly correlated pairs (using Pearson coefficient) with VIF values exceeding the threshold.

## Package ecosystems

**Motivation** 
This package aims to fill the simplify the decision-making process while addressing multicollinearity. This tool brings several other packages together into one interface.
Multicollinearity tools exist but they do not encompass all of the components included in this tool.

For example, linear regression, plotting tools and correlation matrix packages are already part of the Python ecosystem (as part of Pandas, Scipy, and so on).
What makes this package different is that it combines the tools together to create a single package that will allow the researcher to locate troublesome multicollinearity issues.

In addition, the collinearity_tool helps new users, unfamiliar with Python and its broad ecosystem, to plot and deduce multicollinearity without prior knowledge of plotting, calculating VIFF's or manipulating data to create plots and tables.

`variance_inflation_factor()`
This function is necessary to calculate VIF. It is part of the _statsmodels_ [documentation](https://www.statsmodels.org/dev/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html) package. The VIF package calculates the VIF score which predicts how well the variable can be predicted using other explanatory variables in the dataset using linear regression. Higher values highlight multicollinearity problems.
The output is a simple dataframe with two columns: feature (variable name) and VIF (VIF value).

`scipy.stats.linregress`  
Scipy is a necessary package for this collinearity tool. This package conducts linear regression using `linregress` and provides necessary statistical information. For more information on the package, please see the following [documentation](https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.linregress.html).

**Pandas**: `corr()`    
Pandas is another necessary package for this collinearity tool. This package conducts linear regression using and produces a correlation matrix using `corr`. The output is a DataFrame in the shape of a correlation matrix.
For more information on the package, please see the following [documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)).

**Altair**  
_Altair_ is a popular plotting package. It provides the necessary tools to create the heatmap for the collinearity tool. For more information on Altair and heatmaps, please refer to this [example](https://altair-viz.github.io/gallery/simple_heatmap.html).

## 2. Installation

```bash
$ pip install git+https://github.com/UBC-MDS/collinearity_tool.git
```

## 3. Usage

- TODO

## 4. Contributors
- Anahita Einolghozati
- Chaoran Wang
- Katia Aristova
- Lisheng Mao

## 5. Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## 6. License

`collinearity_tool` was created by Anahita Einolghozati, Chaoran Wang, Katia Aristova, Lisheng Mao. It is licensed under the terms of the MIT license.

## 7. Credits

`collinearity_tool` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
