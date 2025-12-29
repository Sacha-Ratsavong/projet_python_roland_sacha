import pandas as pd

EXCLUDED_COUNTRIES = ["Cyprus", "Croatia", "Czechia", "Slovakia"]

def prepare_data_volume(
    df1,
    df2):
    df = df1

    df = df[~df["Country"].isin(EXCLUDED_COUNTRIES)]

    df_pib = df2
    df['Year'] = df['Year'].astype(int)
    df_pib['Year'] = df_pib['Year'].astype(int)
    df['Country Code'] = df['Country Code'].astype(str)
    df_pib['Country Code'] = df_pib['Country Code'].astype(str)
    df = pd.merge(df, df_pib, on=["Year", "Country Code"], how="left")

    df["Dépenses_volume"] = df["Dépenses"] * df["PIB"] / 100

    df = df.dropna(subset=[
        "PIB",
        "Score",
        "Dépenses_volume",
        "HDI",
        "PIB_mean"])

    return df








