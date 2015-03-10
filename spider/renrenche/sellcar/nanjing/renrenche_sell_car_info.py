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
    for a in soup.find_all('a',attrs={'class':'thumbnail'}):
        myUrl = "http://www.renrenche.com" + a.get('href')
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
        soup = BeautifulSoup(html,'html.parser')
        title = ''
        prices = ''
        brand = ''
        vehicle_series = ''
        vehicle_colors = ''
        addrs = u'江苏南京'.encode('utf-8')
        registration_date = ''
        name = ''
        telephone = '4006936019'
        release_time = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        licenses = ''
        engine = ''
        effluent_standard = ''
        owner_readme = ''
        car_config = ''
        m,n,q = 1,1,1
        for div in soup.find_all('div',attrs={'class':'detail-wrapper'}):
            for div2 in soup.find_all('div',attrs={'id':'basic'}):
                for div3 in div2.find_all('div',attrs={'class':'container detail-title-wrapper'}):
                    for h1 in div3.find_all('h1',attrs={'class':'span19'}):
                        title = str(h1.get_text())  
                for div3 in div2.find_all('div',attrs={'class':'detail-box-wrapper'}):
                    for div4 in div3.find_all('div',attrs={'class':'detail-box-bg'}):
                        for p in div4.find_all('p',attrs={'class':'owner-info'}):
                            for strong in p.find_all('strong'):
                                name = str(strong.get_text())
                        for div5 in div4.find_all('div',attrs={'class':'detail-box'}):
                            for p in div5.find_all('p',attrs={'class':'box-price'}):
                                prices = str(p.get_text())
        for ul in soup.find_all('ul',attrs={'class':'row-fluid list-unstyled box-list-primary'}):
            for li in ul.find_all('li'):
                for strong in li.find_all('strong'):
                    car_config += str(strong.get_text()) + " | "
        for div in soup.find_all('div',attrs={'class':'text-block bottom-left'}):
            for h3 in div.find_all('h3'):
                if len(str(h3.get_text()).split('\n'))>1:
                    if len(str(h3.get_text()).split('\n')[1].split('：'))>1:
                        addrs += '-' + str(h3.get_text()).split('\n')[1].split('：')[1]
            for p in div.find_all('p'):
                owner_readme = str(p.get_text())
        for div in soup.find_all('div',attrs={'class':'container detail-parameter-wrapper'}):
            for div2 in div.find_all('div',attrs={'class':'table-responsive'}):
                if n == 3:
                    for tbody in div2.find_all('tbody'):
                        for td in tbody.find_all('td',attrs={'class':'text-center'}):
                            if q == 2:
                                engine = str(td.get_text())
                            elif q == 3:
                                transmissions = str(td.get_text())
                            q += 1
                            
                n += 1
            
        for div in soup.find_all('div',attrs={'class':'container detail-report-card'}):
            for p in div.find_all('p',attrs={'class':'row-fluid'}):
                for span in p.find_all('span',attrs={'class':'span4 offset6'}):
                    if len(str(span.get_text()).split('：'))>1:
                        release_time = str(span.get_text()).split('：')[1]
        print title,name,prices,car_config.rstrip(" |"),telephone,addrs,owner_readme,registration_date
        print engine,transmissions,release_time
        if telephone != '':
            is_seller = u'商家'.encode('utf-8')
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    car_configs = u"发动机：".encode('utf-8') + engine + u" | 变速器：".encode('utf-8') + transmissions + u" | 其他配置：".encode('utf-8') + car_config
                    info_src = "renrenche"
                    res = [title,car_configs,name,telephone,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
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
#get_qiugou_info('http://www.renrenche.com/nj/car/bcee416733ed9ccc')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/44f4ad216c307e31')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/db87e9647de605e0')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/5b201f0c7d1f1ba8')


def main():
    url="http://www.renrenche.com/nj/ershouche/p"
    localfile="Href.txt"
    for i in range(1,6):
        print "current page is %d" % i
        myUrl = url + str(i)
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
