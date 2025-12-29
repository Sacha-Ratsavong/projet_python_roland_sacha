import matplotlib.pyplot as plt
import seaborn as sns


def plot_score_vs_spending(df, save_path=None):
    """
    Trace la relation entre le score olympique et les dépenses sportives
    exprimées en volume.

    Le graphique combine :
    - un nuage de points (pays-année)
    - une droite de régression linéaire
    """

    # Création de la figure
    plt.figure(figsize=(10, 6))

    # Nuage de points + régression linéaire
    sns.regplot(
        data=df,
        x="Dépenses_volume",
        y="Score",
        scatter_kws={"alpha": 0.7},
        line_kws={"color": "red"}
    )

    # Mise en forme du graphique
    plt.title("Score olympique vs dépenses sportives (volume)")
    plt.xlabel("Dépenses (milliards SPA)")
    plt.ylabel("Score olympique")
    plt.grid(True)

    # Affichage
    plt.show()