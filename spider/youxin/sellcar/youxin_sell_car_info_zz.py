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
    hrefs = page.xpath(u"//div[@class='car-box clearfix']/div[@class='car-vtc vtc-border']/div[@class='vtc-info']/p/a")
    for href in hrefs:
        #print href.attrib['href']
        myUrl = 'http://www.xin.com' + href.attrib['href']
        print "====================================================================="
        print myUrl
        get_qiugou_info(myUrl)


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
        m,n,q = 1,1,1
        if len(page.xpath(u"/html/body/div[2]/div/div/div[1]/div[1]/div/h1/text()")) > 0:
            title = page.xpath(u"/html/body/div[2]/div/div/div[1]/div[1]/div/h1/text()")[0]
        car_config = u"上牌时间：" + page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/ul/li[1]/em/text()")[0] + u" | 行驶里程：" + page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/ul/li[2]/em/text()")[0] + u" | 排量：" + page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/ul/li[3]/em/text()")[0] + u" | 销售城市：" + page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/ul/li[4]/em/text()")[0]
        if len(page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/em/text()")) > 0:
            prices = page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/em/text()")[0]
        if len(page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/div[3]/p[2]/text()")) > 0:
            addrs = u'山东枣庄-' + page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/div[3]/p[2]/text()")[0]
        if len(page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/span")) > 0:
            telephone_attrs = page.xpath(u"/html/body/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/span")
            try:
                telephone =  telephone_attrs[0].attrib['tel']
            except:
                print "can not get telephone number..."
        if len(page.xpath(u"/html/body/div[2]/div/div/div[5]/p/text()")) > 0:
            name = page.xpath(u"/html/body/div[2]/div/div/div[5]/p/text()")[0]
        elif len(page.xpath(u"/html/body/div[2]/div/div/div[6]/p/text()")) > 0:
            name = page.xpath(u"/html/body/div[2]/div/div/div[6]/p/text()")[0]
        try:
            owner_readme = page.xpath(u"/html/body/div[2]/div/div/div[3]/div/div[1]/ul/li[1]/text()")[0] + u" | " + page.xpath(u"/html/body/div[2]/div/div/div[3]/div/div[1]/ul/li[2]/text()")[0] + u" | " + page.xpath(u"/html/body/div[2]/div/div/div[3]/div/div[1]/ul/li[3]/text()")[0] + u" | " + page.xpath(u"/html/body/div[2]/div/div/div[3]/div/div[1]/ul/li[4]/text()")[0] + u" | " +page.xpath(u"/html/body/div[2]/div/div/div[3]/div/div[1]/ul/li[5]/text()")[0]
        except:
            print "There is no owner readme info..."
        try:
            print page.xpath(u'/html/body/div[2]/div/div/div[3]/div/div[2]/ul/li[4]/text()')
            release_time = page.xpath(u'/html/body/div[2]/div/div/div[3]/div/div[2]/ul/li[4]/text()')[1]
        except:
            print "There is no release time...."
        print title
        print car_config
        print prices
        print addrs
        print telephone
        print name
        print owner_readme
        print release_time
        
        if telephone != '':
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    info_src = "xin"
                    is_seller = u'商家'.encode('utf-8')
                    res = [str(title).encode('utf-8'),str(car_config).encode('utf-8'),str(name).encode('utf-8'),str(telephone).encode('utf-8'),str(addrs).encode('utf-8'),release_time,str(prices).encode('utf-8'),is_seller,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database,begin to update the data...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)
       

def main():
    url="http://www.xin.com/zaozhuang/s/o2a2i"
    localfile="Href.txt"
    for i in range(1,11):
        print "current page is %d" % i
        myUrl = url + str(i) + "v2/"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
