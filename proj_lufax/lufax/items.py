# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class LufaxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EntryItem(scrapy.Item):
    _id = Field()
    title = Field()
    url = Field()


class LoanRecord(scrapy.Item):
    title = Field()
    uid = Field()
    amount = Field()
    rate = Field()
    raising_begin = Field()
    raising_end = Field()
    maturity = Field()

