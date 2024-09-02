import scrapy

class EvolutionSpider(scrapy.Spider):
    name = 'pokemon_base_scrapper'
    domain = "https://pokemondb.net"

    start_urls = ["https://pokemondb.net/evolution"]

    def parse(self, response: scrapy.http.HtmlResponse):
        evolutions = response.css('div.infocard-filter-block > div.infocard-list-evo')

        array_evolutions = []

        for evolution in evolutions:
            evolution_chain = []  
            evolution_pokemon = evolution.css('div.infocard')

            for pokemon in evolution_pokemon:
                number = pokemon.css('small::text').get()
                name = pokemon.css('a::text').get()
                url = self.domain + pokemon.css('a::attr(href)').get()

                if number and name and url:
                    evolution_chain.append({"number": number, "name": name, "url": url})
            
            if evolution_chain:
                yield {
                    "evolutions": evolution_chain
                }