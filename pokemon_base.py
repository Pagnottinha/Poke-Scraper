# https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
# https://www.digitalocean.com/community/tutorials/como-fazer-crawling-em-uma-pagina-web-com-scrapy-e-python-3-pt
# http://pythonclub.com.br/material-do-tutorial-web-scraping-na-nuvem.html
import scrapy

class PokeSpider(scrapy.Spider):
    name = 'pokemon_base_scrapper'
    domain = "https://pokemondb.net"

    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response: scrapy.http.HtmlResponse):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_pokemon)

    def parse_pokemon(self, response: scrapy.http.HtmlResponse):
        id = response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
        name = response.css('#main > h1::text').get(),
        url_pokemon = response.url,
        height = response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(4) > td::text').get(),
        weight = response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(5) > td::text').get(),
        types = response.css('#main > .tabset-basics > .sv-tabs-panel-list > .active .vitals-table > tbody > tr:nth-child(2) > td > a::text').getall()
        evolutions = response.css('div.infocard-list-evo > div.infocard')
    
        array_evolutions = []

        for evolution in evolutions:
            number = evolution.css('small::text').get()
            name = evolution.css('a::text').get()
            url = self.domain + evolution.css('a::attr(href)').get()

            if number and name and url:
                array_evolutions.append({"number": number, "name": name, "url": url})

        abilities_urls = response.css('div:nth-child(1) > div:nth-child(2) > table > tbody > tr:nth-child(6) > td > * > a::attr(href)').getall()    
        for url in abilities_urls:
            yield response.follow(self.domain + url, self.parse_abilities, meta={"id": id, "name": name, "url_pokemon": url_pokemon, "height": height, "weight": weight, "types": types,
            "evolutions": array_evolutions})

    def parse_abilities(self, response: scrapy.http.HtmlResponse):
        name = response.css('#main > h1::text').get()
        description = ''.join(response.css('div.grid-row > div:nth-child(1) > p::text').getall()).strip()
    
        yield {
        "id" : response.meta["id"],
        "name": response.meta["name"],
        "url_pokemon": response.meta["url_pokemon"],
        "height": response.meta["height"],
        "weight": response.meta["weight"],
        "types": response.meta["types"],
        "evolutions": response.meta["evolutions"],
        "abilities": {
            "url": response.url,
            "name": name,
            "description": description
        }}