# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OpenItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Url = scrapy.Field()
