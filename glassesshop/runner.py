import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from worldometers.worldometers.spiders.countries import CountriesSpider
from glassesshop.spiders.glasses import GlassesSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(GlassesSpider)
process.start()