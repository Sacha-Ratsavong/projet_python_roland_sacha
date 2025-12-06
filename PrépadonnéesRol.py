import pandas as pd

data = "/Users/roland/Desktop/ENSAE 2A/Python data/projet_python_roland_sacha/data/raw/athlete_events.csv"
df_athlete = pd.read_csv(data)
#On enlève les athlètes sans médailles
df_athlete = df_athlete.dropna(subset = "Medal")

df_medals = medal_counts = df_athlete.groupby(['Year', 'Team', 'Medal']).size().reset_index(name='Count')
df_medals



