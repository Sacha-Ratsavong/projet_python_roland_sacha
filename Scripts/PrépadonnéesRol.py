#%%
import pandas as pd

#On s'occupe de la partie médailles en premier (la + longue)
data = "../data/raw/athlete_events.csv"
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




df_2024 = pd.read_csv("../data/raw/paris-2024-results-medals-oly-eng.csv", sep = ";", encoding = "utf-8", on_bad_lines = "skip")
df_2024["Year"] = pd.to_datetime(df_2024["Medal_date"]).dt.year
medal_counts_2024 = df_2024.groupby(['Year', 'Country', 'Medal_type']).size().reset_index(name='Count')
medal_counts_2024 = medal_counts_2024.rename(columns={"Medal_type": "Medal", "Country" : "Team"})

df_jeux = pd.concat([df_medals, medal_counts_2024], ignore_index= True)


df_tokyo = pd.read_csv("../data/raw/Tokyo Olympics  2021 dataset.csv", sep = ",", encoding = "utf-8", on_bad_lines = "skip") 

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

df_score.to_csv('../data_clean/df_score.csv', index = False)





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


#%%
import pandas as pd
#Maintenant, traitons les données des variables de contrôle (PIB, IDH, etc.) : 
#Commençons par avoir les PIB des pays de l'UE pour la période 2016 à 2024 
import re

# Lecture brute du fichier Excel et détection automatique de la ligne d'en-têtes (années)
df_raw_pib = pd.read_excel("../data/raw/PIB_EU.xlsx", header=None, engine="openpyxl")
# Chercher la ligne qui contient le plus d'années au format 20XX
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

# Et on le sauvegarde
df_PIB_long.to_csv("data_clean/PIB_EU_long.csv", index=False, encoding='utf-8')






#%%
import pandas as pd
#PIB/hab et revenus mondiaux
df_pib = pd.read_csv(
    "../data/raw/Data/GDP_hab.csv",
    sep=",",
    encoding="utf-8",
    skiprows=4   # Sp"écificité des fichiers World bank apparemment
)

df_pib.head()
df_pib

jo_years = [2012, 2016, 2021, 2024]
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

df_long.to_csv("../data_clean/df_PIB_hab.csv", index=False)



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









#IDH : Traitement 


import pandas as pd
import numpy as np


df_IDH = pd.read_excel("../data/raw/IDH 1990_2023.xlsx", skiprows=4, engine="openpyxl")
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
jo_years = [1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2021, 2024]

