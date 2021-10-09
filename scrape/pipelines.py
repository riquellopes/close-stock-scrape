# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter


class ScrapePipeline:
    def process_item(self, item, spider):
        self._file.write(f"{json.dumps(dict(item))}\n")
        return item
    
    def open_spider(self, spider):
        self._file = open('prices.txt', 'w')
    
    def close_spider(self, spider):
        self._file.close()