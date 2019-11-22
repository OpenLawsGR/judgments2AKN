# -*- coding: utf-8 -*-
"""
This crawler uses diavgeia API to download any type of dicision.

It performs a simple search (GET /search) and each http response is an
XML page. Please visit the following URL 

"https://diavgeia.gov.gr/api/help"

for instructions http messages, examples of client code, authentication,
decisions types (https://diavgeia.gov.gr/luminapi/opendata/types),
organizations (https://diavgeia.gov.gr/luminapi/opendata/organizations),
query parameters that you can use etc.

Examples for using this crawler are given below (fileType param must contain
greek characters!):
scrapy crawl clarity    (by default circulars (Εγκύκλιοι) published the
                        last 30 days)

scrapy crawl clarity -a fileType=Α.4
                     -a from_issue_date=2000-01-01
                     -a from_date=2000-01-01
                     -a org=50024   (all Legal Council of the State (ΝΣΚ)
                                     opinions since 2000)
                                    
                     
scrapy crawl clarity -a fileType=Α.3
                     -a from_issue_date=2000-01-01
                     -a from_date=2000-01-01    (all circulars of all
                                                 principles since 2000)
"""

import os
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from lxml import etree

ns = {'diav':'http://diavgeia.gov.gr/schema/v2'}
BASE_API_URL = r'https://diavgeia.gov.gr/luminapi/opendata/search.xml'

#some nodes are missing information about pdf files url
#specific pattern is being used to point to a specific file
#we construct it manually
BASE_ADA_URL = r'https://diavgeia.gov.gr/doc/'


def pages(number):
    if number % 500 > 0:
        return number / 500 + 1
    else:
        return number / 500


class claritySpider(scrapy.Spider):
    name = "clarity"
    allowed_domains = ["diavgeia.gov.gr"]
    #We use custom settings (it works!) to avoid being banned from diavgeia
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
        #print self.start_urls
        #pass
        
        #specific folders implementation based on our work
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
        #global STORE_DIR
        selector = Selector(response)
        #print selector
        selector.remove_namespaces()
        decisions = selector.xpath('//decisions').extract()[0]
        #print type(decisions)
        xml = etree.fromstring(decisions)  
        for elem in xml.getchildren():
            ada = elem.find('ada', namespaces = ns)
            #print ada
            #some documentUrl nodes are empty
            #documentUrl = elem.find('diav:documentUrl', namespaces = ns)
            if ada is not None:
                with open(self.STORE_DIR + ada.text + '.txt', 'w') as txt:
                    txt.write(etree.tostring(elem, pretty_print=True,
                                           encoding="UTF-8"))
                yield Request(BASE_ADA_URL+ada.text, callback = self.parsePDF,
                              meta={'ada' : ada.text})

    def parsePDF(self, response):
        #global STORE_DIR
        with open(self.STORE_DIR + response.meta['ada'] + '.pdf', 'wb') as pdf:
            pdf.write(response.body)

