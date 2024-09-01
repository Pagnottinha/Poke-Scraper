# https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
# https://www.digitalocean.com/community/tutorials/como-fazer-crawling-em-uma-pagina-web-com-scrapy-e-python-3-pt
# http://pythonclub.com.br/material-do-tutorial-web-scraping-na-nuvem.html
import scrapy

class PokemonBaseScrapper(scrapy.Spider):
  name = 'pokemon_base_scrapper'
  domain = "https://pokemondb.net"

  start_urls = ["https://pokemondb.net/pokedex/all"]

  def parse(self, response: scrapy.http.HtmlResponse):
    pokemons = response.css('#pokedex > tbody > tr')
    for pokemon in pokemons:
    #pokemon = pokemons[0]
      link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
      yield response.follow(self.domain + link, self.parse_pokemon)

  def parse_pokemon(self, response: scrapy.http.HtmlResponse):
    with open("response.html", "wb") as f:
        f.write(response.body)
    yield {
      'id': response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
      'name': response.css('#main > h1::text').get(),
      'url': response.url,
      'height': response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(4) > td::text').get(),
      'width': response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(5) > td::text').get(),
      'types': response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(2) > td > a::text').getall()
    }
