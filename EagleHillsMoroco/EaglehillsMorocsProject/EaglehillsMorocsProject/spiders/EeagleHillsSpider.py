import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import EaglehillsmorocsprojectItem
from ..utils import clean

class EeaglehillsspiderSpider(scrapy.Spider):
    name = 'EeagleHillsSpider'

    def start_requests(self):
        for i in range(2000, 11442):
            url = f"https://www.eaglehillsmorocco.com/fr/node/{i}"
            yield SeleniumRequest(url=url, callback=self.parse)
            
    def parse(self, response):
        item = EaglehillsmorocsprojectItem()
        item['First_Name'] = clean(response.css(".field--name-field-first-name .field__item ::text").get())
        item['Last_Name'] = clean(response.css(".field--name-field-last-name .field__item ::text").get())
        item['Email'] = clean(response.css(".field--name-field-email-address .field__item ::text").get())
        item['Phone_Number'] = clean(response.css(".field--name-field-phone-number .field__item ::text").get())
        item['Url'] = response.url
        yield  item
        
        self.state['items_count'] = self.state.get('items_count', 0) + 1
