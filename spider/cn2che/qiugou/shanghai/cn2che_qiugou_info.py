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
                        if '/buycar' in a.get('href'):
                            myUrl = "http://sh.cn2che.com" + a.get('href') 
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
        soup = BeautifulSoup(html)
        title = ''
        prices = ''
        brand = ''
        vehicle_series = ''
        vehicle_colors = ''
        addrs = ''
        registration_date = ''
        name = ''
        year = ''
        telephone = ''
        release_time = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        licenses = ''
        effluent_standard = ''
        owner_readme = ''
        car_usage = ''
        
        m,n,p,q = 1,1,1,1
        for div in soup.find_all('div',attrs={'id':'qg_info'}):
            for div2 in div.find_all('div',attrs={'class':'buycar_box'}):
                for h1 in div2.find_all('h1'):
                    title = str(h1.get_text())
                for div3 in div2.find_all('div',attrs={'class':'buycar_info'}):
                    for ul in div3.find_all('ul'):
                        for li in ul.find_all('li'):
                            if n == 2:
                                for dd in li.find_all('dd',attrs={'class':'info_k'}):
                                    for a in dd.find_all('a'):
                                        addrs = str(a.get_text())
                                    for b in dd.find_all('b'):
                                        prices = str(b.get_text())
                            elif n == 3:
                                for dd in li.find_all('dd',attrs={'class':'info_k'}):
                                    if m == 1:
                                        year = str(dd.get_text())
                                    elif m == 2:
                                        transmissions = str(dd.get_text())
                                    m += 1
                            elif n == 4:
                                for dd in li.find_all('dd',attrs={'class':'info_k'}):
                                    if p == 1:
                                        vehicle_colors = str(dd.get_text())
                                    elif p == 2:
                                        car_usage = str(dd.get_text())
                                    p += 1
                            elif n == 5:
                                for dd in li.find_all('dd',attrs={'class':'info_k cblack'}):
                                    release_time = str(dd.get_text())
                            elif n == 6:
                                for dd in li.find_all('dd'):
                                    owner_readme = str(dd.get_text())
                            elif n == 7:
                                for label in li.find_all('label',attrs={'id':'linkname'}):
                                    name = str(label.get_text())
                            elif n == 8:
                                for dd in li.find_all('dd',attrs={'class':'info_k'}):
                                    if q == 1:
                                        for b in dd.find_all('b'):
                                            telephone = str(b.get_text()) 
                                    elif q == 2:
                                        for b in dd.find_all('b'):
                                            if telephone == '':
                                                telephone = str(b.get_text())
                                            else:
                                                telephone += " | " + str(b.get_text())
                                    q += 1
                            elif n == 10:
                                for dd in li.find_all('dd'):
                                    if str(dd.get_text()) != '':
                                        addrs += '-' + str(dd.get_text())
                            n += 1
                                    
        print title,addrs,prices,year,transmissions,vehicle_colors,car_usage,release_time,owner_readme,name,telephone,myUrl
     
        if telephone != '':
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from qiu_gou_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    car_config = u"要求年限：".encode('utf-8') + year + u" | 变速器：".encode('utf-8') + transmissions + u" | 车身颜色：".encode('utf-8') + vehicle_colors + u" | 购车用途：".encode('utf-8') + car_usage + u" | 其他要求：".encode('utf-8') + owner_readme
                    info_src = "cn2che"
                    res = [title,name,telephone,release_time,addrs,prices,car_config,info_src,myUrl]
   
                    print "The data is not exists in the database..."
                    curs.execute("insert into qiu_gou_info(title,name,telephone,release_time,addrs,prices,other_requirements,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
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
    url="http://sh.cn2che.com/qiugou/bccpcmp"
    localfile="Href.txt"
    for i in range(1,2):
        print "current page is %d" % i
        myUrl = url + str(i) + "bcr21mplos2/"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
