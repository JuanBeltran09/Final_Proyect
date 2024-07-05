import pandas as pd

def filtro():

    df = pd.read_csv('db1.csv', on_bad_lines='skip', delimiter=';', low_memory=False)

    filtered_df = df.dropna(subset=['vernacularName'])
    return filtered_df

def filtro_Municipio(df,mun):
    filtro = df[df['municipality'] == mun]
    return filtro

def filtro_Animales(df, animales):
    filtro = df[df['vernacularName'].isin(animales)]
    return filtro
