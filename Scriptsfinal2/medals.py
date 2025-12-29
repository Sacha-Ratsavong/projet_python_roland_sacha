# scripts/medals.py

import pandas as pd


def process_medals():
    """
    Construit deux tables à partir des médailles olympiques (JO d'été uniquement) :

    - df_all_games : données au format long (Year, Team, Medal, Count) pour toutes les éditions couvertes
    - df_score : score agrégé par pays et par année (pondération or/argent/bronze)

    Objectif : produire une mesure de "réussite olympique" exploitable ensuite
    pour étudier ses déterminants (PIB, IDH, dépenses sportives, etc.).
    """

    # --- Base historique : athlete_events.csv (médailles uniquement, JO d'été uniquement) ---
    df_athlete = pd.read_csv("../data/raw/athlete_events.csv")

    # On ne garde que les lignes correspondant à une médaille
    df_athlete = df_athlete.dropna(subset=["Medal"])

    # Filtre JO d'été
    df_filtre = df_athlete[df_athlete["Games"].str.contains("Summer", na=False)]

    # Comptage des médailles par (année, pays, type de médaille)
    # drop_duplicates évite de compter plusieurs fois une même médaille dans un event
    df_medals = (
        df_filtre.drop_duplicates(subset=["Year", "Event", "Team", "Medal"])
        .groupby(["Year", "Team", "Medal"])
        .size()
        .reset_index(name="Count")
    )

    # --- Ajout Paris 2024 (source séparée) ---
    df_2024 = pd.read_csv(
        "../data/raw/paris-2024-results-medals-oly-eng.csv",
        sep=";",
        encoding="utf-8",
        on_bad_lines="skip"
    )

    # Extraction de l'année à partir de la date de médaille
    df_2024["Year"] = pd.to_datetime(df_2024["Medal_date"]).dt.year

    # Comptage par pays et type de médaille, puis harmonisation des noms de colonnes
    medal_counts_2024 = (
        df_2024.groupby(["Year", "Country", "Medal_type"])
        .size()
        .reset_index(name="Count")
        .rename(columns={"Medal_type": "Medal", "Country": "Team"})
    )

    # Fusion base historique + Paris 2024
    df_jeux = pd.concat([df_medals, medal_counts_2024], ignore_index=True)

    # --- Ajout Tokyo 2021 (source séparée, format "wide") ---
    df_tokyo = pd.read_csv(
        "../data/raw/Tokyo Olympics  2021 dataset.csv",
        sep=",",
        encoding="utf-8",
        on_bad_lines="skip"
    )

    # Harmonisation des noms de colonnes avec les autres sources
    df_tokyo = df_tokyo.rename(columns={
        "Gold Medal": "Gold",
        "Silver Medal": "Silver",
        "Bronze Medal": "Bronze",
        "Team/NOC": "Team"
    })

    # Cette table ne contient pas l'année : on la fixe à 2021
    df_tokyo["Year"] = 2021

    # Suppression de colonnes non utiles pour le comptage des médailles
    df_tokyo = df_tokyo.drop(["Total", "Rank by Total", "Rank", "NOCCode"], axis=1)

    # Correction de libellé pour cohérence avec les autres sources
    df_tokyo["Team"] = df_tokyo["Team"].replace("United States of America", "United States")

    # Passage au format long : une ligne par (pays, année, type de médaille)
    df_long = df_tokyo.melt(
        id_vars=["Team", "Year"],
        value_vars=["Gold", "Silver", "Bronze"],
        var_name="Medal",
        value_name="Count"
    )

    # --- Dataset final toutes éditions ---
    df_all_games = pd.concat([df_jeux, df_long], ignore_index=True)

    # Nettoyage des libellés de médailles (uniformisation)
    df_all_games["Medal"] = (
        df_all_games["Medal"]
        .str.replace("Medal", "", case=False)
        .str.strip()
        .str.capitalize()
    )

    # Tri chronologique
    df_all_games = df_all_games.sort_values("Year")

    # --- Construction d'un score de performance olympique (pondération) ---
    coef = {"Gold": 5, "Silver": 2, "Bronze": 1}
    df_all_games["Score"] = df_all_games["Medal"].map(coef) * df_all_games["Count"]

    # Agrégation du score par (année, pays)
    df_score = df_all_games.groupby(["Year", "Team"], as_index=False)["Score"].sum()

    return df_all_games, df_score
