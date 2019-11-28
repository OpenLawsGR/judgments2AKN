# -*- coding: UTF-8 -*-
"""
This crawler extracts judgment decisions of the Greek Supreme Civil and
Criminal court "Areios Pagos". It's architecture is based on DOM of the
Pancyprian Bar Association website (see: www.cylaw.org)

Usage examples:
    scrapy crawl CyLaw (extract decisions published the current year) 
    scrapy crawl CyLaw -a year=2017 (extract decisions of a specific year)
    scrapy crawl CyLaw -a year=2015,2017 (extract decisions within a range of years)
"""
import os
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from datetime import datetime

# Current year to download files when no arguments are used
current_year = datetime.now().year
  
class CyLawSpider(scrapy.Spider):
    name = "CyLaw"
    allowed_domains = ["cylaw.org"]
    
    def __init__(self, year=str(current_year)+','+str(current_year),
                 *args, **kwargs):
        super(CyLawSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.STORE_DIR = r'data/areios_pagos/'
        try:
            year_from = int(year.split(',')[0]) 
            if len(year.split(',')) < 2 :
                year_to = int(year.split(',')[0])+1
            else:
                year_to = int(year.split(',')[1])+1
            
            for year in range(year_from, year_to):
                #print year_from
                #print year_to
                self.start_urls.append(
                    "http://www.cylaw.org/areiospagos/index_"+
                    str(year)+
                    ".html")

            if not os.path.exists(self.STORE_DIR):
                os.makedirs(self.STORE_DIR)
                
        except ValueError, NameError:
            print __doc__

    def parse(self, response):
        sel = Selector(response)
        #print(sel.xpath('//li/a/@href'))
        for url_string in sel.xpath('//li/a/@href').extract(): 
            request = Request("http://www.cylaw.org"+str(url_string),
                              callback = self.parse_objects)
            #print(request)
            yield request

    def parse_objects(self, response):
        sel = Selector(response)
        #print(response.body)
        title = sel.xpath('//title/text()').extract()
        #filename = title[0].encode('utf-8', 'replace')
        filename = title[0]
        filename = filename.replace(r'/', '_')
        #print(sel.xpath('//p/text()').extract())
        if not os.path.exists(self.STORE_DIR+response.url.split('/')[7]+'/'):
            os.makedirs(self.STORE_DIR+response.url.split('/')[7]+'/')

        with open(self.STORE_DIR+response.url.split('/')[7]+'/'+filename+'.txt', 'w') as f:
            for text in sel.xpath('//p/text()').extract():
                f.write(text.encode('utf-8')+'\n')
