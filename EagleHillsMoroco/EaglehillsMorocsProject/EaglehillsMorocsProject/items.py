# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EaglehillsmorocsprojectItem(scrapy.Item):
    # define the fields for your item here like:
    First_Name = scrapy.Field()
    Last_Name = scrapy.Field()
    Email = scrapy.Field()
    Phone_Number = scrapy.Field()
    Url = scrapy.Field()
