# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import chardet
import re
import MySQLdb
import socket 
#socket.setdefaulttimeout(30) 
import threading
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException

import gzip
import cookielib

import time

from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

from lxml import etree
import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO
import pytesseract

def grabHref(url,localfile):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    fails = 0 
    while True:
        try:
            if fails >= 10:
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    #print type(html)
    page = etree.HTML(html.decode('utf-8'))
    hrefs = page.xpath(u"//div[@class='car-products']/div[@class='pro-list']")
    for href in hrefs:
        #print href.attrib['onclick'].split("'")[1]
        print href.attrib['onclick'][24:-2]
        get_qiugou_info(href.attrib['onclick'][24:-2])


def get_qiugou_info(myUrl):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(myUrl,headers=heads)
    html = ''
    fails = 0 
    while True:
        try:
            if fails >= 10:
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    if html != '':
        page = etree.HTML(html.decode('utf-8'))
        
        title = ''
        prices = ''
        brand = ''
        vehicle_series = ''
        vehicle_colors = ''
        addrs = ''
        registration_date = ''
        name = ''
        telephone = ''
        release_time = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        licenses = ''
        engine = ''
        effluent_standard = ''
        owner_readme = ''
        car_config = ''
        car_num = ''
        detail_addrs = ''
        m,n,q = 1,1,1
        if len(page.xpath(u"//div[@class='autotit']/strong/text()")) > 0:
            title = page.xpath(u"//div[@class='autotit']/strong/text()")[0]
        if len(page.xpath(u"//div[@class='autotit']/h2/text()")) > 0:
            car_config = page.xpath(u"//div[@class='autotit']/h2/text()")[0].replace('\n','')
        if len(page.xpath(u"//div[@id='right']/div[@class='car-quotation']/strong/text()")) > 0:
            prices = page.xpath(u"//div[@id='right']/div[@class='car-quotation']/strong/text()")[0]
        #print page.xpath(u"//div[@class='thecar1']/text()")[0]
        if len(page.xpath(u"//div[@class='thecar1']/text()")) > 0:
            addrs = page.xpath(u"//div[@class='thecar1']/text()")[0]
        if len(page.xpath(u"//li[@class='tc-der']/strong/text()")) > 0:
            telephone = page.xpath(u"//li[@class='tc-der']/strong/text()")[0]
        if len(page.xpath(u"/html/body/div[6]/span[1]/div/div[2]/div[2]/div/p[1]/text()")) > 0:
            name_addrs = page.xpath(u"/html/body/div[6]/span[1]/div/div[2]/div[2]/div/p[1]/text()")[0].split('|')
            name = name_addrs[0]
            for i in range(1,len(name_addrs)):
                detail_addrs = name_addrs[i]
        addrs = detail_addrs.replace(' ','') + u'-' + addrs
        if len(page.xpath(u"/html/body/div[6]/span[1]/div/div[2]/div[2]/div/p[2]/text()")) > 0:
            owner_readme = page.xpath(u"/html/body/div[6]/span[1]/div/div[2]/div[2]/div/p[2]/text()")[0]
        relevant_procedures = ''
        #if len(page.xpath(u"/html/body/div[6]/span[1]/div/div[4]/div[2]/div/ul/text()")) > 0:
        relevant_procedures = page.xpath(u"/html/body/div[6]/span[1]/div/div[4]/div[2]/div/ul/li")
        for relevant_procedure in relevant_procedures:
            car_config += u" | " + relevant_procedure.text.replace('\n','').replace(' ','')
        #print relevant_procedures
        print type(title),title
        print type(car_config),car_config
        print type(prices),prices
        print type(addrs),addrs
        print type(telephone),telephone
        print type(name),name
        print type(owner_readme),owner_readme

        release_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        if telephone != '':
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    info_src = "haoche51"
                    is_seller = u'商家'.encode('utf-8')
                    res = [str(title).encode('utf-8'),str(car_config).encode('utf-8'),str(name).encode('utf-8'),str(telephone).encode('utf-8'),str(addrs).encode('utf-8'),release_time,str(prices).encode('utf-8'),is_seller,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    if telephone.isdigit():
                        curs.execute("update sell_car_info set telephone_num='%s' where url='%s'" % (telephone,myUrl))
                    print 'The data is already in the database,begin to update the data...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)
        
#

#print "=================================================================================="
#get_qiugou_info('http://nj.haoche51.com/details/19629.html')

#print "=================================================================================="

#get_qiugou_info('http://nj.haoche51.com/details/19617.html')

#print "=================================================================================="

#get_qiugou_info('http://nj.haoche51.com/details/19609.html')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/5b201f0c7d1f1ba8')


def main():
    url="http://sh.haoche51.com/vehicle_list/p"
    localfile="Href.txt"
    for i in range(1,6):
        print "current page is %d" % i
        myUrl = url + str(i) + ".html"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
