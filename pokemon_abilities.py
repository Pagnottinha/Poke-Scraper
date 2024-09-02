import scrapy

class PokeAbilitySpider(scrapy.Spider):
    name = 'pokemon_ability_scrapper'
    domain = "https://pokemondb.net"

    start_urls = ["https://pokemondb.net/ability"]

    def parse(self, response: scrapy.http.HtmlResponse):
        pokemons = response.css('#abilities > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td > a.ent-name::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_ability)

    def parse_ability(self, response: scrapy.http.HtmlResponse):
        name = response.css('#main > h1::text').get()
        description = ''.join(response.css('div.grid-row > div:nth-child(1) > p').xpath('.//text()').getall()).strip()
        pokemons_table = response.css('div.resp-scroll > table.data-table > tbody > tr')

        pokemons = '['
        for pokemon in pokemons_table:
            pokemons += f'{int(pokemon.css('td:nth-child(1) span::text').get())},'

        if len(pokemons) > 1:
            pokemons = pokemons[:-1]

        pokemons += ']'

        yield {
            'ability_name': name,
            'description': description,
            'ability_url': response.url,
            'pokemons': pokemons
        }