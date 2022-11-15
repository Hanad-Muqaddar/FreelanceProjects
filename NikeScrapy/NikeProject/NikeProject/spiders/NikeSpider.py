import scrapy
import json

class NikespiderSpider(scrapy.Spider):
    name = 'NikeSpider'
    start_urls = ['https://www.nike.com/']

    def parse(self, response):
        links = response.css("#DesktopMenu-0-4-0 .pre-text-color-secondary ::attr(href)").getall()
        for i in links:
            yield scrapy.Request(url=i, callback=self.parse_products)
    
    def parse_products(self, response):
        if response.url == "https://www.nike.com/w/sale-3yaep":
            number = 0
            for i in range(0, 4850//24 + 1):
                api = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=35F8B9FCC766A33196E5E064E13C9636&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(5b21a62a-0503-400c-8336-3ccfbff2a684)%26anchor%3D{number}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24"
                number += 24
                yield scrapy.Request(url=api, callback=self.product_json_parse)
    
    def product_json_parse(self, response):
        data = json.loads(response.body)
        products = data['data']['products']['products']
        for i in products:
            url = i['url'].replace('{countryLang}', "https://www.nike.com")
            item = {}
            item['Title'] = i['title']
            item['Url'] = url
            yield item

                