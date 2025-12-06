import pandas as pd

data = "/Users/roland/Desktop/ENSAE 2A/Python data/projet_python_roland_sacha/data/raw/athlete_events.csv"
df_athlete = pd.read_csv(data)
df_athlete = df_athlete.dropna(subset = "Medal")
df_athlete


