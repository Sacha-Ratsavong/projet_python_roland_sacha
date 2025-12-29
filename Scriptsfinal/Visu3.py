''' Enesemble des fonctions de représentation graphique'''

import matplotlib.pyplot as plt
import seaborn as sns

#Une première pour la corrélation entre score olympique et dépenses (en volume)
def plot_score_vs_spending(df, save_path=None):
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=df,
        x="Dépenses_volume",
        y="Score",
        scatter_kws={"alpha": 0.7},
        line_kws={"color": "red"}
    )

    plt.title("Score olympique vs dépenses sportives (volume)")
    plt.xlabel("Dépenses (milliards SPA)")
    plt.ylabel("Score olympique")
    plt.grid(True)

    

    plt.show()




#Une seconde pour l'IDH au cours du temps
def plot_hdi_over_time(df, countries):
    
    
    # Filtrage des pays + suppression des années manquantes
    df_plot = df[df["Country"].isin(countries)].dropna(subset=["Year"])

    # Sécurité : tri par année
    df_plot = df_plot.sort_values("Year")

    plt.figure(figsize=(10, 6))

    for country in countries:
        data = df_plot[df_plot["Country"] == country]
        plt.plot(data["Year"], data["HDI"], marker='o', label=country)

    plt.title("Évolution de l'IDH au cours du temps")
    plt.xlabel("Année")
    plt.ylabel("IDH")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.show()


import matplotlib.pyplot as plt

#Trace l'évolution du nombre de médailles pour les n premiers pays aux JO (classement historique)
# (on prendra par exemple n = 5)
def plot_top_countries_medals(df, top_n=5):
    

    # Sélection des top N pays les plus titrés
    top_countries = (
        df.groupby('Team')['Count']
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    # Filtrage
    df_top = df[df['Team'].isin(top_countries)]

    # Agrégation par année et pays
    df_agg = (
        df_top
        .groupby(['Year', 'Team'])['Count']
        .sum()
        .reset_index()
    )

    # Mise en forme pour le plot
    df_pivot = (
        df_agg
        .pivot(index='Year', columns='Team', values='Count')
        .fillna(0)
        .sort_index()
    )

    # Plot
    plt.figure(figsize=(15, 8))

    for country in df_pivot.columns:
        plt.plot(
            df_pivot.index,
            df_pivot[country],
            marker='o',
            label=country
        )

    plt.title(f"Évolution des médailles des {top_n} pays les plus titrés aux JO")
    plt.xlabel("Édition des JO")
    plt.ylabel("Nombre de médailles")

    plt.xticks(df_pivot.index, rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()




#Trois corrélations visuelles entre score et dépenses contrôlées par différentes variables 
#L'impact de la troisième variable est modélisé par la couleurs des points à chaque fois

def scatter_controls(df):
    plt.figure(figsize=(18,6))

    plt.subplot(1,3,1)
    sns.scatterplot(df, x='Dépenses', y='Score', hue='HDI')
    plt.title('Score vs Dépenses (% PIB) – contrôle HDI')
    plt.xlabel('Dépenses (% PIB)')
    plt.ylabel('Score Olympique')

    plt.subplot(1,3,2)
    sns.scatterplot(df, x='Dépenses', y='Score', hue='score_précédent', palette='coolwarm')
    plt.title('Score vs Dépenses (% PIB) – contrôle score précédent')
    plt.xlabel('Dépenses (% PIB)')
    plt.ylabel('Score Olympique')

    plt.subplot(1,3,3)
    sns.scatterplot(df, x='Dépenses', y='Score', hue='taille_délégation', palette='plasma')
    plt.title('Score vs Dépenses (% PIB) – contrôle taille délégation')
    plt.xlabel('Dépenses (% PIB)')
    plt.ylabel('Score Olympique')

    plt.tight_layout()
    plt.show()


#Représentation graphique des deux régressions de la partie 2.2

def plot_regression_results(y_full, fitted_full, y_test, y_pred):
    plt.figure(figsize=(12,5))

    # MCO complet
    plt.subplot(1,2,1)
    plt.scatter(y_full, fitted_full, alpha=0.7, color='blue')
    plt.plot([y_full.min(), y_full.max()], [y_full.min(), y_full.max()], 'r--', label='Ligne d\'égalité')
    plt.xlabel('Scores réels')
    plt.ylabel('Scores prédits (OLS)')
    plt.title('Prédictions OLS (échantillon complet)')
    plt.legend()
    plt.grid(True)

    # Train-Test
    plt.subplot(1,2,2)
    plt.scatter(y_test, y_pred, alpha=0.7, color='green')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ligne d\'égalité')
    plt.xlabel('Scores réels (test)')
    plt.ylabel('Scores prédits (Train-Test)')
    plt.title('Prédictions Train-Test')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
