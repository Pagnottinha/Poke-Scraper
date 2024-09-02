### Onde vai ocorrer a junção dos csv
import pandas as pd
import numpy as np
import json
import ast
import re

# Função de extrair somente o valor em kg
def extract_kg(weight_text):
    match = re.search(r'(\d+\.?\d*)\s*kg', weight_text)
    if match:
        return match.group(1) + ' kg' 
    return None

# Função de extrair a altura em cm
def extract_cm(height_text):
    match = re.search(r'(\d+\.?\d*)\s*m', height_text)
    if match:
        return str(round(float(match.group(1)) * 100, 1)) + ' cm' 
    return None

def filter_evolutions(row):
    pokemon_name = row['name']
    evolutions = row['evolution']
    start_save = False
    array_evolutions = []

    if evolutions != None:
        for evolution in evolutions:
            if start_save:
                array_evolutions.append(evolution)
            if pokemon_name == evolution['name']:
                start_save = True

    return [evo for evo in array_evolutions if evo['name'] != pokemon_name]
            

df_pokemons = pd.read_csv('data.csv')
df_pokemons.dropna(inplace=True)

df_pokemons['id'] = df_pokemons['id'].apply(lambda x: int(x))
df_pokemons['height'] = df_pokemons['height'].apply(extract_cm)
df_pokemons['weight'] = df_pokemons['weight'].apply(extract_kg)

df_abilities = pd.read_csv('data_abilities.csv')
df_abilities.dropna(inplace=True)

df_abilities['pokemons'] = df_abilities['pokemons'].apply(lambda x: ast.literal_eval(x))
df_abilities_expanded = df_abilities.explode('pokemons')
df_abilities_expanded.drop_duplicates()

merged_df = pd.merge(df_pokemons, df_abilities_expanded, left_on='id', right_on='pokemons')
# print(merged_df)

merged_df['abilities'] = merged_df.apply(
    lambda row: {
        'ability': row['ability_name'], 
        'description': row['description'],
        'ability_url': row['ability_url'],
    },
    axis=1
)

merged_df = merged_df.drop(columns=['pokemons', 'ability_name', 'description', 'ability_url'])

# Agrupa as habilidades de cada Pokémon em uma lista
df = merged_df.groupby(['id', 'name', 'url', 'height', 'weight', 'types']).agg({
    'abilities': list
}).reset_index()

df_evolutions = pd.read_csv('data_evolution.csv')

df['evolution'] = None

for i, row in df_evolutions.iterrows():
    evolutions = json.loads(re.sub(r"(?<=[:,\[{])\s*'(.*?)'\s*(?=[}\],:])", r'"\1"', row['evolutions']))
    
    for evolution in evolutions:
        for index, df_row in df.iterrows():
            if evolution['name'] == df_row['name']:
                if df.at[index, 'evolution'] is None:
                    df.at[index, 'evolution'] = []
                for evolution in evolutions:
                    if evolution not in df.at[index, 'evolution']:  
                        df.at[index, 'evolution'].append(evolution)


df['evolution'] = df.apply(lambda row: filter_evolutions(row), axis=1)

df.to_json('pokemon_data.json', orient='records', indent=4)
