### Onde vai ocorrer a junção dos csv
import pandas as pd
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

df = pd.read_csv('./data.csv')

df.dropna(inplace=True)

df['height'] = df['height'].apply(extract_cm)
df['weight'] = df['weight'].apply(extract_kg)

df.columns = ['Numero', 'Nome', 'URL', 'Tamanho_em_CM', 'Peso_em_KG', 'Tipo']

df.to_json('pokemon_data.json', orient='records', indent=4)

