import scrapy
import pandas as pd
# from unidecode import unidecode

class ViseemannvSpider(scrapy.Spider):
    name = 'ViseeMannv'

    def start_requests(self):
        df = pd.read_csv("D:/DestopFolder/Five_Proj/PhillProject/ViesMan/German_Postal_Codes_PLZ.csv")
        codes = df['Codes']
        for code in codes:
            # 71686
            urls = [
                f'https://api.viessmann.com/dealer-locator/dealer-search/api/dealer/nearby/address?locale=de-DE&query={code}&count=25',
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        Dealers = data['dealers']
        if len(Dealers) > 0:
            for t in Dealers:    
                item = {}
                item['Name'] = t['name']
                item['Address'] = self.make_address(t['address'])
                item['State'] = t['address']['state']
                item['Country'] = t['address']['country']
                item['Phone'] = t['contact']['phone']
                item['Fax'] = t['contact']['fax']
                item['Mail'] = t['contact']['mail']
                try:
                    item['Distance'] = round(t['distance']['kilometers'], 1)
                except:
                    item['Distance'] = ""
                item['Web-Url'] = t['contact']['homepage']
                item['Specialization'] = t['skills']
                yield item


    def make_address(self, data):
        street = data['street']
        post_code = data['postcode']
        city = data['city']
        complete_address = street + " " + post_code + " " + city
        return complete_address
