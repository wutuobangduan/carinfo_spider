# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request  
from scrapy.exceptions import DropItem  
import time  
import MySQLdb  
import MySQLdb.cursors
import socket
import select
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import errno


class DoubanProgramBookPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',host='127.0.0.1',db='scrapy',user='root',passwd='dp',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8')
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self.handle_error)
        return item
    def _conditional_insert(self,tx,item):
        if item.get('title'):
            for i in range(len(item["title"])):
                tx.execute("select * from douban_book where link = %s",(item['link'][i],))
                result = tx.fetchone()
                if result:
                    log.msg("Item already stored in db: %s" % item,level=log.INFO)
                else:
                    tx.execute("insert into douban_book(title,link) values(%s,%s)",(item['title'][i],item['link'][i]))   
                    log.msg("Item stored in db: %s" % item,level=log.INFO)
    def handle_error(self,e):
        log.err(e)
