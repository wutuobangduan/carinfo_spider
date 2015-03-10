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
from lxml import etree

def grabHref(url,localfile):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    fails = 0 
    html = ''
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
        try:
            file_object = open("html.txt","w")
            file_object.writelines(html) 
        finally:
            file_object.close()
        try:
            fp = open("html.txt","r")
            alllines = fp.readlines()
        finally:
            fp.close()
        for eachline in alllines:
            #if '<p class="pp">' in eachline:
            #    print eachline.decode('gb2312').encode('utf-8')
            if '<dd><span class="bt"><a target="_blank" href="/carfile' in eachline:
                if len(eachline.split('"'))>5:
                    myUrl = "http://www.zg2sc.cn" + eachline.split('"')[5]
                    print myUrl
                    get_qiugou_info(myUrl)
        if os.path.exists("html.txt"):
            os.remove("html.txt")


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
        insurance_date = ''
        inspection_date = ''
        effluent_standard = ''
        owner_readme = ''
        m,n = 1,1
        for div in soup.find_all('div',attrs={'class':'carfile_xinxi'}):
            for div2 in div.find_all('div',attrs={'class':'carfile_xinxi_title'}):
                for span in div2.find_all('span'):
                    for em in span.find_all('em'):
                        title = str(em.get_text())
                    for strong in span.find_all('strong'):
                        prices = str(strong.get_text())
            for div2 in div.find_all('div',attrs={'class':'carfile_xinxi_text_right'}):
                for dl in div2.find_all('dl'):
                    for dd in dl.find_all('dd'):
                        if m == 1:
                            registration_date = str(dd.get_text())
                        elif m == 2:
                            release_time = str(dd.get_text())
                        elif m == 3:
                            trip_distances = str(dd.get_text())
                        elif m == 4:
                            vehicle_colors = str(dd.get_text())
                        elif m == 6:
                            effluent_standard = str(dd.get_text())
                        elif m == 7:
                            insurance_date = str(dd.get_text())
                        elif m == 8:
                            inspection_date = str(dd.get_text()) 
                        m += 1
                for div3 in div2.find_all('div',attrs={'id':'div_tel2'}):
                    if len(str(div3.get_text()).split(':'))>1:
                        name = str(div3.get_text()).split(':')[0]             
                        telephone = str(div3.get_text()).split(':')[1]
        for div in soup.find_all('div',attrs={'id':'xq_01'}):
            for div2 in soup.find_all('div',attrs={'class':'carfile_pz_text_wz'}):
                owner_readme += str(div2.get_text())
        print title,prices,registration_date,release_time,trip_distances,vehicle_colors,effluent_standard,insurance_date,inspection_date,name,telephone,owner_readme,myUrl
        if len(title.split('['))>1:
            if len(title.split('[')[1].split(']'))>0:
                if u'合肥'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'芜湖'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'蚌埠'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'淮南'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'淮北'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'马鞍山'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'铜陵'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'安庆'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'黄山'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'滁州'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'阜阳'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'宿州'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'巢湖'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'六安'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'亳州'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'池州'.encode('utf-8') in title.split('[')[1].split(']')[0] or u'宣城'.encode('utf-8') in title.split('[')[1].split(']')[0]:
                    addrs = u"安徽".encode('utf-8') + title.split('[')[1].split(']')[0]
        if telephone != '' and addrs != '':
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    is_seller = u'商家'.encode('utf-8')
                    car_config = u'上牌时间：'.encode('utf-8') + registration_date + u" | 表显里程：".encode('utf-8') + trip_distances + u" | 车身颜色：".encode('utf-8') + vehicle_colors + u" | 排放标准：".encode('utf-8') + effluent_standard + u" | 保险到期：".encode('utf-8') + insurance_date + u" | 年审到期：".encode('utf-8') + inspection_date
                    info_src = "zg2sc"
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
#get_qiugou_info('http://www.zg2sc.cn/carfile/3079/3079888.html')

#print "=================================================================================="

#get_qiugou_info('http://www.zg2sc.cn/carfile/3079/3079900.html')

#print "=================================================================================="

#get_qiugou_info('http://www.zg2sc.cn/carfile/3079/3079869.html')

#print "=================================================================================="

#get_qiugou_info('http://www.zg2sc.cn/carfile/3079/3079701.html')


def main():
    url="http://www.zg2sc.cn/usedcar/p0a0t0c0y2r0f0d0s0/?pageNo="
    localfile="Href.txt"
    for i in range(1,5):
        print "current page is %d" % i
        myUrl = url + str(i) + "&sr=null&prov=%B0%B2%BB%D5"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
