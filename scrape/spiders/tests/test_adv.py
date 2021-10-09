import os
import pytest
from scrapy.http import HtmlResponse
from scrape.spiders.adv import AdvSpider
from scrape.items import StockItem

def read(name):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, f'./{name}.html')
    return open(file_path, 'rb').read()

@pytest.fixture()
def dummy_dor(): 
    return HtmlResponse(
        url='https://br.advfn.com/bolsa-de-valores/bovespa/rede-dor-sao-luiz-on-RDOR3/historico/mais-dados-historicos', body=read('dor'))

@pytest.fixture()
def dummy_zynga(): 
    return HtmlResponse(
        url='https://br.advfn.com/bolsa-de-valores/bovespa/zynga-Z2NZ34/historico/mais-dados-historicos', body=read('zynga'))


def test_should_get_68_14_when_call_dor_stock(dummy_dor):
    spider = AdvSpider(limit=1)
    result = next(spider.parse_stock(dummy_dor))

    assert StockItem(
        code='RDOR3', 
        last_price='68,14', 
        url='https://br.advfn.com/bolsa-de-valores/bovespa/rede-dor-sao-luiz-on-RDOR3/historico/mais-dados-historicos') == result

def test_should_get_0_when_price_notfound(dummy_zynga):
    spider = AdvSpider(limit=1)
    result = next(spider.parse_stock(dummy_zynga))

    assert StockItem(
        code='Z2NZ34', 
        last_price=0, 
        url='https://br.advfn.com/bolsa-de-valores/bovespa/zynga-Z2NZ34/historico/mais-dados-historicos') == result