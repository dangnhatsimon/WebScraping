import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.example import ExampleSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(ExampleSpider)
process.start()