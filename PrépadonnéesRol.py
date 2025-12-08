import pandas as pd

#On s'occupe de la partie médailles en premier (la + longue)
data = "data/raw/athlete_events.csv"
df_athlete = pd.read_csv(data)
#On enlève les athlètes sans médailles
df_athlete = df_athlete.dropna(subset = "Medal")
df_filtre = df_athlete[df_athlete["Games"].str.contains("Summer", na=False)]


#On a le tableau des médailles / pays / édition
df_medals = medal_counts = df_filtre.groupby(['Year', 'Team', 'Medal']).size().reset_index(name='Count')




df_2024 = pd.read_csv("data/raw/paris-2024-results-medals-oly-eng.csv", sep = ";", encoding = "utf-8", on_bad_lines = "skip")
df_2024["Year"] = pd.to_datetime(df_2024["Medal_date"]).dt.year
medal_counts_2024 = df_2024.groupby(['Year', 'Country', 'Medal_type']).size().reset_index(name='Count')
medal_counts_2024 = medal_counts_2024.rename(columns={"Medal_type": "Medal", "Country" : "Team"})

df_jeux = pd.concat([df_medals, medal_counts_2024], ignore_index= True)


df_tokyo = pd.read_csv("data/raw/Tokyo Olympics  2021 dataset.csv", sep = ",", encoding = "utf-8", on_bad_lines = "skip") 

df_tokyo = df_tokyo.rename(columns={"Gold Medal": "Gold", "Bronze Medal" : "Bronze", "Silver Medal" : "Silver", "Team/NOC" : "Team"})
df_tokyo["Year"] = 2021

df_tokyo = df_tokyo.drop(["Total", "Rank by Total", "Rank", "NOCCode"], axis=1)
df_tokyo["Team"] = df_tokyo["Team"].replace("United States of America", "United States")

df_long = df_tokyo.melt(
    id_vars=["Team", "Year"],      # colonnes qui restent fixes
    value_vars=["Gold", "Silver", "Bronze"],   # colonnes à transformer
    var_name="Medal",             # nom de la nouvelle colonne
    value_name="Count"                # nombre de médailles
)


#On a le df des médailles pr toutes les éditions c bon
df_all_games = pd.concat([df_jeux, df_long], ignore_index = True)
df_all_games = df_all_games.sort_values(by="Year")



#df_all_games.to_csv("data_clean/df_all_games.csv", index=False)


import pandas as pd
import matplotlib.pyplot as plt

# Somme des médailles par pays
top_countries = df_all_games.groupby('Team')['Count'].sum().sort_values(ascending=False).head(5).index

# Filtre du DataFrame pour ne garder que ces pays
df_top = df_all_games[df_all_games['Team'].isin(top_countries)]
df_top

df_agg = df_top.groupby(['Year', 'Team'])['Count'].sum().reset_index()
df_pivot = df_agg.pivot(index='Year', columns='Team', values='Count').fillna(0)

plt.figure(figsize=(15,8))

for country in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[country], marker='o', label=country)  # ajoute des points pour chaque JO

plt.title("Évolution des médailles des 5 pays les plus titrés aux JO")
plt.xlabel("Édition des JO")
plt.ylabel("Nombre de médailles")

# Mettre les années exactes comme ticks
plt.xticks(df_pivot.index, rotation=45)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
