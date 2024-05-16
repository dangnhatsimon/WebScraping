from typing import Any, Iterable
import scrapy
from scrapy_splash import SplashRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy.selector import Selector
from urllib.parse import urlencode, quote


API_KEY = 'YOUR_API_KEY'


def get_scrapeops_url(url):
    payload = {
        'api_key': API_KEY, 
        'url': url, 
        'bypass': 'cloudflare_level_1',
        'js_render': 'true',
        'antibot': 'true',
        'premium_proxy': 'true'
    }
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class CoinSpiderSelenium(scrapy.Spider):
    name = "coin_selenium"
    allowed_domains = ["www.livecoinwatch.com"]
    start_urls = [
        "https://www.livecoinwatch.com"
        ]
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # chrome_path = which("chromedriver")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(self.start_urls[0])
        
        self.html = driver.page_source
        driver.close()
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
    
    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath("//tr[@class='table-row filter-row']"):
            yield {
                'symbol': currency.xpath(".//td[2]/a/div/div[@class='item-name ml10']/div/text()[1]").get(),
                'currency': currency.xpath(".//td[2]/a/div/div[@class='item-name ml10']/small/text()").get(),
                'price': currency.xpath(".//td[@class='filter-item table-item main-price']/text()[2]").get(),
                'volume(24h)': currency.xpath(".//td[@class='filter-item table-item volume price']/text()").get()
            }
