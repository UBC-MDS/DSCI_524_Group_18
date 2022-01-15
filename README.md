# collinearity_tool

## 1. Description

## 1.3. Package ecosystems

**variance_inflation_factor()**
This package aims to fill the simplify the decision-making process while addressing multicollinearity. This tool brings several other packages together into one interface.
It relies on existing package, variance_inflation_factor() by _statsmodels_ [documentation](https://www.statsmodels.org/dev/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html). The VIF package calculates the VIF score which predicts how well the variable can be predicted using other explanatory variables in the dataset using linear regression. Higher values highlight multicollinearity problems.
The output is a simple dataframe with two columns: feature (variable name) and VIF (VIF value).

**scipy.stats.linregress**
_Scipy_'s is another necessary package for this collinearity tool. This package conducts linear regression using `linregress` and provides necessary statistical information, including r-squared.
For more information on the package, please see the following [documentation](https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.linregress.html).

**Altair**
_Altair_ is a popular plotting package. It provides the necessary tools to create the heatmap for the collinearity tool. For more information on Altair and heatmaps, please refer to this [example](https://altair-viz.github.io/gallery/simple_heatmap.html).


Identify multicollinearity issues by correlation, VIF, and visualizations.

## 2. Installation

```bash
$ pip install collinearity_tool
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
