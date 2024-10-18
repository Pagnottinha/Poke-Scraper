import scrapy
from PIL import Image
import numpy as np
import requests
from io import BytesIO
from typing import Dict
import colorsys
from collections import Counter

class PokemonBaseScraper(scrapy.Spider):
  name = 'pokemon_base_scraper'
  domain = "https://pokemondb.net"
  start_urls = ["https://pokemondb.net/pokedex/all"]

  MAIN_COLORS = {
    'red': (255, 0, 0),
    'brown': (165, 42, 42),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'pink': (255, 192, 203),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
  }

  def parse(self, response: scrapy.http.HtmlResponse):
    pokemons = response.css('#pokedex > tbody > tr')
    for pokemon in pokemons:
      link = pokemon.css("td.cell-name > a::attr(href)").get()
      yield response.follow(self.domain + link, self.parse_pokemon)

  def parse_pokemon(self, response: scrapy.http.HtmlResponse):
    image_url = response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active img::attr(src)').get()
    vitals_table = response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr')

    yield {
      'id': vitals_table.css('tr:nth-child(1) > td > strong::text').get(),
      'name': response.css('#main > h1::text').get(),
      'url': response.url,
      'color': self.get_dominant_color(image_url),
      'height': vitals_table.css('tr:nth-child(4) > td::text').get(),
      'weight': vitals_table.css('tr:nth-child(5) > td::text').get(),
      'types': vitals_table.css('tr:nth-child(2) > td > a::text').getall()
    }

  @staticmethod
  def find_closest_color(color: np.ndarray, color_dict: Dict[str, tuple]) -> str:
    # Convert RGB to HSV for better color comparison
    h, s, v = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
    
    min_distance = float('inf')
    closest_color = None
    
    for name, rgb in color_dict.items():
      h2, s2, v2 = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

      # Calculate distance in HSV space, with more weight on hue
      distance = abs(h - h2) * 10 + abs(s - s2) + abs(v - v2)
      
      if distance < min_distance:
        min_distance = distance
        closest_color = name

    return closest_color

  @staticmethod
  def remove_transparency(image: Image.Image) -> Image.Image:
    if image.mode in ('RGBA', 'LA'):
      background = Image.new('RGB', image.size, (255, 255, 255))
      background.paste(image, mask=image.split()[3])
      return background
    return image

  def get_dominant_color(self, image_url: str) -> str:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image = self.remove_transparency(image)

    # Convert image to RGB mode if it's not already
    if image.mode != 'RGB':
      image = image.convert('RGB')

    image = image.resize((100, 100))  # Reduce image size for better performance
    pixels = np.array(image).reshape(-1, 3)

    # Filtrar cores muito claras ou escuras
    filtered_pixels = [tuple(pixel) for pixel in pixels if np.all(pixel < [240, 240, 240]) and np.all(pixel > [10, 10, 10])]

    if not filtered_pixels:
        return 'white'  # Retorna 'white' se não houver pixels válidos

    # Contar a frequência de cada cor
    color_counts = Counter(filtered_pixels)

    # Encontrar a cor mais comum
    most_common_color = color_counts.most_common(1)[0][0]

    return self.find_closest_color(np.array(most_common_color), self.MAIN_COLORS)