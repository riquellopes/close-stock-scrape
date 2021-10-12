# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonItemExporter


class ScrapePipeline:
    def process_item(self, item, spider):
        self._exporter.export_item(item)
        return item
    
    def open_spider(self, spider):
        self._file = open('stocks.json', 'wb')
        self._exporter = JsonItemExporter(self._file)
        self._exporter.start_exporting()
    
    def close_spider(self, spider):
        self._exporter.finish_exporting()
        self._file.close()