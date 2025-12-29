# scripts/pib_eu.py

import pandas as pd
import re
import sys


def process_pib_eu():
    # Lecture brute sans en-tête : permet de détecter la ligne qui contient les années
    df_raw_pib = pd.read_excel("../data/raw/PIB_EU.xlsx", header=None, engine="openpyxl")

    # Compte le nombre d'occurrences d'années (20xx) dans une ligne
    def count_years(row):
        return sum(bool(re.search(r"\b20\d{2}\b", str(x))) for x in row.values)

    # Détection de la ligne d'en-tête : celle qui contient le plus d'années
    year_counts = df_raw_pib.apply(count_years, axis=1)
    header_idx = int(year_counts.idxmax())

    if year_counts.max() >= 2:
        # Cas où on identifie clairement une ligne d'en-tête
        header_row = df_raw_pib.iloc[header_idx].astype(str).str.strip()
        df_PIB_total = df_raw_pib.iloc[header_idx + 1:].copy()
        df_PIB_total.columns = header_row

        # Nettoyage des noms de colonnes : si une année est présente dans le nom, on ne garde que l'année
        new_cols = []
        for c in df_PIB_total.columns:
            m = re.search(r"(20\d{2})", str(c))
            new_cols,append(m.group(1) if m else str(c).strip())
        df_PIB_total.columns = new_cols

    else:
        # Cas de secours : pas d'en-tête détectable, on lit l'Excel normalement
        df_PIB_total = pd.read_excel("../data/raw/PIB_EU.xlsx", engine="openpyxl")

        # Même nettoyage des noms de colonnes pour extraire les années si elles apparaissent dans le texte
        new_cols = []
        for c in df_PIB_total.columns:
            m = re.search(r"(20\d{2})", str(c))
            new_cols.append(m.group(1) if m else str(c).strip())
        df_PIB_total.columns = new_cols

    # Identification des colonnes années (format "20xx")
    year_cols = [c for c in df_PIB_total.columns if re.fullmatch(r"20\d{2}", str(c))]

    # Conversion des colonnes années en numérique (valeurs non convertibles -> NaN)
    for yc in year_cols:
        df_PIB_total[yc] = pd.to_numeric(df_PIB_total[yc], errors="coerce")

    # Tri chronologique des colonnes années
    year_cols_sorted = sorted(year_cols, key=lambda x: int(x))

    # Réorganisation des colonnes : d'abord les colonnes non-années, puis les années triées
    non_year_cols = [c for c in df_PIB_total.columns if c not in year_cols_sorted]
    df_PIB_total = df_PIB_total[non_year_cols + year_cols_sorted]

    # Pays européens sélectionnés (filtre sur la première colonne supposée être le pays)
    selected_countries = [
        "Autriche", "Belgique", "Espagne", "Finlande", "Estonie", "France",
        "Hongrie", "Irlande", "Italie", "Lituanie", "Norvège", "Pologne",
        "Roumanie", "Suède"
    ]
    df_PIB_total = df_PIB_total[df_PIB_total.iloc[:, 0].isin(selected_countries)]

    # Ajout d'un code pays (utile pour joins ou contrôles)
    country_code_mapping = {
        "Autriche": "AUT", "Belgique": "BEL", "Espagne": "ESP", "Finlande": "FIN",
        "Estonie": "EST", "France": "FRA", "Hongrie": "HUN", "Irlande": "IRL",
        "Italie": "ITA", "Lituanie": "LTU", "Norvège": "NOR", "Pologne": "POL",
        "Roumanie": "ROU", "Suède": "SWE"
    }
    df_PIB_total["Country Code"] = df_PIB_total.iloc[:, 0].map(country_code_mapping)

    # Traduction des pays en anglais pour cohérence avec les autres datasets (Team en anglais)
    country_mapping_fr_to_en = {
        "Autriche": "Austria", "Belgique": "Belgium", "Espagne": "Spain", "Finlande": "Finland",
        "Estonie": "Estonia", "France": "France", "Hongrie": "Hungary", "Irlande": "Ireland",
        "Italie": "Italy", "Lituanie": "Lithuania", "Norvège": "Norway", "Pologne": "Poland",
        "Roumanie": "Romania", "Suède": "Sweden"
    }
    df_PIB_total[df_PIB_total.columns[0]] = (
        df_PIB_total[df_PIB_total.columns[0]]
        .map(country_mapping_fr_to_en)
        .fillna(df_PIB_total[df_PIB_total.columns[0]])
    )

    # Sélection des années correspondant aux JO retenus dans le projet
    selected_years = ["2016", "2021", "2024"]
    cols_to_keep = [df_PIB_total.columns[0], "Country Code"] + selected_years
    df_PIB_total = df_PIB_total[cols_to_keep]

    # Passage au format long pour faciliter les merges : une ligne par (pays, année JO)
    df_PIB_long = pd.melt(
        df_PIB_total,
        id_vars=[df_PIB_total.columns[0], "Country Code"],
        value_vars=selected_years,
        var_name="Year",
        value_name="PIB"
    )
    df_PIB_long.rename(columns={df_PIB_total.columns[0]: "Team"}, inplace=True)

    return df_PIB_long
