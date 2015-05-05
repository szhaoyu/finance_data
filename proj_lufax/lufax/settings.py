# -*- coding: utf-8 -*-

# Scrapy settings for lufax project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lufax'

SPIDER_MODULES = ['lufax.spiders']
NEWSPIDER_MODULE = 'lufax.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lufax (+http://www.yourdomain.com)'

########### Item pipeline
ITEM_PIPELINES = [
                  "lufax.pipelines.JsonWriterPipeline",
]



