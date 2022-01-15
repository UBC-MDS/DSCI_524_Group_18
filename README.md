# collinearity_tool

## Functions 

- `corr_matrix`: A function that returns a correlation matrix for all numerical variables in a data frame.
- `corr_heatmap`: A function that returns a correlation heatmap given a dataframe.
- `vif_bar_plot`: A function that returns a list containing a data frame for Variable Inflation Factors (VIF) and a bar chart of the VIFs for each explanatory variable in a multiple linear regression model.
- `ol_identify`: A function that identifies multicollinearity based on highly correlated pairs (using Pearson coefficient) with VIF values exceeding the threshold

## Installation

```bash
$ pip install collinearity_tool
```

## Usage

- TODO

## Contributors
- Anahita Einolghozati
- Chaoran Wang
- Katia Aristova
- Lisheng Mao

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`collinearity_tool` was created by Anahita Einolghozati, Chaoran Wang, Katia Aristova, Lisheng Mao. It is licensed under the terms of the MIT license.

## Credits

`collinearity_tool` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