# Mapping : JO_year → Année de l'IDH la plus récente disponible avant ou à l'année JO
idh_for_jo = {
    1988: 1990,  # Pas de donnée avant, on utilise 1990
    1992: 1990,
    1996: 1990,
    2000: 2000,
    2004: 2000,  # 2000 est la plus récente avant 2004
    2008: 2000,  # 2000 est la plus récente avant 2008
    2012: 2010,  # 2010 est la plus récente avant 2012
    2016: 2015,  # 2015 est la plus récente avant 2016
    2021: 2020,  # 2020 est la plus récente avant 2021
    2024: 2023
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
df_idh_long.to_csv("../data_clean/df_IDH.csv", index = False)




import pandas as pd
# Fusion des dataframes nettoyés
df_score = pd.read_csv('../data_clean/df_score.csv')
df_pib = pd.read_csv('../data_clean/df_PIB_hab.csv')
df_idh = pd.read_csv('../data_clean/df_IDH.csv')

# Mapping pour traduire les noms de pays français en anglais
country_mapping_universel = {
    "Chine": "China",
    "États-Unis": "United States",
    "Japon": "Japan",
    "Allemagne": "Germany",
    "Brésil": "Brazil",
    "Australie": "Australia",
    "Canada": "Canada",
    "Afrique du Sud": "South Africa",
    "Fédération de Russie": "Russian Federation",
    "France": "France",
    "Royaume-Uni": "Great Britain",
    "Italie": "Italy",
    "Espagne": "Spain",
    "Pays-Bas": "Netherlands",
    "Belgique": "Belgium",
    "Suisse": "Switzerland",
    "Suède": "Sweden",
    "Norvège": "Norway",
    "Danemark": "Denmark",
    "Finlande": "Finland",
    "Autriche": "Austria",
    "Portugal": "Portugal",
    "Grèce": "Greece",
    "Irlande": "Ireland",
    "Islande": "Iceland",
    "Luxembourg": "Luxembourg",
    "Albanie": "Albania",
    "Andorre": "Andorra",
    "Argentine": "Argentina",
    "Bahamas": "Bahamas",
    "Bolivie": "Bolivia",
    "Chili": "Chile",
    "Colombie": "Colombia",
    "Costa Rica": "Costa Rica",
    "Cuba": "Cuba",
    "République dominicaine": "Dominican Republic",
    "Équateur": "Ecuador",
    "El Salvador": "El Salvador",
    "Guatemala": "Guatemala",
    "Haïti": "Haiti",
    "Honduras": "Honduras",
    "Jamaïque": "Jamaica",
    "Mexique": "Mexico",
    "Nicaragua": "Nicaragua",
    "Panama": "Panama",
    "Paraguay": "Paraguay",
    "Pérou": "Peru",
    "Suriname": "Suriname",
    "Trinité-et-Tobago": "Trinidad and Tobago",
    "Uruguay": "Uruguay",
    "Venezuela": "Venezuela",
    "Bulgarie": "Bulgaria",
    "Bahreïn": "Bahrain",
    "Bosnie-Herzégovine": "Bosnia and Herzegovina",
    "Bélarus": "Belarus",
    "Bermudes": "Bermuda",
    "Barbade": "Barbados",
    "Brunéi Darussalam": "Brunei",
    "Bhoutan": "Bhutan",
    "Botswana": "Botswana",
    "République centrafricaine": "Central African Republic",
    "Côte d'Ivoire": "Ivory Coast",
    "Cameroun": "Cameroon",
    "Congo, République démocratique du": "Democratic Republic of the Congo",
    "Congo, République du": "Republic of the Congo",
    "Comores": "Comoros",
    "Cabo Verde": "Cape Verde",
    "République tchèque": "Czech Republic",
    "Égypte": "Egypt",
    "Émirats arabes unis": "United Arab Emirates",
    "Équateur": "Ecuador",
    "Estonie": "Estonia",
    "Éthiopie": "Ethiopia",
    "Fidji": "Fiji",
    "Gabon": "Gabon",
    "Gambie": "Gambia",
    "Géorgie": "Georgia",
    "Ghana": "Ghana",
    "Guinée": "Guinea",
    "Guinée-Bissau": "Guinea-Bissau",
    "Guinée équatoriale": "Equatorial Guinea",
    "Guyana": "Guyana",
    "Haïti": "Haiti",
    "Honduras": "Honduras",
    "Hongrie": "Hungary",
    "Îles Marshall": "Marshall Islands",
    "Îles Salomon": "Solomon Islands",
    "Inde": "India",
    "Indonésie": "Indonesia",
    "Iran": "Iran",
    "Iraq": "Iraq",
    "Israël": "Israel",
    "Jordanie": "Jordan",
    "Kazakhstan": "Kazakhstan",
    "Kenya": "Kenya",
    "Kirghizistan": "Kyrgyzstan",
    "Kiribati": "Kiribati",
    "Koweït": "Kuwait",
    "Laos": "Laos",
    "Lesotho": "Lesotho",
    "Lettonie": "Latvia",
    "Liban": "Lebanon",
    "Libéria": "Liberia",
    "Libye": "Libya",
    "Lituanie": "Lithuania",
    "Luxembourg": "Luxembourg",
    "Macédoine du Nord": "North Macedonia",
    "Madagascar": "Madagascar",
    "Malaisie": "Malaysia",
    "Malawi": "Malawi",
    "Maldives": "Maldives",
    "Mali": "Mali",
    "Malte": "Malta",
    "Maroc": "Morocco",
    "Maurice": "Mauritius",
    "Mauritanie": "Mauritania",
    "Mayotte": "Mayotte",
    "Micronésie": "Micronesia",
    "Moldavie": "Moldova",
    "Mongolie": "Mongolia",
    "Mozambique": "Mozambique",
    "Myanmar": "Myanmar",
    "Namibie": "Namibia",
    "Nauru": "Nauru",
    "Népal": "Nepal",
    "Nicaragua": "Nicaragua",
    "Niger": "Niger",
    "Nigéria": "Nigeria",
    "Nioué": "Niue",
    "Norvège": "Norway",
    "Nouvelle-Calédonie": "New Caledonia",
    "Nouvelle-Zélande": "New Zealand",
    "Oman": "Oman",
    "Ouganda": "Uganda",
    "Ouzbékistan": "Uzbekistan",
    "Pakistan": "Pakistan",
    "Palaos": "Palau",
    "Panama": "Panama",
    "Papouasie-Nouvelle-Guinée": "Papua New Guinea",
    "Paraguay": "Paraguay",
    "Pays-Bas": "Netherlands",
    "Philippines": "Philippines",
    "Pologne": "Poland",
    "Polynésie française": "French Polynesia",
    "Portugal": "Portugal",
    "Qatar": "Qatar",
    "Roumanie": "Romania",
    "Royaume-Uni": "United Kingdom",
    "Rwanda": "Rwanda",
    "Sahara occidental": "Western Sahara",
    "Saint-Kitts-et-Nevis": "Saint Kitts and Nevis",
    "Saint-Marin": "San Marino",
    "Saint-Vincent-et-les-Grenadines": "Saint Vincent and the Grenadines",
    "Sainte-Lucie": "Saint Lucia",
    "Samoa": "Samoa",
    "Sao Tomé-et-Principe": "Sao Tome and Principe",
    "Sénégal": "Senegal",
    "Serbie": "Serbia",
    "Seychelles": "Seychelles",
    "Sierra Leone": "Sierra Leone",
    "Singapour": "Singapore",
    "Slovaquie": "Slovakia",
    "Slovénie": "Slovenia",
    "Somalie": "Somalia",
    "Soudan": "Sudan",
    "Soudan du Sud": "South Sudan",
    "Sri Lanka": "Sri Lanka",
    "Suède": "Sweden",
    "Suisse": "Switzerland",
    "Suriname": "Suriname",
    "Swaziland": "Eswatini",
    "Syrie": "Syria",
    "Tadjikistan": "Tajikistan",
    "Tanzanie": "Tanzania",
    "Tchad": "Chad",
    "Thaïlande": "Thailand",
    "Timor oriental": "Timor-Leste",
    "Togo": "Togo",
    "Tonga": "Tonga",
    "Trinité-et-Tobago": "Trinidad and Tobago",
    "Tunisie": "Tunisia",
    "Turkménistan": "Turkmenistan",
    "Turquie": "Turkey",
    "Tuvalu": "Tuvalu",
    "Ukraine": "Ukraine",
    "Uruguay": "Uruguay",
    "Vanuatu": "Vanuatu",
    "Venezuela": "Venezuela",
    "Viêt Nam": "Vietnam",
    "Yémen": "Yemen",
    "Zambie": "Zambia",
    "Zimbabwe": "Zimbabwe",
}



# Renommer les colonnes pour cohérence
df_score = df_score.rename(columns={'Team': 'Country'})
df_pib = df_pib.rename(columns={'Country Name': 'Country', 'JO Year': 'Year'})

# Appliquer le mapping
df_score['Country'] = df_score['Country'].replace(country_mapping_universel)
df_pib['Country'] = df_pib['Country'].replace(country_mapping_universel)
df_idh['Country'] = df_idh['Country'].replace(country_mapping_universel)

# Fusionner df_score et df_pib sur Year et Country
df_merged = pd.merge(df_score, df_pib, on=['Year', 'Country'], how='outer')

# Puis fusionner avec df_idh
df_merged = pd.merge(df_merged, df_idh, on=['Year', 'Country'], how='outer')

# Supprimer Year_IDH si présent
df_merged = df_merged.drop(columns=['Year_IDH'], errors='ignore')

# Garder seulement les lignes avec Score, HDI et PIB_mean non nuls
df_merged = df_merged.dropna(subset=['Score', 'HDI', 'PIB_mean'])

# Filtrer pour garder seulement les pays européens et les USA
european_countries = [
    "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", 
    "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", 
    "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", 
    "Hungary", "Iceland", "Ireland", "Italy", "Kazakhstan", "Kosovo", "Latvia", 
    "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", 
    "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", 
    "Romania", "Russian Federation", "San Marino", "Serbia", "Slovakia", "Slovenia", 
    "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom"
]

countries_to_keep = european_countries + ["United States"]

df_merged = df_merged[df_merged['Country'].isin(countries_to_keep)]

# Sauvegarder le dataframe fusionné filtré
#df_merged.to_csv('../data_clean/df_merged.csv', index=False)








import pandas as pd
df_merged = pd.read_csv('/Users/roland/Desktop/ENSAE 2A/Python data/projet_python_roland_sacha/data_clean/df_merged.csv')
df_merged['Year'] = df_merged['Year'].astype(int)
df_dépenses_UE = pd.read_csv("/Users/roland/Desktop/ENSAE 2A/Python data/projet_python_roland_sacha/data/raw/depenses_sports_UE.csv")

df_dépenses_UE = df_dépenses_UE.rename(columns = {"Entité géopolitique (déclarante)" : "Country", "TIME_PERIOD" : "Year"})

df_dépenses_UE['Country'] = df_dépenses_UE['Country'].replace(country_mapping_universel)
df_merged_final2 = pd.merge(df_dépenses_UE, df_merged, on = ['Year', 'Country'], how = "inner")
df_merged_final2










# Graphiques pour visualiser les relations pour chaque année JO
import matplotlib.pyplot as plt
import seaborn as sns

jo_years_plot = [2016, 2021, 2024]

for year in jo_years_plot:
    df_year = df_merged[df_merged['Year'] == year]
    
    # Table for HDI and Score
    print(f"\nTable for HDI and Score in {year}:")
    table = df_year[['Country', 'HDI', 'Score']].sort_values('HDI', ascending=False)
    print(table.to_string(index=False))
    
    # Scatter plot Score vs PIB_mean
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df_year, x='PIB_mean', y='Score')
    plt.title(f'Relation between Olympic Score and GDP per capita for {year}')
    plt.xlabel('GDP per capita (mean, USD)')
    plt.ylabel('Olympic Score')
    plt.grid(True)
    plt.show()




