
import pandas as pd
import re
import sys



def process_pib_eu():
    df_raw_pib = pd.read_excel("../data/raw/PIB_EU.xlsx", header=None, engine="openpyxl")
    def count_years(row):
        return sum(bool(re.search(r"\b20\d{2}\b", str(x))) for x in row.values)
    year_counts = df_raw_pib.apply(count_years, axis=1)
    header_idx = int(year_counts.idxmax())
    if year_counts.max() >= 2:
        header_row = df_raw_pib.iloc[header_idx].astype(str).str.strip()
        df_PIB_total = df_raw_pib.iloc[header_idx+1:].copy()
        df_PIB_total.columns = header_row
    # Nettoyer les noms de colonnes pour garder juste l'année si présente
        new_cols = []
        for c in df_PIB_total.columns:
            m = re.search(r"(20\d{2})", str(c))
            if m:
                new_cols.append(m.group(1))
            else:
                new_cols.append(str(c).strip())
        df_PIB_total.columns = new_cols
    else:
        # Pas d'en-tête évident, on lit avec header=0
        df_PIB_total = pd.read_excel("../data/raw/PIB_EU.xlsx", engine="openpyxl")
    # tenter d'extraire les années des noms de colonnes
        new_cols = []
        for c in df_PIB_total.columns:
            m = re.search(r"(20\d{2})", str(c))
            if m:
                new_cols.append(m.group(1))
            else:
                new_cols.append(str(c).strip())
        df_PIB_total.columns = new_cols
# Assurer que les colonnes années sont au format int et ordonnées
    year_cols = [c for c in df_PIB_total.columns if re.fullmatch(r"20\d{2}", str(c))]
# Convertir types et trier
    for yc in year_cols:
        df_PIB_total[yc] = pd.to_numeric(df_PIB_total[yc], errors='coerce')
    year_cols_sorted = sorted(year_cols, key=lambda x: int(x))
# Réorganiser les colonnes en mettant d'abord les éventuelles colonnes non-années
    non_year_cols = [c for c in df_PIB_total.columns if c not in year_cols_sorted]
    df_PIB_total = df_PIB_total[non_year_cols + year_cols_sorted]


# Pays européens sélectionnés
    selected_countries = [
    "Autriche", "Belgique", "Espagne", "Finlande", "Estonie", "France",
    "Hongrie", "Irlande", "Italie", "Lituanie", "Norvège", "Pologne",
    "Roumanie", "Suède"
    ]
    df_PIB_total = df_PIB_total[df_PIB_total.iloc[:, 0].isin(selected_countries)]  # Assumer que la première colonne est le pays

# Country Code
    country_code_mapping = {
    "Autriche": "AUT", "Belgique": "BEL", "Espagne": "ESP", "Finlande": "FIN",
    "Estonie": "EST", "France": "FRA", "Hongrie": "HUN", "Irlande": "IRL",
    "Italie": "ITA", "Lituanie": "LTU", "Norvège": "NOR", "Pologne": "POL",
    "Roumanie": "ROU", "Suède": "SWE"
    }
    df_PIB_total['Country Code'] = df_PIB_total.iloc[:, 0].map(country_code_mapping)

# Traduire les noms de pays en anglais (NB : On a un dictionnaire immense pour ça mais il est situé après dans le code donc on le refait ici
# ce qui est un peu dommage mais tant pis)
    country_mapping_fr_to_en = {
    "Autriche": "Austria", "Belgique": "Belgium", "Espagne": "Spain", "Finlande": "Finland",
    "Estonie": "Estonia", "France": "France", "Hongrie": "Hungary", "Irlande": "Ireland",
    "Italie": "Italy", "Lituanie": "Lithuania", "Norvège": "Norway", "Pologne": "Poland",
    "Roumanie": "Romania", "Suède": "Sweden"
    }
    df_PIB_total[df_PIB_total.columns[0]] = df_PIB_total[df_PIB_total.columns[0]].map(country_mapping_fr_to_en).fillna(df_PIB_total[df_PIB_total.columns[0]])

#Seulement les années de JO
    selected_years = ['2016', '2021', '2024']
    cols_to_keep = [df_PIB_total.columns[0], 'Country Code'] + selected_years
    df_PIB_total = df_PIB_total[cols_to_keep]

# On le rallonge pour matcher avec le reste des données
    df_PIB_long = pd.melt(df_PIB_total, id_vars=[df_PIB_total.columns[0], 'Country Code'], value_vars=selected_years, var_name='Year', value_name='PIB')
    df_PIB_long.rename(columns={df_PIB_total.columns[0]: 'Team'}, inplace=True)

    #df_PIB_long.to_csv("../data_clean/PIB_EU_long.csv", index=False)
    return df_PIB_long
