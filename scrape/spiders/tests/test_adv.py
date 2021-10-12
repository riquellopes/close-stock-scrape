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


@pytest.fixture()
def dummy_letter_b(): 
    return HtmlResponse(
        url='https://br.advfn.com/bolsa-de-valores/bovespa/B', body=read('letter_b'))

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

def test_should_call_with_b2w_data(dummy_letter_b, mocker):
    form = mocker.patch('scrape.spiders.adv.FormRequest')

    spider = AdvSpider(limit=1)
    next(spider.parse(dummy_letter_b))

    form.assert_called()
    form.assert_called_with(
        'https://br.advfn.com/bolsa-de-valores/bovespa/b2w-digital-on-BTOW1/historico/mais-dados-historicos',
        callback=spider.parse_stock,
        formdata={'Date1': '23/12/20', 'Date2': '23/12/20'}
    )