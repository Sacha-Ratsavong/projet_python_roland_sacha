#Code dédié à la production de résultats sur les données de df_merged_final

#En premier lieu, on doit un peu traiter le dataset df_merged_final (on ne travaille plus que sur celui-ci)
#%% Etapes de téléchargement et cleaning rapide
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = pd.read_csv('data_clean/df_merged_final.csv')
df = df[(df["Country"] != "Cyprus") & (df["Country"] != "Croatia") & (df["Country"] != "Czechia") & (df["Country"] != "Slovakia")]

# Ajouter les données pour les États-Unis
# Données FRED en milliards USD, converties en % PIB
# PIB US (en milliards USD): 2016: 18569.1, 2021: 23315.1, 2024: 28750.96
# Dépenses FRED: 2016: 33.024, 2021: 40.503, 2024: 43.342 (proxy 2023)
us_data = pd.DataFrame({
    'Year': [2016.0, 2021.0, 2024.0],
    'Country': ['United States', 'United States', 'United States'],
    'Score': [278.0, 254.0, 277.0],  # Scores depuis df_score
    'Country Code': ['USA', 'USA', 'USA'],
    'PIB_mean': [54252.16, 63138.21, 73968.61],  # Depuis df_PIB_hab.csv
    'HDI': [0.928, 0.928, 0.928],  # Depuis df_IDH.csv (stable)
    'Dépenses': [(33.024 / 18569.1) * 100, (40.503 / 23315.1) * 100, (43.342 / 28750.96) * 100]  # % PIB
})

df = pd.concat([df, us_data], ignore_index=True)

# Convertir les colonnes numériques
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
df['PIB_mean'] = pd.to_numeric(df['PIB_mean'], errors='coerce')
df['HDI'] = pd.to_numeric(df['HDI'], errors='coerce')
df['Dépenses'] = pd.to_numeric(df['Dépenses'], errors='coerce')

# Supprimer les lignes avec NaN dans les colonnes clés
df_clean = df.dropna(subset=['Score', 'Dépenses', 'HDI', 'PIB_mean'])

print("Nombre de lignes après nettoyage:", len(df_clean))


#%% Analyse de corrélation
# Corrélation simple entre Score et Dépenses
corr_simple = df_clean['Score'].corr(df_clean['Dépenses'])
print(f"Corrélation simple entre Score et Dépenses: {corr_simple:.3f}")

# Corrélation partielle contrôlant pour HDI
from scipy.stats import pearsonr

def partial_corr(x, y, z):
    # Corrélation partielle entre x et y contrôlant pour z
    r_xy = pearsonr(x, y)[0]
    r_xz = pearsonr(x, z)[0]
    r_yz = pearsonr(y, z)[0]
    return (r_xy - r_xz * r_yz) / np.sqrt((1 - r_xz**2) * (1 - r_yz**2))

partial_corr_hdi = partial_corr(df_clean['Score'], df_clean['Dépenses'], df_clean['HDI'])
print(f"Corrélation partielle Score-Dépenses contrôlant pour HDI: {partial_corr_hdi:.3f}")

partial_corr_pib = partial_corr(df_clean['Score'], df_clean['Dépenses'], df_clean['PIB_mean'])
print(f"Corrélation partielle Score-Dépenses contrôlant pour PIB: {partial_corr_pib:.3f}")

'''
#%% Visualisation
plt.figure(figsize=(12, 5))

# Scatter plot avec HDI
plt.subplot(1, 2, 1)
sns.scatterplot(data=df_clean, x='Dépenses', y='Score', hue='HDI', palette='viridis')
plt.title('Score vs Dépenses (couleur: HDI)')
plt.xlabel('Dépenses (% PIB)')
plt.ylabel('Score Olympique')

# Scatter plot avec PIB
plt.subplot(1, 2, 2)
sns.scatterplot(data=df_clean, x='Dépenses', y='Score', hue='PIB_mean', palette='plasma')
plt.title('Score vs Dépenses (couleur: PIB/hab)')
plt.xlabel('Dépenses (% PIB)')
plt.ylabel('Score Olympique')

plt.tight_layout()
plt.show()
'''

#%% Régression linéaire
import statsmodels.api as sm

# Modèle avec HDI
X = df_clean[['Dépenses', 'HDI']]
X = sm.add_constant(X)
y = df_clean['Score']
model_hdi = sm.OLS(y, X).fit()
print("\nRégression Score ~ Dépenses + HDI:")
print(model_hdi.summary())

