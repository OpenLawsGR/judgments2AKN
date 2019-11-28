# -*- coding: utf-8 -*-
"""
This crawler uses diavgeia API to download any type of dicision.

It performs a simple search (GET /search) and each http response is an
XML page (for more information on authentication, organizations, decisions
types etc. see link below) 

https://diavgeia.gov.gr/api/help"

Usage examples (fileType param must contain greek characters!):
    scrapy crawl clarity (by default circulars published in the last 30 days)

    scrapy crawl clarity -a fileType=Α.4
                         -a from_date=2000-01-01
                         -a org=50024 (all legal opinions of the Legal
                                     Council of State since 2000)
"""

import os
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from lxml import etree

# Declare namespace
ns = {'diav':'http://diavgeia.gov.gr/schema/v2'}
BASE_API_URL = r'https://diavgeia.gov.gr/luminapi/opendata/search.xml'

# A specific pattern is used to point to a pdf file 
BASE_ADA_URL = r'https://diavgeia.gov.gr/doc/'

# Get the number of pages that the crawler will visit
def pages(number):
    if number % 500 > 0:
        return number / 500 + 1
    else:
        return number / 500

class claritySpider(scrapy.Spider):
    name = "clarity"
    allowed_domains = ["diavgeia.gov.gr"]
    # We use custom settings to avoid being banned from diavgeia
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'+
                        'AppleWebKit/537.36(KHTML, like Gecko)'+
                        'Chrome/55.0.2883.95 Safari/537.36',
        'DOWNLOAD_DELAY' : 2.5,   
    }
    
    def __init__(self, fileType='Α.3', *args, **kwargs):
        super(claritySpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.reqUrl = BASE_API_URL + "?type="+ str(fileType)

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                self.reqUrl += "&" + str(key) + "=" + str(value)
                #print key, value

        self.reqUrl += "&size=500"
        #print self.reqUrl
        self.start_urls.append(self.reqUrl)
        
        # Declare specific folders for each type of file
        if str(fileType) == 'Α.3':
            self.STORE_DIR = r'data/clarity_egkyklioi/'
        elif str(fileType) == 'Α.4':
            self.STORE_DIR = r'data/nsk/'
        else:      
            self.STORE_DIR = r'data/diavgeia_other/'

        if not os.path.exists(self.STORE_DIR):
            os.makedirs(self.STORE_DIR)

        print __doc__

    def parse(self, response):
        selector = Selector(response)
        selector.remove_namespaces()
        results = int(selector.xpath('//info/total/text()').extract()[0])
        #print results
        num_pages = pages(results)
        #print num_pages
        for page in range(num_pages):
            request = Request(response.url + "&page=" + str(page),
                              callback = self.parseXML)
            yield request

    def parseXML(self, response):
        selector = Selector(response)
        #print selector
        selector.remove_namespaces()
        decisions = selector.xpath('//decisions').extract()[0]
        #print type(decisions)
        xml = etree.fromstring(decisions)  
        for elem in xml.getchildren():
            ada = elem.find('ada', namespaces = ns)
            #print ada
            #documentUrl = elem.find('diav:documentUrl', namespaces = ns)
            if ada is not None:
                with open(self.STORE_DIR + ada.text + '.txt', 'w') as txt:
                    txt.write(etree.tostring(elem, pretty_print=True,
                                           encoding="UTF-8"))
                yield Request(BASE_ADA_URL+ada.text, callback = self.parsePDF,
                              meta={'ada' : ada.text})

    def parsePDF(self, response):
        with open(self.STORE_DIR + response.meta['ada'] + '.pdf', 'wb') as pdf:
            pdf.write(response.body)
