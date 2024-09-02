### Onde vai ocorrer a junção dos csv
import pandas as pd
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

#Agrupar por ID e combinar as habilidades
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

df = pd.read_csv('data.csv')
df.dropna(inplace=True)

df['height'] = df['height'].apply(extract_cm)
df['weight'] = df['weight'].apply(extract_kg)

df['evolutions'] = df['evolutions'].apply(lambda x: ast.literal_eval(x))
df['abilities'] = df['abilities'].apply(lambda x: ast.literal_eval(x))

# Aplicar agregação
df_grouped = df.groupby('id').apply(aggregate).apply(pd.Series)
df_grouped.to_json('pokemon_data.json', orient='records')

print(df_grouped)