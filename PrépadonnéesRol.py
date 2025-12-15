import pandas as pd

#On s'occupe de la partie médailles en premier (la + longue)
data = "data/raw/athlete_events.csv"
df_athlete = pd.read_csv(data)
#On enlève les athlètes sans médailles
df_athlete = df_athlete.dropna(subset = "Medal")

df_filtre = df_athlete[df_athlete["Games"].str.contains("Summer", na=False)]


#On a le tableau des médailles / pays / édition
df_medals = (
    df_filtre
    .drop_duplicates(subset=["Year", "Event", "Team", "Medal"])
    .groupby(["Year", "Team", "Medal"])
    .size()
    .reset_index(name="Count")
)




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


df_all_games["Medal"] = df_all_games["Medal"].str.replace("Medal", "", case = False)
df_all_games["Medal"] = df_all_games["Medal"].str.strip().str.capitalize()


#df_all_games.to_csv("data_clean/df_all_games.csv", index=False)

#Création d'un score associé à chaque perf d'un pays à une édition
df_all_games = df_all_games.sort_values(by="Year")


coef = {"Gold": 5, "Silver": 2, "Bronze": 1}
df_all_games["Score"] = df_all_games["Medal"].map(coef) * df_all_games["Count"]

#  On groupe par Year et Team et on somme les scores
df_score = df_all_games.groupby(["Year", "Team"], as_index=False)["Score"].sum()

df_score.to_csv('data_clean/df_score.csv', index = False)





import pandas as pd
import matplotlib.pyplot as plt

# Somme des médailles par pays
top_countries = df_all_games.groupby('Team')['Count'].sum().sort_values(ascending=False).head(5).index

# Filtre du DataFrame pour garder que ces pays
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










import pandas as pd
#PIB/hab et revenus mondiaux
df_pib = pd.read_csv(
    "data/raw/Data/GDP_hab.csv",
    sep=",",
    encoding="utf-8",
    skiprows=4   # Sp"écificité des fichiers World bank apparemment
)

df_pib.head()
df_pib

jo_years = [2012, 2016, 2020, 2024]
for jo in jo_years:
    start = jo - 4
    years = [str(y) for y in range(start, jo)]
    df_pib[f'PIB_mean_{jo}'] = df_pib[years].mean(axis=1)

df_long = pd.melt(
    df_pib,
    id_vars=['Country Name', 'Country Code'],
    value_vars=[f'PIB_mean_{jo}' for jo in jo_years],
    var_name='JO Year',
    value_name='PIB_mean'
)

# Ajuster la colonne 'JO Year' pour ne garder que l'année
df_long['JO Year'] = df_long['JO Year'].str.extract('(\d+)$').astype(int)


#df_long.to_csv("data_clean/df_PIB_hab.csv", index=False)



import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import make_interp_spline

countries = ["Chine", "Japon", "France", "Allemagne",
             "Brésil", "Australie", "Canada", "Afrique du Sud", "Fédération de Russie"]

df_plot = df_long[df_long['Country Name'].isin(countries)]

plt.figure(figsize=(12,6))

for country in countries:
    df_country = df_plot[df_plot['Country Name'] == country].sort_values('JO Year')
    
    x = df_country['JO Year'].values
    y = df_country['PIB_mean'].values
    
    # Ligne lissée avec label pour la légende
    x_smooth = np.linspace(x.min(), x.max(), 200)
    spline = make_interp_spline(x, y, k=2)
    y_smooth = spline(x_smooth)
    
    line, = plt.plot(x_smooth, y_smooth, label=country)  # label ici
    plt.scatter(x, y, s=50, color=line.get_color())       # points aux mêmes couleurs

plt.title('Évolution du PIB/hab moyen des pays aux éditions des JO')
plt.ylabel('PIB moyen (USD)')
plt.xlabel('Année des JO')
plt.xticks(jo_years)
plt.legend(title='Pays', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
#plt.show()












import pandas as pd
import numpy as np
#IDH

df_IDH = pd.read_excel("data/raw/IDH 1990_2023.xlsx", skiprows=4, engine="openpyxl")
print(df_IDH.columns)
cols_to_drop = [
     'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9',
    'Unnamed: 11', 'Unnamed: 13', 'Unnamed: 15', 'Unnamed: 17',
    'Unnamed: 21', 'Unnamed: 23', 'Unnamed: 25'
]

# Supprimer ces colonnes
df_IDH = df_IDH.drop(columns=cols_to_drop)

# Vérification
print(df_IDH.columns.tolist())




#Une première figure assez modeste sur l'évolut° de l'IDH
#import matplotlib.pyplot as plt

# Exemples de pays
#countries = ["France", "United States", "India", "Switzerland", "Norway", "China", "Bresil"]

# Colonnes avec les années ou périodes
#cols_time = [1990, 2000, 2010, 2020, 2023]  
# Filtrer les données
#df_plot = df_IDH[df_IDH['Country'].isin(countries)][['Country'] + cols_time]

#df_long = df_plot.melt(id_vars='Country', value_vars=cols_time,
                       #var_name='Period', value_name='HDI')

#plt.figure(figsize=(10,6))

#for country in countries:
    #data = df_long[df_long['Country'] == country]
    #plt.plot(data['Period'], data['HDI'], marker='o', label=country)

#plt.title("Évolution de l'IDH au cours du temps")
#plt.xlabel("Période")
#plt.ylabel("IDH")
#plt.ylim(0, 1)
#plt.legend()
#plt.grid(True)
#plt.show()










# Colonnes IDH disponibles
idh_years = [1990, 2000, 2010, 2015, 2020, 2021, 2022, 2023]

# Années JO
jo_years = [1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024]

# Mapping : JO_year → Année de l'IDH la plus proche (un peu arbitraire sur les bords mais on s'en contentera)
idh_for_jo = {
    1988: 1990, 1992: 1990, 1996: 1990,
    2000: 2000,
    2004: 2010, 2008: 2010,
    2012: 2015, 2016: 2015,
    2020: 2020, 2024: 2023
}

# On crée un df long (plus pratique pour la fusion qu'on va faire après avec médailles, PIB, etc.)
df_idh_long = df_IDH.melt(id_vars='Country', value_vars=idh_years,
                          var_name='Year_IDH', value_name='HDI')

# Transfo années IDH en années JO correspondantes
df_idh_long['Year_JO'] = df_idh_long['Year_IDH'].map({v:k for k,v in idh_for_jo.items()})

df_idh_long['Year_IDH'] = df_idh_long['Year_IDH'].astype(int)
df_idh_long.rename(columns={'Year_JO': 'Year'}, inplace=True)
df_idh_long.head(10)
#Sauvegarde de ce superbe dataframe de l'IDH calqué sur les éditions de JO
df_idh_long.to_csv("data_clean/df_IDH.csv", index = False)


