# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import SelectorList
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.http import Request
from scrapy import log

from lufax.items import LufaxItem
from lufax.items import LoanRecord 

class WenyinESpider(CrawlSpider):
    name = 'wenyin-e'
    allowed_domains = ['lufax.com']
    start_urls = ['https://list.lufax.com/list/anyi?minMoney=&maxMoney=&minDays=&maxDays=&minRate=&maxRate=&mode=&trade=&isCx=&currentPage=1&orderType=&orderAsc=']
    rules = []

    def parse_directory_1(self, response):
        log.msg( 'Inline response URL: ', level=log.INFO)
        itemPattern = '<a href="(/list/productDetail\\?productId=\\d+)" target="_blank" class="list-btn">'
        log.msg( 'Pattern: '+itemPattern, level=log.INFO)
        reg_item = re.compile(itemPattern)
        #1) recgonize every detail url address
        for item in response.xpath('/html/body/div[3]/div/div[2]/ul/li' ):
            result = reg_item.match( item )
            if result != None :
                yield Request( 'https://list.lufax.com' + result.group(1), callback=self.parse_detail_1 )
        log.msg( 'NEXT PAGE -------------------  ', level=log.INFO)
        #2) recgonize next page url address
        nextPagePattern = 'data-val=(\\d+)>下一页<span'
        reg_nextPage = re.compile(nextPagePattern)
        log.msg(nextPagePattern, level=log.INFO)
        div_next = response.xpath('/html/body/div[3]/div/div[2]/div[4]')[0].extract()
        log.msg( div_next, log.INFO )
        nextPage = reg_nextPage.search( div_next )
        #response.css('body > div.main-wide-wrap > div > div.main-body > div.pagination.ui_complex_pagination').extract()[0] )
        if nextPage != None:
            log.msg( 'currentPage='+nextPage.group(1), level=log.INFO )
            yield Request('/list/anyi?minMoney=&maxMoney=&minDays=&maxDays=&minRate=&maxRate=&mode=&trade=&isCx=&orderType=&orderAsc=&currentPage='+ nextPage.group(1), callback=self.parse_directory_1)


    def parse_detail_1(self, response):
        items=[]
        item=LoanRecord()
        log.msg( 'fetch detail url:'+response.url )
        #response.xpath('/html/body/div[3]/div[2]/div[1]/div')
        titleSels = response.css('body > div.main-wrap > div.product-detail > div.product-detail-head > div')
        if titleSels != None and len(titleSels) > 0 :
            titleTxt = re.sub( "<[^>]*?>", "", titleSels[0].extract() )
            #titleTxt = re.sub( "[ \n]", "", titleTxt )
            titleTxt = ''.join( titleTxt.split() )
            print 'title:'+titleTxt
            item['title'] = titleTxt
        items.append( item )
        return items

    def parse(self, response):
        log.msg( 'response URL: '+response.url, level=log.INFO)
        #i = LufaxItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        records=[]
        #-----------------------------------------------------------------------------
        #1. check if it's a directory page ...
        dirPattern = 'currentPage=\\d+'
        regex_directory = re.compile( dirPattern )
        #2. check if it's a detail page ...
        detailPattern = "productDetail\\?productId=1207253&lufax_ref="
        regex_detail = re.compile( detailPattern )
        log.msg( 'Directory Pattern: ' + dirPattern, level=log.INFO)
        log.msg( 'Detail Pattern: ' + detailPattern, level=log.INFO)
        #3. execute
        if regex_directory.search( response.url ) != None :
            log.msg('To parse directory URL: '+response.url, level=log.INFO )
            #WenyinESpider.parse_directory( self, response )
            #self.parse_directory_1( response )
            itemPattern = '<a href="(/list/productDetail\\?productId=\\d+)" target="_blank" class="list-btn">'
            log.msg( 'Pattern: '+itemPattern, level=log.INFO)
            reg_item = re.compile(itemPattern)
            #1) recgonize every detail url address
            items = response.xpath('/html/body/div[3]/div/div[2]/ul/li')
            #log.msg( items.extract()[0], level=log.INFO )
            for item in items:
                #log.msg( item.extract(), level=log.INFO)
                result = reg_item.search( item.extract() )
                #log.msg(result, level=log.INFO)
                if result != None :
                    yield Request( 'https://list.lufax.com'+result.group(1), callback=self.parse_detail_1 )
        #2) recgonize next page url address
        nextPagePattern = r'data-identity="pages" data-val="(\d+)">'
        reg_nextPage = re.compile(nextPagePattern)
        log.msg(nextPagePattern, level=log.INFO)
        #div_next = response.xpath('/html/body/div[3]/div/div[2]/div[4]')[0].extract()
        div_nexts = response.css('body > div.main-wide-wrap > div > div.main-body > div.pagination.ui_complex_pagination > div > a.btns.btn_page.btn_small.next')
        if div_nexts != None and len(div_nexts)>0:
            div_next = div_nexts[0].extract()
            log.msg( div_next, log.INFO )
            nextPage = reg_nextPage.search( div_next )
            log.msg( nextPage.group(0), level=log.INFO )
            if nextPage != None :
                yield Request('https://list.lufax.com/list/anyi?minMoney=&maxMoney=&minDays=&maxDays=&minRate=&maxRate=&mode=&trade=&isCx=&orderType=&orderAsc=&currentPage='+ nextPage.group(1), callback=self.parse)
            elif regex_detail.search( 'https://list.lufax.com'+response.url ) != None :
                records=self.parse_detail_1( response )
            #log.msg( 'Before response URL: '+response.url, level=log.INFO)
            #log.msg( response.body )
            #self.parse_directory( response )
            #log.msg( 'After response URL: '+response.url, level=log.INFO)
        return


