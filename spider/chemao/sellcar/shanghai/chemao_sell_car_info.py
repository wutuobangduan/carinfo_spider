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
    for div in soup.find_all('div',attrs={'id':'carPicList'}):
        for div2 in div.find_all('div',attrs={'class':'list'}):
            for h2 in div2.find_all('h2'):
                for a in h2.find_all('a'):
                    myUrl = "http://www.chemao.com.cn/" + a.get('href')  
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
        engine = ''
        effluent_standard = ''
        owner_readme = ''
        car_config = ''
        car_num = ''
        m,n,q = 1,1,1
        for div in soup.find_all('div',attrs={'class':'detail_info fr'}):
            for div2 in div.find_all('div',attrs={'class':'detail-cont'}):
                for h2 in div2.find_all('h2'):
                    title = str(h2.get_text())
                for span in div2.find_all('span',attrs={'class':'numbers'}):
                    car_num = str(span.get_text()).split('：')[1]
                for p in div2.find_all('p',attrs={'class':'ins'}):
                    for span in p.find_all('span'):
                        if u'发布时间'.encode('utf-8') in str(span.get_text()):
                            release_time = str(span.get_text()).split('：')[1]
                for div3 in div2.find_all('div',attrs={'class':'detail_price_left '}):
                    for span in div3.find_all('span'):
                        prices = str(span.get_text())
                for div3 in div2.find_all('div',attrs={'class':'car_detail clear'}):
                    for div4 in div3.find_all('div',attrs={'class':'item'}):
                        for em in div4.find_all('em'):
                            if m == 1:
                                car_config += u"首次上牌：".encode('utf-8') + str(em.get_text())
                            elif m == 2:
                                car_config += u" | 行驶里程：".encode('utf-8') + str(em.get_text())
                            elif m == 3:
                                addrs += u"上海".encode('utf-8') + str(em.get_text())
                            elif m == 4:
                                car_config += u" | 排放标准：".encode('utf-8') + str(em.get_text())
                            m += 1
                for div3 in div2.find_all('div',attrs={'class':'detail-address clear'}):
                    for div4 in div3.find_all('div',attrs={'class':'address-text fl'}):
                        for p in div4.find_all('p'):
                            if n == 2:
                                name = str(p.get_text())
                            elif n == 3:
                                if p.get_text() is not None:
                                    addrs += "-" + str(p.get_text())
                            n += 1
        print title,release_time,prices,name
        print car_config,addrs
        print car_num
        get_tele_fail = 0
        tele_fail = 0
        try:
            browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8-linux-x86_64/bin/phantomjs',) 
            browser.implicitly_wait(20)
            browser.set_page_load_timeout(60)
        except WebDriverException,e:
            print e
        if browser is not None:
            while True:
                try:
                    if tele_fail > 10:
                        break
                    browser.get(myUrl)
                except:
                    tele_fail += 1
                    print "get page info failed ... ",tele_fail
                else:
                    break

            res = browser.find_element_by_id('show_chezhu_tel')
            
            t = res.find_element_by_xpath('a')
            t.click()
            time.sleep(5)
            result = browser.find_element_by_id('show_chezhu_tel')
            telephone = str(result.text)
            browser.quit()

        print telephone
        #cj = cookielib.CookieJar()
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #urllib2.install_opener(opener)
        #request = urllib2.Request(myUrl) 

        #response = opener.open(request)
       
        #car_id = int(car_num)
        #data = {'car_id':car_num}
        #data_urlencode = urllib.urlencode(data)
        #req = Request("http://www.chemao.com.cn/index.php?app=show&act=ajax_get_user_tel",data_urlencode)
        #response = urlopen(req)
        #print response.read()
        #headers = {
        #   'Accept':'application/json, text/javascript, */*; q=0.01',
        #   'Accept-Encoding':'gzip,deflate',
        #   'Accept-Language':'zh-CN,zh;q=0.8',
        #   'Connection':'keep-alive',
        #   'Content-Length':13,
        #   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           #'Cookie':'FC_ID=a2881a4f9e1cc93787a86efe2698a17b48af88b9; Hm_lvt_996dd03d99962cc3d2411df00b3a3e38=1426124181; Hm_lpvt_996dd03d99962cc3d2411df00b3a3e38=1426148721; uuid=41d0e2dab01e266f429c0e736e11ee27;',
        #   'Host':'www.chemao.com.cn',
        #   'Origin':'http://www.chemao.com.cn',
        #   'Referer':myUrl,
        #   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
        #   'X-Requested-With':'XMLHttpRequest',
        #}
        #headers['Cookie'] += " reredirectURL=%252Findex.php%253Fapp%253Dshow%2526id%253D" + myUrl.split('-')[-1].split('.')[0] 
        #print response.info().getheader("")
        #car_id = int(car_num)
        #data = {'car_id':car_id}
        #data_urlencode = urllib.urlencode(data)
        #print data_urlencode
        #opener.addheaders = [('Accept','application/json, text/javascript, */*; q=0.01'),('Accept-Encoding','gzip,deflate'),('Accept-Language','zh-CN,zh;q=0.8'),('Connection','keep-alive'),('Content-Length',13),('Content-Type','application/x-www-form-urlencoded; charset=UTF-8'),('Host','www.chemao.com.cn'),('Origin','http://www.chemao.com.cn'),('Referer',myUrl),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'),('X-Requested-With','XMLHttpRequest'),]
        #response = opener.open(r'http://www.chemao.com.cn/index.php?app=show&act=ajax_get_user_tel',data_urlencode)
        #reque = urllib2.Request(url = "http://www.chemao.com.cn/index.php?app=show&act=ajax_get_user_tel",data = data_urlencode,headers = headers)
        #res_data = urllib2.urlopen(reque)
        #print response.read()
        #print res_data.code
        #print res_data.getcode()
        #print res_data.geturl()
        #print res_data.info()
        #result = res_data.read()
        #print str(result).encode('utf-8')
        #print chardet.detect(result)
        #print response.info()

        if telephone != '' and telephone.isdigit():
            is_seller = u'商家'.encode('utf-8')
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    info_src = "chemao"
                    res = [title,car_config,name,telephone,addrs,release_time,prices,is_seller,info_src,myUrl]
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
#get_qiugou_info('http://www.renrenche.com/nj/car/bcee416733ed9ccc')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/44f4ad216c307e31')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/db87e9647de605e0')

#print "=================================================================================="

#get_qiugou_info('http://www.renrenche.com/nj/car/5b201f0c7d1f1ba8')


def main():
    url="http://www.chemao.com.cn/market-condition-rZcR7GDpGYSdugq1dhYLBEQ0N1E5XvNv9Y2QJJHqxqM.-page-"
    localfile="Href.txt"
    for i in range(1,6):
        print "current page is %d" % i
        myUrl = url + str(i) + ".html"
        grabHref(myUrl,localfile)
        
        print "current page is %d" % i

if __name__=="__main__":
    main()
