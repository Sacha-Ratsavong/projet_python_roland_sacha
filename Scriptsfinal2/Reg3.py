import statsmodels.api as sm


def run_ols(df, y_var, x_vars):
    """
    Estime une régression linéaire (OLS) à partir d’un DataFrame.

    Paramètres :
    - df : DataFrame contenant les données
    - y_var : nom de la variable dépendante
    - x_vars : liste des variables explicatives

    Retour :
    - objet résultat statsmodels (OLSResults)
    """

    # Sélection des variables explicatives
    X = df[x_vars]

    # Ajout de la constante (intercept)
    X = sm.add_constant(X)

    # Variable dépendante
    y = df[y_var]

    # Estimation du modèle OLS
    model = sm.OLS(y, X).fit()

    return model