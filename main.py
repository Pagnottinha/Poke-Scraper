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

#Função para combinar habilidades
def combine_abilities(abilities):
    combined = []
    for ability in abilities:
        url = ability['url']
        name = ability['name'].strip()
        description = ability['description'].strip()
        combined.append({'url': url, 'name': name, 'description': description})
    return combined

# Agrupar por ID e combinar as habilidades
def aggregate(group):
    # Unir evoluções em uma lista de dicionários
    evolutions = group['evolutions'].iloc[0] if not group['evolutions'].isnull().all() else []
    
    # Combinar habilidades
    combined_abilities = []
    for abilities in group['abilities']:
        combined_abilities.extend(combine_abilities([abilities]))
    
    # Construir o resultado
    result = {
        'name': group['name'].iloc[0],
        'url_pokemon': group['url_pokemon'].iloc[0],
        'height': group['height'].iloc[0],
        'weight': group['weight'].iloc[0],
        'types': group['types'].iloc[0],
        'evolutions': evolutions,
        'abilities': combined_abilities
    }
    return result

def filter_evolutions(row):
    pokemon_name = row['name']
    evolutions = row['evolution']
    start_save = False
    array_evolutions = []

    print(f'Pokemon: {pokemon_name}\nEvolutions: {evolutions}')
    if evolutions != None:
        for evolution in evolutions:
            if start_save:
                array_evolutions.append(evolution)
            if pokemon_name == evolution['name']:
                start_save = True

    return [evo for evo in array_evolutions if evo['name'] != pokemon_name]
            

df = pd.read_csv('data.csv')
df.dropna(inplace=True)

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
                    df.at[index, 'evolution'].append(evolution)


df['height'] = df['height'].apply(extract_cm)
df['weight'] = df['weight'].apply(extract_kg)

df['evolution'] = df.apply(lambda row: filter_evolutions(row), axis=1)

df.to_json('pokemon_data.json', orient='records', indent=4)

