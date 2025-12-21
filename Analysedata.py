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

# Charger athlete_events pour taille_délégation
df_athletes = pd.read_csv('data/raw/athlete_events.csv')
df_athletes['Year'] = df_athletes['Year'].astype(int)

# Compter le nombre d'athlètes uniques par NOC et Year
delegation_size = df_athletes.groupby(['Year', 'NOC'])['ID'].nunique().reset_index()
delegation_size = delegation_size.rename(columns={'NOC': 'Country Code', 'ID': 'taille_délégation'})

# Merger avec df_clean
df_clean = df_clean.merge(delegation_size, on=['Year', 'Country Code'], how='left')

# Supprimer les NaN supplémentaires si nécessaire
df_clean = df_clean.dropna(subset=['score_précédent', 'taille_délégation'])

print(f"Nombre de lignes après ajout des variables: {len(df_clean)}")

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

#%% Régression mise à jour
# Modèle complet
X = df_clean[['Dépenses', 'HDI', 'score_précédent', 'taille_délégation']]
X = sm.add_constant(X)
y = df_clean['Score']
model_full = sm.OLS(y, X).fit()
print("\nRégression Score ~ Dépenses + HDI + Score_précédent + Taille_délégation:")
print(model_full.summary())

# Sauvegarder le summary
with open('regression_summary.txt', 'w') as f:
    f.write(str(model_full.summary()))
print("Summary sauvegardé dans 'regression_summary.txt'")
