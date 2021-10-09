import os
import pytest
from scrapy.http import HtmlResponse
from scrape.spiders.adv import AdvSpider
from scrape.items import StockItem


@pytest.fixture()
def dummy_dor():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './dor.html')
    body = open(file_path, 'rb').read()
    
    return HtmlResponse(
        url='https://br.advfn.com/bolsa-de-valores/bovespa/rede-dor-sao-luiz-on-RDOR3/historico/mais-dados-historicos', body=body)

def test_should_get_68_14_when_call_dor_stock(dummy_dor):
    spider = AdvSpider(limit=1)
    result = next(spider.parse_stock(dummy_dor))

    assert StockItem(
        code='RDOR3', 
        last_price='68,14', 
        url='https://br.advfn.com/bolsa-de-valores/bovespa/rede-dor-sao-luiz-on-RDOR3/historico/mais-dados-historicos') == result