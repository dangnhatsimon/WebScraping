from typing import Iterable
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = "example"
    # allowed_domains = ["example.com"]
    # start_urls = ["https://example.com"]
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com/',
            wait_time=3,
            screenshot=True,
            callback=self.parse,
        )
            
    def parse(self, response):
        img = response.meta['screenshot']
        
        with open('screenshot.png', 'wb') as f:
            f.write(img)
            
        driver = response
        # print(response)
        # with open('response.txt', 'w') as f:
        #     f.write(response)
            
        # search_input = driver.find_element(By.XPATH, '//input[@id="searchbox_input"]')
        # search_input.send_keys('Hello World')
        # search_input.send_keys(Keys.ENTER)
        
        # # driver.save_screenshot('after_filling_input.png')
        
        # html = driver.page_source
        # response_obj = Selector(text=html)
            
        # links = response_obj.xpath("//ol[@class='react-results--main']/li/article/div/div/a")
        # for link in links:
        #     yield {
        #         'URL': link.xpath(".//@href").get()
        #     }
        