# Modèle avec PIB
X = df_clean[['Dépenses', 'PIB_mean']]
X = sm.add_constant(X)
model_pib = sm.OLS(y, X).fit()
print("\nRégression Score ~ Dépenses + PIB:")
print(model_pib.summary())





#%% Ajouter variables supplémentaires : score_précédent et taille_délégation
# Charger df_score
df_score = pd.read_csv('data_clean/df_score.csv')
df_score = df_score.rename(columns={'Team': 'Country'})

# Calculer score_précédent : moyenne des 3 éditions précédentes
df_score['Year'] = df_score['Year'].astype(int)
df_clean['Year'] = df_clean['Year'].astype(int)

# Fonction pour calculer la moyenne des scores précédents
def get_prev_score_avg(country, year, df_score, n=3):
    prev_years = df_score[(df_score['Country'] == country) & (df_score['Year'] < year)]['Year'].nlargest(n)
    if len(prev_years) == 0:
        return np.nan
    scores = df_score[(df_score['Country'] == country) & (df_score['Year'].isin(prev_years))]['Score']
    return scores.mean() if len(scores) > 0 else np.nan

df_clean['score_précédent'] = df_clean.apply(lambda row: get_prev_score_avg(row['Country'], row['Year'], df_score, 3), axis=1)
pd.set_option('display.max_rows', None)
print("DataFrame df_clean :")
print(df_clean)
# Charger athlete_events pour taille_délégation
df_athletes = pd.read_csv('data/raw/athlete_events.csv')
df_athletes['Year'] = df_athletes['Year'].astype(int)

# Compter le nombre d'athlètes uniques par NOC et Year
delegation_size = df_athletes.groupby(['Year', 'NOC'])['ID'].nunique().reset_index()
delegation_size = delegation_size.rename(columns={'NOC': 'Country Code', 'ID': 'taille_délégation'})

# Ajouter les données scrapées pour 2021 et 2024
delegation_2021 = {
    'FRA': 398,
    'GER': 425,
    'ITA': 384,
    'ESP': 321,
    'NED': 278,
    'POL': 210,
    'SWE': 134,
    'GRE': 83,
    'AUT': 60,
    'CRO': 59,
    'SLO': 53,
    'FIN': 45,
    'BUL': 42,
    'LTU': 42,
    'SVK': 41,
    'POR': 92,
    'CZE': 115,
    'BEL': 121,
    'IRL': 116,
    'DEN': 107,
    'HUN': 166,
    'ROU': 101,
    'EST': 33,
    'LAT': 33,
    'LUX': 12,
    'MLT': 6,
    'CYP': 15,
    'USA': 620
}

delegation_2024 = {
    'FRA': 571,
    'GER': 427,
    'ITA': 403,
    'ESP': 383,
    'NED': 275,
    'POL': 210,
    'SWE': 128,
    'GRE': 101,
    'AUT': 81,
    'CRO': 73,
    'POR': 73,
    'DEN': 133,
    'IRL': 133,
    'FIN': 57,
    'HUN': 180,
    'CZE': 111,
    'ROU': 106,
    'BEL': 165,
    'BUL': 46,
    'LTU': 50,
    'SVK': 28,
    'SLO': 90,
    'EST': 25,
    'LAT': 29,
    'LUX': 13,
    'MLT': 5,
    'CYP': 15,
    'USA': 591
}

# Créer DataFrames pour les ajouter
df_2021 = pd.DataFrame({
    'Year': 2021,
    'Country Code': list(delegation_2021.keys()),
    'taille_délégation': list(delegation_2021.values())
})

df_2024 = pd.DataFrame({
    'Year': 2024,
    'Country Code': list(delegation_2024.keys()),
    'taille_délégation': list(delegation_2024.values())
})

delegation_size = pd.concat([delegation_size, df_2021, df_2024], ignore_index=True)
# Merger avec df_clean
df_clean = df_clean.merge(delegation_size, on=['Year', 'Country Code'], how='left')

# Supprimer les NaN supplémentaires si nécessaire
df_clean = df_clean.dropna(subset=['score_précédent', 'taille_délégation'])
df_clean.to_csv("data_clean/df_used_for_regression.csv")
print(f"Nombre de lignes après ajout des variables: {len(df_clean)}")

