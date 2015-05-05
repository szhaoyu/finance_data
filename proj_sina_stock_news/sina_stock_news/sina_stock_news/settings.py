# -*- coding: utf-8 -*-

# Scrapy settings for sina_stock_news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'sina_stock_news'

SPIDER_MODULES = ['sina_stock_news.spiders']
NEWSPIDER_MODULE = 'sina_stock_news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sina_stock_news (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 10
COOKIES_ENABLED = True

ITEM_PIPELINES = {
        'sina_stock_news.pipelines.NewsImagesPipeline': 600,
        'sina_stock_news.pipelines.MongodbImagesPipeline': 700,
        }

#DOWNLOADER_MIDDLEWARES = {
#        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
#        'crawler_images.rotate_useragent.RotateUserAgentMiddleware': 400,
#        }

IMAGES_STORE = os.path.join(os.getcwd(), 'image')
IMAGES_EXPIRES = 90
#IMAGES_THUMBS = {
#        'small': (50, 50),
#        'big': (500, 500),
#        }
#IMAGES_MIN_HEIGHT = 110
#IMAGES_MIN_WIDTH = 110

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'sina_stock'
MONGODB_COLLECTION = 'news'

