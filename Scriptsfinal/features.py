import pandas as pd
import numpy as np
'''Permet d'ajouter le score précédent et la taille de la délégation pour régression longue'''


def add_previous_score(df_clean, df_score, n=3):
    """
    Ajoute la colonne 'score_précédent' : moyenne des n éditions précédentes (on dit 3 dans notre projet)
    """
    df_score = df_score.copy()
    #On convertit pour lier ensuite
    df_score['Year'] = df_score['Year'].astype(int)
    df_clean['Year'] = df_clean['Year'].astype(int)
    

    def prev_avg(country, year):
        prev = df_score[(df_score['Team'] == country) & (df_score['Year'] < year)]
        prev = prev.sort_values('Year', ascending=False).head(n)
        return prev['Score'].mean() if not prev.empty else np.nan

    df_clean['score_précédent'] = df_clean.apply(lambda r: prev_avg(r['Country'], r['Year']), axis=1)
    return df_clean


def add_delegation_size(df_clean, df_athletes, add_2021_2024=True):
    """
    Ajoute la colonne 'taille_délégation' en utilisant df_athletes, notre fichier d'origine
    """
    df_athletes = df_athletes.copy()
    df_athletes['Year'] = df_athletes['Year'].astype(int)

    delegation = (
        df_athletes.groupby(['Year', 'NOC'])['ID']
        .nunique()
        .reset_index()
        .rename(columns={'NOC': 'Country Code', 'ID': 'taille_délégation'})
    )
    #On peut décider d'inclure les délégations en 2021 et 2024 (ce qu'on fait dans le projet en général) ou non 
    if add_2021_2024:
        delegation_2021 = {'FRA': 398, 'GER': 425, 'ITA': 384, 'ESP': 321, 'NED': 278, 'POL': 210,
                           'SWE': 134, 'GRE': 83, 'AUT': 60, 'CRO': 59, 'SLO': 53, 'FIN': 45,
                           'BUL': 42, 'LTU': 42, 'SVK': 41, 'POR': 92, 'CZE': 115, 'BEL': 121,
                           'IRL': 116, 'DEN': 107, 'HUN': 166, 'ROU': 101, 'EST': 33, 'LAT': 33,
                           'LUX': 12, 'MLT': 6, 'CYP': 15, 'USA': 620}

        delegation_2024 = {'FRA': 571, 'GER': 427, 'ITA': 403, 'ESP': 383, 'NED': 275, 'POL': 210,
                           'SWE': 128, 'GRE': 101, 'AUT': 81, 'CRO': 73, 'POR': 73, 'DEN': 133,
                           'IRL': 133, 'FIN': 57, 'HUN': 180, 'CZE': 111, 'ROU': 106, 'BEL': 165,
                           'BUL': 46, 'LTU': 50, 'SVK': 28, 'SLO': 90, 'EST': 25, 'LAT': 29,
                           'LUX': 13, 'MLT': 5, 'CYP': 15, 'USA': 591}

        df_2021 = pd.DataFrame({
            'Year': 2021,
            'Country Code': list(delegation_2021.keys()),
            'taille_délégation': list(delegation_2021.values())
        })
        df_2024 = pd.DataFrame({
            'Year': 2024,
            'Country Code': list(delegation_2024.keys()),
            'taille_délégation': list(delegation_2024.values())
        })
        delegation = pd.concat([delegation, df_2021, df_2024], ignore_index=True)
    
    #On fusionne et on obtient le df complet paré pour régresser 
    df_clean = df_clean.merge(delegation, on=['Year', 'Country Code'], how='left')
    df_clean = df_clean.dropna(subset=['taille_délégation'])
    return df_clean
