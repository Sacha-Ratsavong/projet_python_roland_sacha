# scripts/pib_world.py

import pandas as pd


def process_pib_world():
    """
    Prépare les données de PIB par habitant comme déterminant
    de la performance olympique.

    Principe :
    - pour chaque édition des JO, on calcule le PIB moyen
      sur les 4 années précédentes
    - sortie au format long pour faciliter les fusions
    """

    # Lecture des données PIB par habitant (source mondiale)
    df_pib = pd.read_csv(
        "../data/raw/Data/GDP_hab.csv",
        sep=",",
        encoding="utf-8",
        skiprows=4
    )

    # Années des Jeux Olympiques retenues
    jo_years = [2012, 2016, 2021, 2024]

    # Calcul du PIB moyen sur les 4 années précédant chaque JO
    for jo in jo_years:
        start = jo - 4
        years = [str(y) for y in range(start, jo)]
        df_pib[f"PIB_mean_{jo}"] = df_pib[years].mean(axis=1)

    # Passage au format long : une ligne par (pays, année JO)
    df_long = pd.melt(
        df_pib,
        id_vars=["Country Name", "Country Code"],
        value_vars=[f"PIB_mean_{jo}" for jo in jo_years],
        var_name="JO Year",
        value_name="PIB_mean"
    )

    # Nettoyage de la colonne année JO (extraction de l'année)
    df_long["JO Year"] = df_long["JO Year"].str.extract(r"(\d+)$").astype(int)

    return df_long
