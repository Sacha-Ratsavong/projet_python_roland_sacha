# scripts/idh.py

import pandas as pd


def process_idh():
    """
    Prépare les données d’Indice de Développement Humain (IDH)
    pour l’analyse des déterminants de la réussite olympique.

    Principe :
    - les valeurs d’IDH ne sont disponibles que pour certaines années
    - chaque édition des JO est associée à une année d’IDH proxy
    - la sortie est mise au format long pour faciliter les fusions
    """

    # Lecture du fichier IDH brut (format Excel)
    df_IDH = pd.read_excel(
        "../data/raw/IDH 1990_2023.xlsx",
        skiprows=4,
        engine="openpyxl"
    )

    # Suppression des colonnes vides / parasites dues à la mise en page Excel
    cols_to_drop = [
        "Unnamed: 3", "Unnamed: 5", "Unnamed: 7", "Unnamed: 9",
        "Unnamed: 11", "Unnamed: 13", "Unnamed: 15", "Unnamed: 17",
        "Unnamed: 21", "Unnamed: 23", "Unnamed: 25"
    ]
    df_IDH = df_IDH.drop(columns=cols_to_drop)

    # Années pour lesquelles l'IDH est disponible dans le fichier
    idh_years = [1990, 2000, 2010, 2015, 2020, 2021, 2022, 2023]

    # Années des Jeux Olympiques et correspondance avec l'année d'IDH utilisée
    idh_for_jo = {
        1988: 1990, 1992: 1990, 1996: 1990,
        2000: 2000, 2004: 2000, 2008: 2000,
        2012: 2010, 2016: 2015,
        2021: 2020, 2024: 2023
    }

    # Passage au format long : une ligne par pays et par année d'IDH
    df_idh_long = df_IDH.melt(
        id_vars="Country",
        value_vars=idh_years,
        var_name="Year_IDH",
        value_name="HDI"
    )

    # Association de chaque valeur d'IDH à l'année des JO correspondante
    df_idh_long["Year_JO"] = df_idh_long["Year_IDH"].map(
        {v: k for k, v in idh_for_jo.items()}
    )

    # Conversion explicite de l'année IDH
    df_idh_long["Year_IDH"] = df_idh_long["Year_IDH"].astype(int)

    # Renommage pour cohérence avec les autres datasets (Year = année JO)
    df_idh_long.rename(columns={"Year_JO": "Year"}, inplace=True)

    return df_idh_long
