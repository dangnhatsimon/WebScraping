import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from worldometers.worldometers.spiders.countries import CountriesSpider
from bookstoscrape.spiders.books import BooksSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(BooksSpider)
process.start()