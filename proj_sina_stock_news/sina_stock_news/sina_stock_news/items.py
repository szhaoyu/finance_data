# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SinaStockNewsItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = Field()
    title = Field()
    pub_date = Field()
    media_name = Field()
    media_comment = Field()
    content = Field()
    #images in NEWs page...
    image_urls = Field()
    image_paths = Field()


