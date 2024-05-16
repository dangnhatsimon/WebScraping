from typing import Iterable
import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]
    # start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250',
                             headers={
                                 'User-Agent': self.user_agent
                             })
    
    rules = (Rule(LinkExtractor(restrict_xpaths="//div[@class='ipc-metadata-list-summary-item__tc']//a"),
                  callback="parse_item",
                  follow=True,
                  process_request='set_user_agent'),
             )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request
         
    def parse_item(self, response):
        # item = {}
        # item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        # item["name"] = response.xpath('//div[@id="name"]').get()
        # item["description"] = response.xpath('//div[@id="description"]').get()
        # return item
        # print(response.url)
        yield {
            'title': response.xpath("//span[@class='hero__primary-text']/text()").get(),
            'year': response.xpath("(//h1[@data-testid='hero__pageTitle']/following-sibling::node())[1]/li[1]/a[1]/text()").get(),
            'duration': response.xpath("normalize-space(//h1[@data-testid='hero__pageTitle']/following-sibling::node()/li[3]/text())").get(),
            'genre': response.xpath("(//div[@class='ipc-chip-list__scroller'])[1]/a/span/text()").getall(),
            'rating': ''.join(response.xpath("(//div[@data-testid='hero-rating-bar__aggregate-rating__score'])[position() = 2]//text()").getall()),
            'movie_url': response.url
        }
