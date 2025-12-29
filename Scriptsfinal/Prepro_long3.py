import pandas as pd

def prepare_data_long(df, df_previous):
    # Ajoute variables nécessaires au modèle long (score précédent, etc.)
    

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
            "Country"
        ],
        how="right"
    )

    df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], errors="ignore")

    df = df.dropna(subset=[
        "Dépenses_volume",
        "score_précédent",
        "Score"
    ])

    return df
