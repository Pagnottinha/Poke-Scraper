# Poke-Scraper

O objetivo é fazer um scraper que navega no site e coleta as informações, trata e gerar o resultado em formato json

O que devemos buscar de cada Pokémon obrigatoriamente:

- Número
- URL da página
- Nome
- Próximas evoluções do Pokémon se houver (Número, nome e URL)
- Tamanho em cm
- Peso em kg apenas
- Tipos (água, veneno, ...)
- Habilidades (link para outra página)
    - URL da página
    - Nome
    - Descrição do efeito

Pode puxar mais dados, mas são opcionais.

### Como rodar o projeto

1. Instale as dependencias.

```
pip install -r requirements.txt
```

2. Rode os spiders (scrapers).

- Utilização das spiders

```
scrapy runspider nome_arquivo.py -o nome_saida.csv
```

3. Atualize as variáveis de caminho e execute o main.py (o tratamento desses dados)

```
python main.py
```