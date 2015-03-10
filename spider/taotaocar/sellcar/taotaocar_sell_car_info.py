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
    for div in soup.find_all('div',attrs={'class':'buy_details'}):
        for li in div.find_all('li',attrs={'class':'buy_details_tiltle2'}):
            for a in li.find_all('a',attrs={'class':'blue_14'}):
                if '/car' in a.get('href'):
                    for span in li.find_all('span',attrs={'class':'orange_12'}):
                        if u'待售'.encode('utf-8') in str(span.get_text()):
                            myUrl = "http://jiangsu.taotaocar.com" + a.get('href')
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
        telephone = ''
        release_time = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        licenses = ''
        effluent_standard = ''
        owner_readme = ''
        m,n = 1,1
        for div in soup.find_all('div',attrs={'id':'buybox_left'}):
            for div2 in div.find_all('div',attrs={'class':'bugtitle'}):
                title = str(div2.get_text()).replace('\n','')
            for div2 in div.find_all('div',attrs={'class':'bugright_hang1_right'}):
                for div3 in div2.find_all('div',attrs={'class':'bugright_hang1_box1'}):
                    for li in div3.find_all('li'):
                        if m == 1:
                            for a in li.find_all('a'):
                                addrs = u'江苏'.encode('utf-8') + str(a.get_text()).replace(' ','')
                        elif m == 3:
                            if u'上牌时间'.encode('utf-8') in str(li.get_text()):
                                if len(str(li.get_text()).split('∶'))>1:
                                    registration_date = str(li.get_text()).split('∶')[1]
                        elif m == 4:
                            if u'排气量'.encode('utf-8') in str(li.get_text()):
                                if len(str(li.get_text()).split('∶'))>1:
                                    displacements = str(li.get_text()).split('∶')[1]
                        elif m == 5:
                            if u'行使里程'.encode('utf-8') in str(li.get_text()):
                                if len(str(li.get_text()).split('∶'))>1:
                                    trip_distances = str(li.get_text()).split('∶')[1]
                        elif m == 6:
                            if u'变速器'.encode('utf-8') in str(li.get_text()):
                                if len(str(li.get_text()).split('∶'))>1:
                                    transmissions = str(li.get_text()).split('∶')[1]
                        elif m == 7:
                            if u'发布时间'.encode('utf-8') in str(li.get_text()):
                                if len(str(li.get_text()).split('∶'))>1:
                                    release_time = str(li.get_text()).split('∶')[1]
                        elif m == 10:
                            if u'联系人'.encode('utf-8') in str(li.get_text()):
                                if len(str(li.get_text()).split('∶'))>1:
                                    name = str(li.get_text()).split('∶')[1]
                        elif m == 11:
                            for span in li.find_all('span',attrs={'class':'wanyuan'}):
                                prices = str(span.get_text())
                        
                        m += 1
        for div in soup.find_all('div',attrs={'style':'margin:4px;'}):
            telephone = str(div.get_text()).replace('    ','')
        for div in soup.find_all('div',attrs={'class':'lxnr385'}):
            for li in div.find_all('li',attrs={'class':'lxnr_mangen'}):
                if n == 1:
                    name = str(li.get_text())
                elif n == 2:
                    addrs += "-" + str(li.get_text())
                n += 1
        for div in soup.find_all('div',attrs={'class':'basic_bg'}):
            for div2 in div.find_all('div',attrs={'class':'basic_text'}):
                owner_readme = str(div2.get_text())
        print title, addrs,registration_date,displacements,trip_distances,transmissions,release_time,name,prices,telephone,myUrl
        if telephone != '':
            is_seller = u'个人'.encode('utf-8')
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    curs.execute("select id from sell_car_info where telephone_num like '%s' and info_src='taotaocar'" % ("%"+telephone+"%"))
                    get_img_srcs = curs.fetchall()
                    if not get_img_srcs:
                        is_seller = u'个人'.encode('utf-8')
                    else:
                        is_seller = u'商家'.encode('utf-8')
                    if telephone.startswith("400"):
                        is_seller = u'商家'.encode('utf-8')
                    car_config = u"上牌时间：".encode('utf-8') + registration_date + u" | 排气量：".encode('utf-8')  + displacements + u" | 行使里程：".encode('utf-8') + trip_distances + u" | 变速器：".encode('utf-8') + transmissions
                    info_src = "taotaocar"
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
#get_qiugou_info('http://jiangsu.taotaocar.com/car20152/2055633.html')

#print "=================================================================================="

#get_qiugou_info('http://jiangsu.taotaocar.com/car20153/2062993.html')

#print "=================================================================================="

#get_qiugou_info('http://jiangsu.taotaocar.com/car20152/2055662.html')

#print "=================================================================================="

#get_qiugou_info('http://jiangsu.taotaocar.com/car20153/2062919.html')


def main():
    url="http://jiangsu.taotaocar.com/buy.asp?usertype=2&page="
    localfile="Href.txt"
    for i in range(1,2):
        print "current page is %d" % i
        myUrl = url + str(i)
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
