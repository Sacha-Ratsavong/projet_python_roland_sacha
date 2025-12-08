import pandas as pd

#On s'occupe de la partie médailles en premier (la + longue)
data = "W:/Bureau/Projet Python/Code/projet_python_roland_sacha/data/raw/athlete_events.csv"
df_athlete = pd.read_csv(data)
#On enlève les athlètes sans médailles
df_athlete = df_athlete.dropna(subset = "Medal")

#On a le tableau des médailles / pays / édition
df_medals = medal_counts = df_athlete.groupby(['Year', 'Team', 'Medal']).size().reset_index(name='Count')




df_2024 = pd.read_csv("data/raw/paris-2024-results-medals-oly-eng.csv", sep = ";", encoding = "utf-8", on_bad_lines = "skip")
df_2024["Year"] = pd.to_datetime(df_2024["Medal_date"]).dt.year
medal_counts_2024 = df_2024.groupby(['Year', 'Country', 'Medal_type']).size().reset_index(name='Count')
medal_counts_2024 = medal_counts_2024.rename(columns={"Medal_type": "Medal", "Country" : "Team"})

df_jeux = pd.concat([df_medals, medal_counts_2024], ignore_index= True)
df_jeux

df_tokyo = pd.read_csv("data/raw/Tokyo Olympics  2021 dataset.csv", sep = ",", encoding = "utf-8", on_bad_lines = "skip") 
print(df_tokyo.columns.tolist())
df_tokyo = df_tokyo.rename(columns={"Gold Medal": "Gold", "Bronze Medal" : "Bronze", "Silver Medal" : "Silver", "Team/NOC" : "Team"})
df_tokyo["Year"] = 2021
df_tokyo = df_tokyo.drop(["Total", "Rank by Total", "Rank", "NOCCode"], axis=1)

df_long = df_tokyo.melt(
    id_vars=["Team", "Year"],      # colonnes qui restent fixes
    value_vars=["Gold", "Silver", "Bronze"],   # colonnes à transformer
    var_name="Medal",             # nom de la nouvelle colonne
    value_name="Count"                # nombre de médailles
)
df_long

#On a le df des médailles pr toutes les éditions c bon
df_all_games = pd.concat([df_jeux, df_long], ignore_index = True)
df_all_games = df_all_games.sort_values(by="Year")
df_all_games






