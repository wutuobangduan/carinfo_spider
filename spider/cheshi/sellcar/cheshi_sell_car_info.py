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
    for div in soup.find_all('div',attrs={'class':'sc-link'}):
        for table in div.find_all('table',attrs={'class':'link-table link_table_info'}):
            for td in table.find_all('td',attrs={'class':'lk_tb_l'}):
                for dd in td.find_all('dd',attrs={'class':'l'}):
                    for a in dd.find_all('a',attrs={'class':'lk_tit_a'}):
                            myUrl = "http://2sc.cheshi.com" + a.get('href')
                            print myUrl
                            #get_qiugou_info(myUrl)


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
        
        
         
        #if telephone != '':
        #    is_seller = u'个人'.encode('utf-8')
        #    try:
        #        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
        #        curs = conn.cursor()
        #        conn.select_db('spider')
        #        curs.execute("select id from sell_car_info where url='%s'" % myUrl)
        #        getrows=curs.fetchall()
        #        if not getrows:
        #            curs.execute("select id from sell_car_info where telephone_num like '%s' and info_src='cn2che'" % ("%"+telephone+"%"))
        #            get_img_srcs = curs.fetchall()
        #            if not get_img_srcs:
        #                is_seller = u'个人'.encode('utf-8')
        #            else:
        #                is_seller = u'商家'.encode('utf-8')
        #            if telephone.startswith("400"):
        #                is_seller = u'商家'.encode('utf-8')
        #            car_config = brand + " | " + vehicle_series + " | " + registration_date + " | " + trip_distances 
        #            info_src = "cn2che"
        #            res = [title,car_config,name,telephone,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
        #            print "The data is not exists in the database..."
        #            curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
        #        else:
        #            print 'The data is already in the database,begin to update the data...'
        #        conn.commit()
        #        curs.close()
        #        conn.close()
        #    except MySQLdb.Error,e:
        ##        print "Error %d %s" % (e.args[0],e.args[1])
        #        sys.exit(1)


print "=================================================================================="
get_qiugou_info('http://2sc.cheshi.com/info/1543229.html')

print "=================================================================================="



#print "=================================================================================="

get_qiugou_info('http://2sc.cheshi.com/info/1543223.html')

#print "=================================================================================="

#get_qiugou_info('http://js.cn2che.com/sellcarinfo_1885748.html')


def main():
    url="http://2sc.cheshi.com/jiangsu/s3/p_"
    localfile="Href.txt"
    for i in range(1,6):
        print "current page is %d" % i
        myUrl = url + str(i) + "/?order=5"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

#if __name__=="__main__":
#    main()
