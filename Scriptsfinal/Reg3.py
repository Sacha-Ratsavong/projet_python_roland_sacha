import statsmodels.api as sm

def run_ols(df, y_var, x_vars):
    X = df[x_vars]
    X = sm.add_constant(X)
    y = df[y_var]

    model = sm.OLS(y, X).fit()
    return model
