# scripts/idh.py
import pandas as pd

def process_idh():
    df_IDH = pd.read_excel("../data/raw/IDH 1990_2023.xlsx", skiprows=4, engine="openpyxl")
    cols_to_drop = [
         'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9',
        'Unnamed: 11', 'Unnamed: 13', 'Unnamed: 15', 'Unnamed: 17',
        'Unnamed: 21', 'Unnamed: 23', 'Unnamed: 25'
    ]
    df_IDH = df_IDH.drop(columns=cols_to_drop)

    # Colonnes IDH disponibles
    idh_years = [1990, 2000, 2010, 2015, 2020, 2021, 2022, 2023]

    # Années JO et mapping
    jo_years = [1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2021, 2024]
    idh_for_jo = {1988:1990,1992:1990,1996:1990,2000:2000,2004:2000,2008:2000,2012:2010,2016:2015,2021:2020,2024:2023}

    df_idh_long = df_IDH.melt(id_vars='Country', value_vars=idh_years, var_name='Year_IDH', value_name='HDI')
    df_idh_long['Year_JO'] = df_idh_long['Year_IDH'].map({v:k for k,v in idh_for_jo.items()})
    df_idh_long['Year_IDH'] = df_idh_long['Year_IDH'].astype(int)
    df_idh_long.rename(columns={'Year_JO':'Year'}, inplace=True)
    #df_idh_long.to_csv("../data_clean/df_IDH.csv", index=False)
    return df_idh_long
