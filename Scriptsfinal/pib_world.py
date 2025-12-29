'''Traitement du PIB/habitant'''
import pandas as pd

def process_pib_world():
    df_pib = pd.read_csv("../data/raw/Data/GDP_hab.csv", sep=",", encoding="utf-8", skiprows=4)
    
    #On garde les années de JO (NB: au départ nous étions partis pour traiter 2012 également)

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

    # On ajuste la colonne 'JO Year' pour ne garder que l'année
    df_long['JO Year'] = df_long['JO Year'].str.extract('(\d+)$').astype(int)
    
    return df_long
