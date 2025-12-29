# scripts/medals.py
import pandas as pd

def process_medals():
    df_athlete = pd.read_csv("../data/raw/athlete_events.csv")
    df_athlete = df_athlete.dropna(subset=["Medal"])
    df_filtre = df_athlete[df_athlete["Games"].str.contains("Summer", na=False)]

    df_medals = (
        df_filtre.drop_duplicates(subset=["Year", "Event", "Team", "Medal"])
        .groupby(["Year", "Team", "Medal"])
        .size()
        .reset_index(name="Count")
    )

    # Ajout données Paris 2024
    df_2024 = pd.read_csv("../data/raw/paris-2024-results-medals-oly-eng.csv",
                          sep=";", encoding="utf-8", on_bad_lines="skip")
    df_2024["Year"] = pd.to_datetime(df_2024["Medal_date"]).dt.year
    medal_counts_2024 = df_2024.groupby(['Year', 'Country', 'Medal_type']).size().reset_index(name='Count')
    medal_counts_2024 = medal_counts_2024.rename(columns={"Medal_type": "Medal", "Country": "Team"})

    df_jeux = pd.concat([df_medals, medal_counts_2024], ignore_index=True)

    # Tokyo 2021
    df_tokyo = pd.read_csv("../data/raw/Tokyo Olympics  2021 dataset.csv", sep=",", encoding="utf-8", on_bad_lines="skip")
    df_tokyo = df_tokyo.rename(columns={"Gold Medal": "Gold", "Silver Medal": "Silver", "Bronze Medal": "Bronze", "Team/NOC": "Team"})
    df_tokyo["Year"] = 2021
    df_tokyo = df_tokyo.drop(["Total", "Rank by Total", "Rank", "NOCCode"], axis=1)
    df_tokyo["Team"] = df_tokyo["Team"].replace("United States of America", "United States")
    df_long = df_tokyo.melt(id_vars=["Team","Year"], value_vars=["Gold","Silver","Bronze"], var_name="Medal", value_name="Count")

    df_all_games = pd.concat([df_jeux, df_long], ignore_index=True)
    df_all_games["Medal"] = df_all_games["Medal"].str.replace("Medal", "", case=False).str.strip().str.capitalize()
    df_all_games = df_all_games.sort_values("Year")

    coef = {"Gold":5, "Silver":2, "Bronze":1}
    df_all_games["Score"] = df_all_games["Medal"].map(coef) * df_all_games["Count"]
    df_score = df_all_games.groupby(["Year","Team"], as_index=False)["Score"].sum()

    
    return df_all_games, df_score, df_athlete
