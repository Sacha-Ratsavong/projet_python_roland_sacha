import pandas as pd


def prepare_data_long(df, df_previous):
    """
    Enrichit un DataFrame destiné à un modèle en panel (format long)
    en y intégrant des variables issues d’un DataFrame précédent
    (ex. score à la période précédente).

    Objectif :
    - obtenir un dataset exploitable pour analyser la dynamique
      de la performance olympique dans le temps
    """

    # Fusion avec le DataFrame contenant les variables retardées
    df = pd.merge(
        df,
        df_previous,
        on=[
            "Year",
            "Country Code",
            "Score",
            "Dépenses",
            "HDI",
            "PIB_mean",
            "Country",
        ],
        how="right"
    )

    # Suppression des colonnes d’index parasites éventuellement présentes
    df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], errors="ignore")

    # Suppression des observations incomplètes pour les variables clés du modèle
    df = df.dropna(
        subset=[
            "Dépenses_volume",
            "score_précédent",
            "Score",
        ]
    )

    return df