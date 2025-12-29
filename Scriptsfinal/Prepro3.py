import pandas as pd

EXCLUDED_COUNTRIES = ["Cyprus", "Croatia", "Czechia", "Slovakia"]

def prepare_data_volume(
    path_main,
    path_pib):
    df = pd.read_csv(path_main)

    df = df[~df["Country"].isin(EXCLUDED_COUNTRIES)]

    df_pib = pd.read_csv(path_pib)
    df = pd.merge(df, df_pib, on=["Year", "Country Code"], how="left")

    df["Dépenses_volume"] = df["Dépenses"] * df["PIB"] / 100

    df = df.dropna(subset=[
        "PIB",
        "Score",
        "Dépenses_volume",
        "HDI",
        "PIB_mean"])

    return df








