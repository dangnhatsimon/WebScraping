import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from worldometers.worldometers.spiders.countries import CountriesSpider
from bookscraper.spiders.bookspider import BookspiderSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(BookspiderSpider)
process.start()