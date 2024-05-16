from typing import Iterable
import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = "coin"
    allowed_domains = ["www.livecoinwatch.com"]
    start_urls = ["https://www.livecoinwatch.com"]

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(3))
            
            splash:set_viewport_full()
            return splash:html()
            end
    '''
    
    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0], callback=self.parse, endpoint='execute', args={'lua_source': self.script})
    
    def parse(self, response):
        for currency in response.xpath("//tr[@class='table-row filter-row']"):
            yield {
                'symbol': currency.xpath(".//td[2]/a/div/div[@class='item-name ml10']/div/text()[1]").get(),
                'currency': currency.xpath(".//td[2]/a/div/div[@class='item-name ml10']/small/text()").get(),
                'price': currency.xpath(".//td[@class='filter-item table-item main-price']/text()[2]").get(),
                'volume(24h)': currency.xpath(".//td[@class='filter-item table-item volume price']/text()").get()
            }
