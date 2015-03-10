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

class Qiugou58TcPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',host='127.0.0.1',db='scrapy',user='root',passwd='dp',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8')
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self.handle_error)
        return item
    def _conditional_insert(self,tx,item):
        if len(item['title'])>0 and len(item['img_src'])>0:
            tx.execute("select * from 58_qiugou_info_tmp where url = %s",(item['link'],))
            result = tx.fetchone()
            if result:
                log.msg("Item already stored in db: %s" % item,level=log.DEBUG)
            else:
                tx.execute("insert into 58_qiugou_info_tmp(title,tag,price,displacement,transmission,Travel_requirement,is_seller,name,img_src,url,release_time,addr) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['title'][0],item['tag'][0],item['price'][0],item['displacement'][0],item['transmission'][0],item['Travel_requirement'][0],len(item['is_seller']),len(item['name']),item['img_src'],item['link'],item['release_time'][0],item['addr'][0]))   
                log.msg("Item stored in db: %s" % item,level=log.DEBUG)
    def handle_error(self,e):
        log.err(e)
