import matplotlib.pyplot as plt
import seaborn as sns

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
