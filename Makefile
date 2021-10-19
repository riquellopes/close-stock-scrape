.SILENT:

run:
	scrapy runspider scrape/spiders/adv.py

clean:
	find . -name "*.pyc" -exec rm -rf {} \;