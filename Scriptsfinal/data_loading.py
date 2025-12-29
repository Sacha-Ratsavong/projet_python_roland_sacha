import pandas as pd

def clean_main_df(df):
    """
    Supprime les pays problématiques et convertit les colonnes numériques.
    """
    excluded = ["Cyprus", "Croatia", "Czechia", "Slovakia"]
    df = df[~df["Country"].isin(excluded)].copy()

    for col in ['Score', 'PIB_mean', 'HDI', 'Dépenses']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def add_us_data(df):
    """
    Ajoute les données des USA.
    """
    us_data = pd.DataFrame({
        'Year': [2016, 2021, 2024],
        'Country': ['United States']*3,
        'Score': [278, 254, 277],
        'Country Code': ['USA']*3,
        'PIB_mean': [54252.16, 63138.21, 73968.61],
        'HDI': [0.928]*3,
        'Dépenses': [
            (33.024 / 18569.1) * 100,
            (40.503 / 23315.1) * 100,
            (43.342 / 28750.96) * 100
        ]
    })
    return pd.concat([df, us_data], ignore_index=True)
