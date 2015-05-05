# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from sina_stock_news.items import SinaStockNewsItem
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
import re

class StocknewsSpider(CrawlSpider):
    name = 'stockNews'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index_1.shtml']
    rules = (
        #Rule(LinkExtractor(allow=r'stock/jsy/\\d+/\\d+.shtml'), callback=self.parse_item, follow=True),
        #Rule(LinkExtractor(allow=r'finance/zq1/gsjsy/index_\\d+.shtml'), callback=self.parse, follow=True)
    )
    #reg_next_page = re.compile('<a title="下一页" href="\\./(index_\\d+.shtml)">')
    reg_next_page = re.compile('href="\\./(index_\\d+.shtml)">')
    reg_img_url = re.compile('<img src="([^"\n\r]+)[\r\n]*"')
    #reg_img_url = re.compile('<img src="(http://.*?(.jpg|.png|.gif))"')

    def parse_item(self, response):
        log.msg( 'Take detail url:' + response.url, level=log.INFO )
        i = SinaStockNewsItem()
        i['title'] = response.xpath('//*[@id="artibodyTitle"]/text()').extract()
        i['url'] = response.url
        i['pub_date'] = response.xpath('//span[@id="pub_date"]/text()').extract()
        i['media_name'] = response.xpath('//span[@id="media_name"]/text()').extract()
        content = response.xpath('//div[@id="artibody"]').extract()
        i['content'] = content[0]
        #log.msg( content[0], level=log.INFO )
        img_urls = re.findall( self.reg_img_url, content[0] )
        o_urls = []
        for url in img_urls:
            url1 = re.sub( "%0A$", "", url )
            o_urls.append( url1 )
        i['image_urls']=o_urls
        log.msg( str(o_urls), level=log.INFO )
        #parse different image urls
        yield i

    def parse(self, response):
        #log.msg( response.body, level=log.INFO )
        sel = Selector(response)
        #1. all items in current page
        urls = sel.re('<a href="(http://finance.sina.com.cn/stock/jsy/\\d+/\\d+.shtml)" target="_blank">')
        for url in urls:
            log.msg( url, level=log.INFO )
            yield Request( url, callback=self.parse_item)
        #2. next page detect
        #pageBar = sel.css('#Main > div.listBlk > table:nth-child(1) > tbody > tr > td > div > span.pagebox_next')
        #pageBar = sel.xpath( '//div[@id="Main"]/div[3]/table[1]/tbody/tr/td/div')
        #pageBar = response.xpath( '//div[@id="Main"]/div[3]/table[1]/tbody/tr/td/div')
        pageBar = response.xpath('//span[@class="pagebox_next"]')
        if pageBar != None and len(pageBar) > 0 :
            pageTxt = pageBar.extract()[0]
            log.msg( 'matched txt:'+pageTxt, level=log.INFO )
            tail_url = self.reg_next_page.search( pageTxt )
            log.msg('NEXT PAGE: '+tail_url.group(1), level=log.INFO )
            yield Request( 'http://roll.finance.sina.com.cn/finance/zq1/gsjsy/'+tail_url.group(1), callback=self.parse )
        #tbodys = sel.css( '.listBlk')
        #for tb in tbodys:

