# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class LegalSpidersPipeline(object):
    def process_item(self, item, spider):
        if not os.path.exists(item['store_dir']+
                              item['title'].split('_')[1]+'/'+
                              item['title'].split('_')[2]+'/'):
            os.makedirs(item['store_dir']+
                        item['title'].split('_')[1]+'/'+
                        item['title'].split('_')[2]+'/')

        with open(item['store_dir']+
                  item['title'].split('_')[1]+'/'+
                  item['title'].split('_')[2]+'/'+
                  item['title']+'.pdf', 'wb') as f:
            f.write(item['desc'])
        return item

