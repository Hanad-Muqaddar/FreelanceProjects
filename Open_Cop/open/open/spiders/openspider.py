import scrapy
from scrapy_selenium import SeleniumRequest
from ..utils import clean
from ..items import OpenItem
import pandas as pd

class OpenspiderSpider(scrapy.Spider):
    name = 'openspider'
    def start_requests(self):
        df = pd.read_excel("C:/Users/Lenovo/Desktop/Five_Proj/Data/1 (1).xlsx")
        urls = list(df['Link'])
        for link in urls:
            yield SeleniumRequest(url=link, wait_time = 3 ,callback=self.parse)

    def parse(self, response):
        item = OpenItem()
        item['Name'] = clean(response.xpath('//h1[@class="wrapping_heading fn org"]/text()').get())
        item['Url'] = response.url
        yield item
