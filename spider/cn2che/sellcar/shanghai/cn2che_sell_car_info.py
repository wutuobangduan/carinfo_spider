# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import socket 
#socket.setdefaulttimeout(30) 
import threading
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException

from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(html)
    for div in soup.find_all('div',attrs={'class':'allmain'}):
        for div2 in div.find_all('div',attrs={'class':'cheyuan'}):
            for ul in div2.find_all('ul'):
                for dt in ul.find_all('dt'):
                    for a in dt.find_all('a'):
                        if 'cn2che.com' in a.get('href'):
                            print a.get('href')
                            get_qiugou_info(a.get('href'))


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
        soup = BeautifulSoup(html)
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
        effluent_standard = ''
        owner_readme = ''
        
        for div in soup.find_all('div',attrs={'class':'leftmain'}):
            for div2 in div.find_all('div',attrs={'class':'Detailed'}):
                for h1 in div2.find_all('h1',attrs={'id':'title'}):
                    title = str(h1.get_text())
                for dl in div2.find_all('dl'):
                    for dd in dl.find_all('dd'):
                        for ol in dd.find_all('ol'):
                            for strong in ol.find_all('strong',attrs={'id':'price'}):
                                prices = str(strong.get_text())
                            for li in ol.find_all('li'):
                                if u'车辆品牌'.encode('utf-8') in str(li.get_text()):
                                    if len(str(li.get_text()).split('：'))>1:
                                        brand = str(li.get_text()).split('：')[1]
                                if u'车辆系列'.encode('utf-8') in str(li.get_text()):
                                    if len(str(li.get_text()).split('：'))>1:
                                        vehicle_series = str(li.get_text()).split('：')[1]
                                if u'上牌时间'.encode('utf-8') in str(li.get_text()):
                                    if len(str(li.get_text()).split('：'))>1:
                                        registration_date = str(li.get_text()).split('：')[1]
                                if u'行驶里程'.encode('utf-8') in str(li.get_text()):
                                    if len(str(li.get_text()).split('：'))>1:
                                        trip_distances = str(li.get_text()).split('：')[1]
                                if u'交易地区'.encode('utf-8') in str(li.get_text()):
                                    if len(str(li.get_text()).split('：'))>1:
                                        addrs = str(li.get_text()).split('：')[1].replace('-','')
                                if u'更新时间'.encode('utf-8') in str(li.get_text()):
                                    if len(str(li.get_text()).split('：'))>1:
                                        release_time = str(li.get_text()).split('：')[1].replace('-','')
                                
                        for dl in dd.find_all('dl'):
                            for dd in dl.find_all('dd',attrs={'id':'address'}):
                                addrs += '-' + str(dd.get_text())        
                        #for dl in dd.find_all('dl',attrs={'class':'contact'}):
                        #    for b in dl.find_all('b',attrs={'id':'phone'}):
                        #        telephone = str(b.get_text())        
            for div3 in div.find_all('div',attrs={'class':'parameters'}):
                for span in div3.find_all('span',attrs={'class':'describe'}):
                    owner_readme = str(span.get_text())
        for div in soup.find_all('div',attrs={'class':'rightmain'}):
            for div2 in div.find_all('div',attrs={'id':'shopinfo'}):
                for div3 in div2.find_all('div',attrs={'class':'inwords'}):
                    for i in div3.find_all('i',attrs={'id':'link'}):
                        name = str(i.get_text())
                    for dd in div3.find_all('dd',attrs={'id':'telphone'}):
                        telephone = str(dd.get_text())                   
        
        print title,prices,brand,vehicle_series,registration_date,trip_distances,addrs,release_time,name,telephone,owner_readme,myUrl
     
        if telephone != '':
            is_seller = u'个人'.encode('utf-8')
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    curs.execute("select id from sell_car_info where telephone_num like '%s' and info_src='cn2che'" % ("%"+telephone+"%"))
                    get_img_srcs = curs.fetchall()
                    if not get_img_srcs:
                        is_seller = u'个人'.encode('utf-8')
                    else:
                        is_seller = u'商家'.encode('utf-8')
                    if telephone.startswith("400"):
                        is_seller = u'商家'.encode('utf-8')
                    car_config = brand + " | " + vehicle_series + " | " + registration_date + " | " + trip_distances 
                    info_src = "cn2che"
                    res = [title,car_config,name,telephone,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database,begin to update the data...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)


#print "=================================================================================="
#get_qiugou_info('http://js.cn2che.com/sellcarinfo_1882035.html')

#print "=================================================================================="



#print "=================================================================================="

#get_qiugou_info('http://js.cn2che.com/sellcarinfo_1884039.html')

#print "=================================================================================="

#get_qiugou_info('http://js.cn2che.com/sellcarinfo_1885748.html')


def main():
    url="http://sh.cn2che.com/buycar/cccpcmp"
    localfile="Href.txt"
    for i in range(1,5):
        print "current page is %d" % i
        myUrl = url + str(i) + "bcr21m1plos2/"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
