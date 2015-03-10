# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
import time
import socket 
#socket.setdefaulttimeout(30) 
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import httplib
import html5lib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup,BeautifulStoneSoup

def grabHref(url,localfile):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    html = None
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
    if html is not None:
        #dictionary = {}
        #print BeautifulSoup(html)
        for div in BeautifulSoup(html).find_all('div',attrs={'class':'card-box clearfix car-wrap '}):
            for div2 in div.find_all('div',attrs={'class':'carsItem carItem'}):
                for a in div2.find_all('a',attrs={'class':'car-link'}):
                    print "====================================================================================================================================="
                    ans = 'http://www.souche.com' + a.get('href')
                    print ans
                    get_qiugou_info(ans)
                    print "====================================================================================================================================="


def get_qiugou_info(myUrl):
    #proxy = {'http':'http://202.106.16.36:3128'}
    #proxy_support = urllib2.ProxyHandler(proxy)
    #opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    #urllib2.install_opener(opener)  
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
        soup = BeautifulSoup(html,"html.parser")
        title = ''
        prices = ''
        addrs = u'江苏'.encode('utf-8')
        name = ''
        owner_readme = ''
        release_time = ''
        telephone = ''
        tele = u' 转 '.encode('utf-8')
        licenses = ''
        new_car_prices = ''
        trip_distance = ''
        emission_standard = ''
        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        j,k = 1,1
        for div in soup.find_all('div',attrs={'class':'shop-head'}):
            for div2 in div.find_all('div',attrs={'class':'shop-info'}):
                for a in div2.find_all('a',attrs={'class':'shop-name'}):
                   name = str(a.get_text()).replace('\n','').replace('\t','').replace(' ','')
        for div in soup.find_all('div',attrs={'class':'main-top'}):
            for h1 in div.find_all('h1'):
                title = str(h1.get_text()).replace('\n','')
            for div2 in div.find_all('div',attrs={'class':'detail-price clearfix'}):
                for div3 in div2.find_all('div',attrs={'class':'detail_price_left clearfix'}):
                    prices = str(div3.get_text()).replace('\n','')
                for div4 in div2.find_all('div',attrs={'class':'detail_price_right '}):
                    for label in div4.find_all('label',attrs={'class':'new'}):
                        if len(str(label.get_text()).split('：'))>1:
                            new_car_prices = str(label.get_text()).split('：')[1]
            for div4 in div.find_all('div',attrs={'class':'car_detail clearfix'}):
                for div5 in div4.find_all('div',attrs={'class':'item'}):
                    if j == 1:
                        for strong in div5.find_all('strong'):
                            licenses = str(strong.get_text())
                    elif j == 2:
                        for strong in div5.find_all('strong'):
                            trip_distance = str(strong.get_text())
                    elif j == 3:
                        for strong in div5.find_all('strong'):
                            if u'江苏'.encode('utf-8') in str(strong.get_text()):
                                addrs = str(strong.get_text())
                            else:
                                addrs += str(strong.get_text())
                    elif j == 4:
                        for strong in div5.find_all('strong'):
                            emission_standard = str(strong.get_text())   
                    j += 1
            for div6 in div.find_all('div',attrs={'class':'detail-button clearfix'}):
                for div7 in div6.find_all('div',attrs={'class':'phone-num'}):
                    telephone = str(div7.get_text())
        for div in soup.find_all('div',attrs={'class':'car-act clearfix'}):
            for div2 in soup.find_all('div',attrs={'class':'push-time'}):      
                release_time = str(div2.get_text())
        if telephone != '':
            print title,name,release_time,prices,new_car_prices,telephone,addrs,licenses,trip_distance,emission_standard,myUrl
            #res = [title,name,release_time,prices,new_car_prices,telephone,addrs,licenses,trip_distance,emission_standard,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    curs.execute("select id from sell_car_info where telephone_num='%s'" % telephone)
                    get_telephones = curs.fetchall()
                    if not get_telephones:
                        is_seller = u'个人'.encode('utf-8')
                    else:
                        is_seller = u'商家'.encode('utf-8')
                    if telephone.startswith("400"):
                        is_seller = u'商家'.encode('utf-8')
                    car_config = trip_distance + " | " + licenses + " | " + emission_standard
                    info_src = "dasouche"
                    res = [title,car_config,name,telephone,addrs,release_time,prices,is_seller,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=c9c4861d-4fdf-49eb-9519-88065a628363')

print "=================================================================================="

#get_qiugou_info('http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=dlqWu0k823')

#print "=================================================================================="

#get_qiugou_info('http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=ngiiHPnJEK')

#print "=================================================================================="

#get_qiugou_info('http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=fqBLaUcU7Q')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4356447.html')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4458823.html')


def main():
    url="http://www.souche.com/jiangsu/list-mx2014-stzaishou-pg"
    localfile="Href.txt"
    for i in range(1,10):
        print "current page is %d" % i
        myUrl = url + str(i)
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d" % i

if __name__=="__main__":
    main()
