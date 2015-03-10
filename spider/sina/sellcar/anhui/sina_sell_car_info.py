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
    for div in soup.find_all('div',attrs={'class':'user-car-search'}):
        for div2 in div.find_all('div',attrs={'class':'meet-condit'}):
            for div3 in div2.find_all('div',attrs={'class':'condi-box'}):
                for tr in div3.find_all('tr',attrs={'data-rel':'remove'}):
                    for div4 in tr.find_all('div',attrs={'class':'car-con left w200'}):
                        for p in div4.find_all('p',attrs={'class':'f14'}):
                            for a in p.find_all('a'):
                                if len(a.get('href').split('/'))>4 and len(a.get('href').split('/')[4].split('_'))>1:
                                    myUrl = "http://usedcar.auto.sina.com.cn/ucprice.php?action=getDetail&id=" + a.get('href').split('/')[4].split('_')[-1] + "&cid=" + a.get('href').split('/')[3]
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
        car_config = ''
        m,n,q = 1,1,1
          
        for div in soup.find_all('div',attrs={'class':'wrap main clearfix'}):
            for div2 in div.find_all('div',attrs={'class':'m_lf fL'}):
                for div3 in div2.find_all('div',attrs={'class':'m_lf_bot'}):
                    for h1 in div3.find_all('h1',attrs={'class':'sailname'}):
                        title = str(h1.get_text())
                    for div4 in div3.find_all('div',attrs={'class':'m_lf_bot_end_r fR'}):
                        for p in div4.find_all('p',attrs={'class':'t1'}):
                            for span in p.find_all('span'):
                                prices = str(span.get_text())
                        for p in div4.find_all('p',attrs={'class':'t2'}):
                            if len(str(p.get_text()).split('\n'))>5:
                                if len(str(p.get_text()).split('\n')[1].split('：'))>1:
                                    if u'安徽'.encode('utf-8') in str(p.get_text()).split('\n')[1].split('：')[1]:
                                        addrs = str(p.get_text()).split('\n')[1].split('：')[1]
                                if len(str(p.get_text()).split('\n')[3].split('：'))>1:
                                    if len(str(p.get_text()).split('\n')[3].split('：')[1].split('  '))>0:
                                        displacements = str(p.get_text()).split('\n')[3].split('：')[1].split('  ')[0]
                                if len(str(p.get_text()).split('\n')[3].split('：'))>1:
                                    transmissions = str(p.get_text()).split('\n')[3].split('：')[-1]
                                if len(str(p.get_text()).split('\n')[4].split('：'))>1:
                                    trip_distances = str(p.get_text()).split('\n')[4].split('：')[-1]
                                if len(str(p.get_text()).split('\n')[5].split('：'))>1:
                                    if len(str(p.get_text()).split('\n')[5].split('：')[1].split(' '))>0:
                                        registration_date = str(p.get_text()).split('\n')[5].split('：')[1].split(' ')[0]
                    for ul in div3.find_all('ul',attrs={'class':'carinfo clearfix'}):
                        for li in ul.find_all('li'):
                            if q == 1:
                                for span in li.find_all('span'):
                                    release_time = str(span.get_text())
                            q += 1
                    for p in div3.find_all('p',attrs={'class':'descption'}):
                        if n == 1:
                            if u'联系我时，请说是在新浪网二手车看到的，谢谢！'.encode('utf-8') in str(p.get_text()):
                                owner_readme = str(p.get_text())
                            else:
                                car_config = str(p.get_text())
                        elif n == 2:
                            if u'联系我时，请说是在新浪网二手车看到的，谢谢！'.encode('utf-8') in str(p.get_text()):
                                owner_readme = str(p.get_text())
                            else:
                                if addrs != '':
                                    addrs += '-' + str(p.get_text())
                        elif n == 3:
                            if addrs != '':
                                addrs += '-' + str(p.get_text())
                        n += 1
        for div in soup.find_all('div',attrs={'class':'said fR'}):
            for div2 in div.find_all('div',attrs={'class':'cnt'}):
                for strong in div2.find_all('strong'):
                    name = str(strong.get_text())
                for p in div2.find_all('p'):
                    if m == 2:
                        if len(str(p.get_text()).split('：'))>1:
                            telephone = str(p.get_text()).split('：')[-1]
                    m += 1
        print myUrl
        print title,release_time,prices,name,telephone,displacements,transmissions,trip_distances,registration_date,addrs,car_config,owner_readme
        if telephone != '' and addrs != '':
            is_seller = u'商家'.encode('utf-8')
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    car_configs = u"上牌时间：".encode('utf-8') + registration_date + u" | 排气量：".encode('utf-8')  + displacements + u" | 行使里程：".encode('utf-8') + trip_distances + u" | 变速器：".encode('utf-8') + transmissions + u" | 其他配置：".encode('utf-8') + car_config
                    info_src = "sina"
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
#get_qiugou_info('http://usedcar.auto.sina.com.cn/ucprice.php?action=getDetail&id=242769&cid=3091462873')

#print "=================================================================================="

#get_qiugou_info('http://usedcar.auto.sina.com.cn/ucprice.php?action=getDetail&id=237606&cid=3760709513')

#print "=================================================================================="

#get_qiugou_info('http://usedcar.auto.sina.com.cn/ucprice.php?action=getDetail&id=67352&cid=2986887060')

#print "=================================================================================="

#get_qiugou_info('http://usedcar.auto.sina.com.cn/ucprice.php?action=getDetail&id=242567&cid=1670621601')


def main():
    url="http://usedcar.auto.sina.com.cn/usedcar/price.php?prov=34&page="
    localfile="Href.txt"
    for i in range(1,11):
        print "current page is %d" % i
        myUrl = url + str(i) + "#ajContent"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
