import pandas as pd


# Pays exclus de l’analyse (données incomplètes ou incohérences)
EXCLUDED_COUNTRIES = ["Cyprus", "Croatia", "Czechia", "Slovakia"]


def prepare_data_volume(path_main, path_pib):
    """
    Prépare le dataset final pour l’analyse en volume des dépenses sportives.

    Principe :
    - fusion des données principales avec le PIB
    - conversion des dépenses en pourcentage du PIB
      en niveau absolu (dépenses × PIB)
    - nettoyage des observations incomplètes
    """

    # Chargement du dataset principal
    df = pd.read_csv(path_main)

    # Exclusion de certains pays
    df = df[~df["Country"].isin(EXCLUDED_COUNTRIES)]

    # Chargement et fusion des données de PIB
    df_pib = pd.read_csv(path_pib)
    df = pd.merge(df, df_pib, on=["Year", "Country Code"], how="left")

    # Calcul des dépenses sportives en volume
    df["Dépenses_volume"] = df["Dépenses"] * df["PIB"] / 100

    # Suppression des observations incomplètes sur les variables clés
    df = df.dropna(
        subset=[
            "PIB",
            "Score",
            "Dépenses_volume",
            "HDI",
            "PIB_mean",
        ]
    )

    return df