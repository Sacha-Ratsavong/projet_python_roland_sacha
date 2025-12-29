
import pandas as pd

def merge_all(df_score, df_pib, df_idh, df_depenses):


    # ----------------------
    # 2️⃣ Mapping des noms de pays en anglais
    # ----------------------
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


    df_score = df_score.rename(columns={'Team': 'Country'})
    df_pib = df_pib.rename(columns={'Country Name': 'Country', 'JO Year': 'Year'})
    
    df_score['Country'] = df_score['Country'].replace(country_mapping_universel)
    df_pib['Country'] = df_pib['Country'].replace(country_mapping_universel)
    df_idh['Country'] = df_idh['Country'].replace(country_mapping_universel)

    # ----------------------
    # 3️⃣ Fusionner Score, PIB, IDH
    # ----------------------
    df_merged = pd.merge(df_score, df_pib, on=['Year', 'Country'], how='outer')
    df_merged = pd.merge(df_merged, df_idh, on=['Year', 'Country'], how='outer')
    df_merged = df_merged.drop(columns=['Year_IDH'], errors='ignore')
    df_merged = df_merged.dropna(subset=['Score', 'HDI', 'PIB_mean'])

    # ----------------------
    # 4️⃣ Filtrer pays européens + USA
    # ----------------------
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

    # ----------------------
    # 5️⃣ Ajouter les dépenses sportives
    # ----------------------
    
    df_depenses = df_depenses.rename(columns={
        'Entité géopolitique (déclarante)': 'Country',
        'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Dépenses'
    })
    dep_country_mapping = {
        "Allemagne": "Germany",
        "Autriche": "Austria",
        "Belgique": "Belgium",
        "Bulgarie": "Bulgaria",
        "Chypre": "Cyprus",
        "Croatie": "Croatia",
        "Danemark": "Denmark",
        "Espagne": "Spain",
        "Estonie": "Estonia",
        "Finlande": "Finland",
        "France": "France",
        "Grèce": "Greece",
        "Hongrie": "Hungary",
        "Irlande": "Ireland",
        "Islande": "Iceland",
        "Italie": "Italy",
        "Lettonie": "Latvia",
        "Lituanie": "Lithuania",
        "Luxembourg": "Luxembourg",
        "Malte": "Malta",
        "Norvège": "Norway",
        "Pays-Bas": "Netherlands",
        "Pologne": "Poland",
        "Portugal": "Portugal",
        "Roumanie": "Romania",
        "Slovaquie": "Slovakia",
        "Slovénie": "Slovenia",
        "Suisse": "Switzerland",
        "Suède": "Sweden",
        "Tchéquie": "Czech Republic"
    }
    df_depenses['Country'] = df_depenses['Country'].replace(dep_country_mapping)

    df_depenses['Year'] = df_depenses['Year'].astype(int)
    df_merged['Year'] = df_merged['Year'].astype(int)

    # Pour 2024, reprendre les valeurs 2023 si manquantes
    df_2024 = df_depenses[df_depenses["Year"] == 2023].copy()
    df_2024["Year"] = 2024
    df_depenses = pd.concat([df_depenses, df_2024], ignore_index=True)
    
    # Fusion finale
    df_merged_final = pd.merge(df_merged, df_depenses[['Year', 'Country', 'Dépenses']],
                               on=['Year', 'Country'], how='inner')
    df_merged_final = df_merged_final.drop_duplicates()
    return df_merged_final


    


