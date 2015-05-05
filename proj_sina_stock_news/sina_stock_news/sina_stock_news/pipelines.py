# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from scrapy import log
from scrapy.conf import settings

class SinaStockNewsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongodbImagesPipeline(object):
    def __init__(self):
        import pymongo
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        #if item['image_urls'] and item['image_paths']:
        self.collection.insert(dict(item))
        log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        return item

class NewsImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            log.msg( 'REQUEST IMG: '+str(image_url), level=log.INFO )
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('WanImagesItem contains no images.')
        item['image_paths'] = image_paths
        log.msg( 'IMAGE_PATH: '+str(image_paths), level=log.INFO )
        return item



