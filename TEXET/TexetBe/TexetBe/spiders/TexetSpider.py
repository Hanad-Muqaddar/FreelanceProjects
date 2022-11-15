import scrapy
import json

class TexetspiderSpider(scrapy.Spider):
    name = 'TexetSpider'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'authority': 'commerce.gateway.nwg.se',
        'method': 'GET',
        'path': '/assortment/nl/search?categories=298440&selectedFilters=%7B%7D&orderBy=relevance&pageSize=40&page=3',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'contextid': 'FC241118-1D6D-44B1-A884-CBD14DC40E85',
        'origin': 'https://www.texet.be',
        'pragma': 'no-cache',
        'referer': 'https://www.texet.be/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'Cookie': 'incap_ses_1221_2731571=0x9GDUgZxQUBoisoO93xEKMZZWMAAAAACpLTEgKR84H9y1yYMYoJxg==; nlbi_2731571=LQWYPbpMJQUr03qMm7f6DgAAAAAwJ3FyX97o7PUEKi1/5BVu; visid_incap_2731571=rkeQSUcNTMm4gaVgkv3PsvwXZWMAAAAAQUIPAAAAAABfp80bEqmXDTwWiK2VpH/C; ARRAffinity=a6b51ac05424af5c1f78f65bd84f21308992db0f024672d4a595fc4c1563aa54; ARRAffinitySameSite=a6b51ac05424af5c1f78f65bd84f21308992db0f024672d4a595fc4c1563aa54'
        }
    def start_requests(self):
        for i in range(1,22):
            url = f"https://commerce.gateway.nwg.se/assortment/nl/search?categories=298440&selectedFilters=%7B%7D&orderBy=relevance&pageSize=40&page={i}"
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        items = data['items']
        for ii in items:
            item = {}
            sku=  ii['price']['sku'].split("-")[0]
            next_url = f"https://www.texet.be/api/nl/product/{sku}/matrix?includeStock=false&outlet=false"
            yield scrapy.Request(url=next_url, callback=self.parse_final_object)
    
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
            
        
        
