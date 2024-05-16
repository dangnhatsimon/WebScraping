from typing import Iterable
import scrapy
from scrapy.http import Request
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class ComputerdealsSpider(CrawlSpider):
    name = "computerdeals"
    allowed_domains = ["slickdeals.net"]
    start_urls = ["https://slickdeals.net/computer-deals/"]
    # start_urls = [f"https://slickdeals.net/computer-deals/?page={i}" for i in range(1,13)]
    page = 1
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    pattern = r"\n|\xa0|Get Deal at |\t"
    
    def remove_characters(self, value):
        if re.match(self.pattern, value):
            return re.sub(self.pattern, "", value).strip()
        else:
            return None
    
    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            wait_time=3,
        )
        
    # def start_requests(self):
    #     yield scrapy.Request(url=self.start_urls[0],
    #                          headers={
    #                              'User-Agent': self.user_agent
    #                          })
    
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//div[@class='bp-c-card_content']/a[2]"),
            callback='parse',
            follow=False,
            process_request='set_user_agent'
        ),
        Rule(
            LinkExtractor(allow=r"page=\d"),
            follow=True
        ),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request 
        
    def parse(self, response):
        yield {
            'name': self.remove_characters(response.xpath("//div[@id='dealTitle']/h1/text()").get()) or None,
            'link': response.url,
            'store_name': self.remove_characters(response.xpath("//div[@class='buyNowButton']/a[1]/text()").get()) or None,
            'price': response.xpath("normalize-space((//div[@class='dealPrice'])[1]/text())").get(),
            'original_price': response.xpath("normalize-space((//span[@class='oldListPrice'])[1]/text())").get() or None,
        }
        # products = response.xpath("//li[@data-catalogitem='DealCard']/div[@class='bp-c-card_content']")
        # for product in products:
        #     yield {
        #         'name': product.xpath(".//a[2]/text()").get(),
        #         'link': "https://slickdeals.net" + product.xpath(".//a[2]/@href").get(),
        #         'store_name': self.remove_characters(product.xpath(".//span[@class='bp-c-card_subtitle']/text()").get()) or None,
        #         'price': product.xpath("normalize-space(.//span[@class='bp-p-dealCard_price']/text())").get(),
        #         'original_price': product.xpath("normalize-space(.//span[@class='bp-p-dealCard_originalPrice']/text())").get() or None,
        #     }
        
        # pages = response.xpath("////div[@class='bp-c-pagination_wrapper'][last()]/child::node()/text()").get()
        # for page in range(2, pages+1):
        #     next_page = f"{self.start_urls[0]}/?page={self.page}"
        #     if next_page:
        #         yield response.follow(next_page, callback=self.parse)

            
        
