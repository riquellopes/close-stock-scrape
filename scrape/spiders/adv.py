import string
import scrapy
from scrapy.utils.project import get_project_settings
from urllib.parse import urlparse
from scrapy.http import FormRequest
from scrape.items import StockItem

class AdvSpider(scrapy.Spider):
    name = 'adv'
    allowed_domains = ['br.advfn.com']

    def start_requests(self):
        return (scrapy.Request(f'https://br.advfn.com/bolsa-de-valores/bovespa/{letter}', self.parse) for letter in list(string.ascii_uppercase))

    def parse(self, response):
        settings = get_project_settings()
        formdata = {
            "Date1": settings.get("START_DATE"),
            "Date2": settings.get("END_DATE")
        }
        tr_element = response.css("table.atoz-link-bov")[0].css("tr") if response.css("table.atoz-link-bov") else []
       
        for tr in tr_element:
            url = str(tr.css("td a::attr(href)").extract_first()).replace("cotacao", "historico/mais-dados-historicos")
            if urlparse(url).netloc == '':
                continue
            yield FormRequest(f"https:{url}", callback=self.parse_stock, formdata=formdata)

    def parse_stock(self, response):
        url = response.url
        code = response.css("h1.symbol-h1 strong::text").extract_first()
        last_price = 0

        if len(response.css("table.histo-results tr")[1].css("td::text")) > 1:
            last_price = response.css("table.histo-results tr")[1].css("td::text")[1].extract()
        yield StockItem(code=code, last_price=last_price, url=url)
