import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from worldometers.worldometers.spiders.countries import CountriesSpider
from tinydeal.spiders.special_offers import SpecialOffersSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(SpecialOffersSpider)
process.start()