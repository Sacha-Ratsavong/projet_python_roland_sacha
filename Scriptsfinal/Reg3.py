'''Fichier comportant de nombreuses fonctions de régressions utilisées tout au long du notebook'''

import statsmodels.api as sm

#Fonction défectueuse pour une raison inconnue au dernier moment
def run_ols(df, y_var, x_vars):
    
    df_ols = df.dropna(subset=[y_var] + x_vars)
    
    # Prépare X et y
    X = df_ols[x_vars]
    X = sm.add_constant(X)  # ajoute l'intercept
    y = df_ols[y_var]
    
    # Ajuste le modèle
    model = sm.OLS(y, X).fit()
    return model








from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


import numpy as np
from scipy.stats import pearsonr
#2 fonctions de calcul de corrélations, "contrôlées" par des variables 
# plus ou moins exogènes dans notre modèle

def partial_corr(x, y, z):
    r_xy = pearsonr(x, y)[0]
    r_xz = pearsonr(x, z)[0]
    r_yz = pearsonr(y, z)[0]
    return (r_xy - r_xz*r_yz) / np.sqrt((1 - r_xz**2)*(1 - r_yz**2))

def correlation_analysis(df):
    df = df.dropna(subset=['Score', 'Dépenses', 'HDI', 'PIB_mean'])
    corr_simple = df['Score'].corr(df['Dépenses'])
    corr_hdi = partial_corr(df['Score'], df['Dépenses'], df['HDI'])
    corr_pib = partial_corr(df['Score'], df['Dépenses'], df['PIB_mean'])
    return corr_simple, corr_hdi, corr_pib




def run_ols(df, variables):
    X = sm.add_constant(df[variables])
    y = df['Score']
    return sm.OLS(y, X).fit()


#Régression en validation non croisée : Calcul de l'estimateur sur une partie des données 
#puis estimation de l'erreur moyenne sur l'autre partie, classique en économétrie 

def train_test_validation(df, variables):
    X = df[variables].values
    y = df['Score'].values

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LinearRegression().fit(X_tr, y_tr)
    y_pred = model.predict(X_te)

    return {
        "R2": r2_score(y_te, y_pred),
        "MSE": mean_squared_error(y_te, y_pred),
        "coef_depenses": model.coef_[0],
        "y_test": y_te,
        "y_pred": y_pred
    }










#Partie Double MCO avec variable instrumentale Z = dépenses passées 
#On ajoute ces dépenses au tableur
def add_lagged_depenses(df, lag_dict={2021: 2016, 2024: 2021}):
    """
    Ajoute une colonne 'Depenses_lag' avec les dépenses de l'édition précédente selon lag_dict.
    """
    def get_prev_depenses(row):
        prev_year = lag_dict.get(row['Year'], None)
        if prev_year:
            match = df[(df['Country'] == row['Country']) & (df['Year'] == prev_year)]
            if not match.empty:
                return match['Dépenses'].values[0]
        return np.nan
    
    df['Depenses_lag'] = df.apply(get_prev_depenses, axis=1)
    n_missing = df['Depenses_lag'].isna().sum()
    if n_missing > 0:
        print(f"⚠ {n_missing} lignes n'ont pas de Depenses_lag et seront ignorées.")
    return df.dropna(subset=['Depenses_lag'])

#Puis on tente d'estimer un effet causal des dépenses sur le score 
# en régressant d'abord les dépenses sur le lag des dépenses

def run_2sls(df, controls=['HDI', 'score_précédent', 'taille_délégation']):
    """
    Effectue la régression 2SLS : 
    1ère étape : Dépenses ~ Dépenses_lag + contrôles
    2ème étape : Score ~ Dépenses_hat + contrôles
    Retourne les résultats (first_stage, second_stage)
    """
    import statsmodels.api as sm
    
    # 1ère étape
    X_first = df[['Depenses_lag'] + controls]
    X_first = sm.add_constant(X_first)
    y_dep = df['Dépenses']
    first_stage = sm.OLS(y_dep, X_first).fit()
    df['Depenses_hat'] = first_stage.fittedvalues

    # 2ème étape
    X_second = df[['Depenses_hat'] + controls]
    X_second = sm.add_constant(X_second)
    y_score = df['Score']
    second_stage = sm.OLS(y_score, X_second).fit()

    return first_stage, second_stage
