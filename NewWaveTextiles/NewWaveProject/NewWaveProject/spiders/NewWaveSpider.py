import scrapy
import json


class NewwavespiderSpider(scrapy.Spider):
    name = 'NewWaveSpider'
    
    def start_requests(self):
        count_number = 48
        for i in range(1,31):
            url = f"https://www.newwavetextiles.nl/products/productlist?offset={count_number}&facets=%7B%7D&orderBy=relevance&outlet=false"
            count_number += 48
            yield scrapy.Request(url=url, callback=self.parse)
    
    
    def parse(self, response):
        skus = response.xpath("//article[@class='product']/@data-product-id").getall()
        for sku in skus:
            api_url = f"https://www.newwavetextiles.nl/api/nl/product/{sku}/matrix?includeStock=false&outlet=false"
            yield scrapy.Request(url=api_url, callback=self.parse_final_object)
    
    def parse_final_object(self, response):
        data = json.loads(response.body)
        rows = data['rows']
        for i in rows:
            final_prod_skus = i['quantities']
            for j in final_prod_skus:
                item = {}
                item['Sku'] = j['sku']
                item['Stock'] = j['stock']
                if int(item['Stock']) > 1:
                    text = "werkdag voor 11 uur besteld, volgende werkdag verzonden"
                else:
                    text = "2-4 werkdagen"
                item['Levertijd'] = text
                yield item
            
