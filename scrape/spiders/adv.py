import scrapy
import string

class AdvSpider(scrapy.Spider):
    name = 'adv'
    allowed_domains = ['br.advfn.com']

    def start_requests(self):
        for letter in list(string.ascii_uppercase):
            yield scrapy.Request(
                f'https://br.advfn.com/bolsa-de-valores/bovespa/{letter}', self.parse)

    def parse(self, response):
        for tr in response.css("table.atoz-link-bov")[0].css("tr"):
            link = tr.css("td a::attr(href)").extract_first()
            code = tr.css("td::text").extract_first()

            yield {'link': link, 'code': code}
