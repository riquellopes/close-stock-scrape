from scrapy.crawler import CrawlerProcess
from scrape.spiders.adv import AdvSpider

def main(event, context):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': '/tmp/stocks.json'
    })

    process.crawl(AdvSpider)
    process.start()

if __name__ == '__main__':
    main(None, None)