'''
#%% Visualisation mise à jour
plt.figure(figsize=(18, 6))

# Scatter plot avec HDI
plt.subplot(1, 3, 1)
sns.scatterplot(data=df_clean, x='Dépenses', y='Score', hue='HDI', palette='viridis')
plt.title('Score vs Dépenses (HDI)')

# Scatter plot avec score_précédent
plt.subplot(1, 3, 2)
sns.scatterplot(data=df_clean, x='Dépenses', y='Score', hue='score_précédent', palette='coolwarm')
plt.title('Score vs Dépenses (Score précédent)')

# Scatter plot avec taille_délégation
plt.subplot(1, 3, 3)
sns.scatterplot(data=df_clean, x='Dépenses', y='Score', hue='taille_délégation', palette='plasma')
plt.title('Score vs Dépenses (Taille délégation)')

plt.tight_layout()
plt.show()
'''



#%% Régression mise à jour
# Modèle complet
X = df_clean[['Dépenses', 'HDI', 'score_précédent', "taille_délégation"]] #Rajouter/enlever HDI, taille_délégation et score_précédent si besoin
X = sm.add_constant(X)
y = df_clean['Score']
model_full = sm.OLS(y, X).fit()
print("\nRégression Score ~ Dépenses + HDI + Score_précédent + Taille_délégation:")
print(model_full.summary())

# Modèle sans USA
df_no_usa = df_clean[df_clean['Country'] != 'United States']
X_no_usa = df_no_usa[['Dépenses', 'HDI', 'score_précédent', 'taille_délégation']]
X_no_usa = sm.add_constant(X_no_usa)
y_no_usa = df_no_usa['Score']
model_no_usa = sm.OLS(y_no_usa, X_no_usa).fit()
print("\nRégression Score ~ Dépenses + HDI + Score_précédent + Taille_délégation (sans USA):")
print(model_no_usa.summary())

# Sauvegarder le summary sans USA
from datetime import datetime
timestamp_no_usa = datetime.now().strftime("%Y%m%d_%H%M%S")
filename_no_usa = f'regression_summary_no_usa_{timestamp_no_usa}.txt'
#with open(filename_no_usa, 'w') as f:
    #f.write(str(model_no_usa.summary()))
#print(f"Summary sans USA sauvegardé dans '{filename_no_usa}'")

# Validation train-test 
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

X_sk = X.values
y_sk = y.values
X_train, X_test, y_train, y_test = train_test_split(X_sk, y_sk, test_size=0.3, random_state=42)
model_tt = LinearRegression()
model_tt.fit(X_train, y_train)
y_pred = model_tt.predict(X_test)
r2_tt = r2_score(y_test, y_pred)
mse_tt = mean_squared_error(y_test, y_pred)
print(f"\nTrain-test validation: R² = {r2_tt:.3f}, MSE = {mse_tt:.3f}")
print(f"Coefficient de Dépenses estimé: {model_tt.coef_[1]:.3f}")

# Sauvegarder le summary
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'regression_summary_{timestamp}.txt'
#with open(filename, 'w') as f:
    #f.write(f"Train-test validation: R² = {r2_tt:.3f}, MSE = {mse_tt:.3f}\n")
    #f.write(f"Coefficient de Dépenses estimé: {model_tt.coef_[1]:.3f}\n")
#print(f"Summary sauvegardé dans '{filename}'")




# Graphiques comparatifs
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))

# Graphique pour OLS (échantillon complet)
plt.subplot(1, 2, 1)
plt.scatter(y, model_full.fittedvalues, alpha=0.7, color='blue')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', label='Ligne d\'égalité')
plt.xlabel('Scores réels')
plt.ylabel('Scores prédits (OLS)')
plt.title('Prédictions OLS (échantillon complet)\nCoef Dépenses: 2.05, p=0.204')
plt.legend()
plt.grid(True)

# Graphique pour Train-Test
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_pred, alpha=0.7, color='green')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ligne d\'égalité')
plt.xlabel('Scores réels (test)')
plt.ylabel('Scores prédits (Train-Test)')
plt.title('Prédictions Train-Test\nCoef Dépenses: 1.26, R²=0.969')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Régression avec interaction continue : effet des dépenses selon score_précédent
X_int = df_clean[['Dépenses', 'HDI', 'score_précédent', 'taille_délégation']]
X_int['Depenses_score_prec'] = X_int['Dépenses'] * X_int['score_précédent']
X_int = sm.add_constant(X_int)
y_int = df_clean['Score']
model_int = sm.OLS(y_int, X_int).fit()
print("\nRégression avec interaction continue Dépenses * score_précédent:")
print(model_int.summary())

# Sauvegarder le summary interaction continue
timestamp_int = datetime.now().strftime("%Y%m%d_%H%M%S")
filename_int = f'regression_summary_interaction_continue_{timestamp_int}.txt'
with open(filename_int, 'w') as f:
    f.write(str(model_int.summary()))
print(f"Summary interaction continue sauvegardé dans '{filename_int}'")




# %%
