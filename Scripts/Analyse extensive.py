#Code visant à étudier la relation score/dépenses en prenant les dépenses en termes de volume et plus de pourcentage du PIB

#%%
import pandas as pd
df = pd.read_csv('../data_clean/df_merged_final2.csv')
df = df[(df["Country"] != "Cyprus") & (df["Country"] != "Croatia") & (df["Country"] != "Czechia") & (df["Country"] != "Slovakia")]

# Merger avec PIB_EU_long pour ajouter la colonne PIB
df_pib_long = pd.read_csv('../data_clean/PIB_EU_long.csv')
df = pd.merge(df, df_pib_long, on=['Year', 'Country Code'], how='left')
df
# Transformer les dépenses de % du PIB en volume (milliards de SPA)
df['Dépenses_volume'] = df['Dépenses'] * df['PIB'] / 100

# Enlever les lignes où PIB est manquant
df = df.dropna(subset=['PIB'])

# Supprimer toutes les lignes avec des NaN dans les colonnes utilisées pour la régression
df = df.dropna(subset=['Score', 'Dépenses_volume', 'HDI', 'PIB_mean'])
#df.to_csv("../data_clean/df_with_dépenses.csv")


# %%
#Représentation graphique de ces nouvelles données
import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plot avec droite de régression
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='Dépenses_volume', y='Score', scatter_kws={'alpha':0.7}, line_kws={'color':'red'})
plt.title('Corrélation entre Score Olympique et Dépenses en Volume (Milliards SPA)')
plt.xlabel('Dépenses en Volume (Milliards SPA)')
plt.ylabel('Score Olympique')
plt.grid(True)
plt.show()

# %%
# Régression linéaire
import statsmodels.api as sm

# Modèle simple : Score ~ Dépenses_volume
X = df[['Dépenses_volume']]
X = sm.add_constant(X)
y = df['Score']
model = sm.OLS(y, X).fit()
print("Régression Score ~ Dépenses_volume :")
print(model.summary())

#Lecture : Le modèle prédit qu'un investissement public à hauteur d'un milliard de SPA 
#en sport, loisir et culte permet une augmentation de 1,73 du score olympique

# Save
with open('../ResultsV2/regression_simple_volume.txt', 'w') as f:
    f.write(str(model.summary()))




#%%
# Modèle avec contrôles : Score ~ Dépenses_volume + PIB_mean
import statsmodels.api as sm
X_full = df[['Dépenses_volume', 'PIB_mean']]
X_full = sm.add_constant(X_full)
y = df['Score']
model_V2 = sm.OLS(y, X_full).fit()
print("\nRégression Score ~ Dépenses_volume + HDI + PIB_mean :")
print(model_V2.summary())

#Résultats peu intéressants par rapport à régression courte, testons d'autres régresseurs

# %%
#Maintenant, rajoutons les données utilisées dans les régressions avec les dépenses en pourcentage du PIB
import statsmodels.api as sm
df_previous = pd.read_csv("../data_clean/df_used_for_regression2.csv")
df_complet = pd.merge(df, df_previous, on=['Year', 'Country Code', 'Score', 'Dépenses', 'HDI', 'PIB_mean', 'Country', 'Unnamed: 0' ], how='right')
df_complet = df_complet.drop(columns = ["Unnamed: 0", "Unnamed: 0.1"] )
df_complet
# Supprimer les lignes avec NaN dans les variables de la régression
df_complet = df_complet.dropna(subset=['Dépenses_volume', 'taille_délégation', 'score_précédent', 'Score'])

#Cette régression est assurément la plus pertinente, on la garde
X = df_complet[['Dépenses_volume', 'score_précédent']]
X = sm.add_constant(X)
y = df_complet['Score']
model_V3 = sm.OLS(y, X).fit()
print(model_V3.summary())

# Save
with open('../ResultsV2/regression_longue_volume.txt', 'w') as f:
    f.write(str(model_V3.summary()))


#On remarque un biais positif de variable omise : on surestimait l'effet des dépenses publiques 
#Quand on ne contrôlait pas par le score précédent, c'est-à-dire le niveau historique du pays


#Bilan : 
#Il est possible que la variable omise permettant de prédire le score olympique plus précisément encore soit la population :

#On peut penser que le niveau sportif des individus au sein d'une population est probabiliste et
#peut être modélisé par une loi manipulable (disons une gaussienne pour se fixer les idées) ; ainsi on pourrait établir un lien entre taille de la population et performances  olympiques, 
# en considérant que le nombre de grands sportifs correspond au nombre d'occurence de valeurs extrêmes d’une loi normale. 
# Une population de grande taille correspondrait à une loi du Khi2 avec un grand nombre de degrés de liberté, 
# produisant des sportifs de très haut niveau en quantité.

#Pour différencier les pays entre eux et expliquer par exemple les mauvaises performances de l'Inde malgré son immenses population, 
# on pourrait considérer que les dépenses publiques servent à redresser l'espérance de la gaussienne 
# (infrastructures sportives, subventions de la pratique sportive, heures de sport à l'école), 
# ou bien à rendre les valeurs extrêmement élevées plus probables (cursus scolaires aménagés pour les sportifs de haut niveau, clubs d'élite, etc. )

# %%
