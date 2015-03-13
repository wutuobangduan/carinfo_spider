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

import chardet

def grabHref(url,localfile):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
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
    if chardet.detect(html)['encoding'] == 'GB2312':
        soup = BeautifulSoup(html.decode('gbk').encode('utf-8'),'html.parser')
    else:
        soup = BeautifulSoup(html,'html.parser') 
    for ul in soup.find_all('ul',attrs={'id':'carList'}):
        for div in ul.find_all('div',attrs={'class':'sr_cl'}):
            for div2 in div.find_all('div',attrs={'class':'sr_carcn'}):
                for a in div2.find_all('a'):
                    print a.get('href')
                    myUrl = a.get('href')
            for div2 in div.find_all('div',attrs={'class':'icon_left'}):
                for span in div2.find_all('span'):
                    #print str(span.get_text())
                    release_time = str(span.get_text())
            get_qiugou_info(myUrl,release_time)


def get_qiugou_info(myUrl,release_time):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
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
        if chardet.detect(html)['encoding'] == 'GB2312':
            soup = BeautifulSoup(html.decode('gbk').encode('utf-8'),'html.parser')
        else:
            soup = BeautifulSoup(html,'html.parser')
        #print soup
        title = ''
        prices = ''
        vehicle_colors = ''
        addrs = u'江苏'.encode('utf-8')
        name = ''
        img_src = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        licenses = ''
        effluent_standard = ''
        telephone = ''
        car_config = ''
        owner_readme = ''
        contact = u'人'.encode('utf-8')
        addr = u'看车地点'.encode('utf-8')
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = None
        #try:
        #    browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8-linux-x86_64/bin/phantomjs') 
        #except WebDriverException,e:
        #    print e
        #if browser is not None:
        #    browser.get(myUrl)
        #    release_content = None
        #    try:
        #        release_content = browser.find_element_by_id('car_publish_time')
        #    except NoSuchElementException,e:
        #        print e
        #    if release_content is not None:
        #        if len(str(release_content.text).split('：'))>1:
        #            RG = re.compile(r'\d+-\d+-\d+')
        #            if len(RG.findall(str(release_content.text).split('：')[1]))>0:
        #                release_time = RG.findall(str(release_content.text).split('：')[1])[0]
        m,n,x = 1,1,1
        for div in soup.find_all('div',attrs={'class':'right-car-info'}):
            for div2 in div.find_all('div',attrs={'class':'car-title'}):
                #print div2
                for h1 in div2.find_all('h1'):
                    title = str(h1.get_text())
                
            for div2 in div.find_all('div',attrs={'id':'sell-ok'}):
                for div3 in div2.find_all('div',attrs={'class':'section-car-price'}):
                    for span in div3.find_all('span',attrs={'class':'price'}):
                        prices = str(span.get_text())
                for div3 in div2.find_all('div',attrs={'class':'section-km'}):
                    for span in div3.find_all('span'):
                        if m == 1:
                            car_config += u'行驶里程：'.encode('utf-8') + str(span.get_text())
                        elif m == 2:
                            regist_date = str(span.get_text()).replace('\n','').replace(' ','')
                            #car_config += u' | 上牌时间：'.encode('utf-8') + str(span.get_text()).replace('\n','')
                        m += 1
                for div3 in div2.find_all('div',attrs={'id':'contact-tel1'}):
                    for p in div3.find_all('p'):
                        telephone = str(p.get_text())
                for div3 in div2.find_all('div',attrs={'div':'section-contact'}):
                    name = str(div3.get_text()).split('：')[1]
        for div in soup.find_all('div',attrs={'id':'car-cheyuan'}):
            for div2 in div.find_all('div',attrs={'class':'car-detail-container'}):
                for p in div2.find_all('p'):
                    owner_readme = str(p.get_text())
        if len(title.split(']'))>1:
            addrs += title.split(']')[0][1:]
         
        car_config += u' | 上牌时间：'.encode('utf-8') + regist_date

        #req = Request(myUrl)
        #response = urlopen(req)
        #if response.info().getheader("ETag") is not None:
        #    id = response.info().getheader("ETag").split('/')[1][1:-1]
        #    number = myUrl.split('/')[-1].split('.')[0]
        #    test_data = {'callCount':1,'c0-scriptName':'CarViewAJAX','c0-methodName':'getCarInfoNew','xml':'true'}
#
#            test_data['c0-id']=str(id)
#            test_data['c0-param0']='number:' + str(number)
#
#            test_data_urlencode = urllib.urlencode(test_data)
#            requrl = "http://www.51auto.com/dwr/exec/CarViewAJAX.getCarInfoNew"
#
#            req = urllib2.Request(url = requrl,data =test_data_urlencode)
#
#            res_data = urllib2.urlopen(req)
#            res = res_data.read()
#            Regex = re.compile(r'\d+-\d+-\d+')
#            if len(Regex.findall(res))>0:
#                release_time = Regex.findall(res)[0]
        
        print title
        #print name       
        #print regist_date
        #print car_config
        print addrs
        print prices,telephone
        print release_time
        if telephone != '':
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    is_seller = u'商家'.encode('utf-8')
                    info_src = "51auto"
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
#get_qiugou_info('http://www.51auto.com/buycar/2489927.html')

#print "=================================================================================="



#print "=================================================================================="

#get_qiugou_info('http://www.51auto.com/buycar/2488833.html')

#print "=================================================================================="

#get_qiugou_info('http://www.51auto.com/buycar/2479037.html')


def main():
    url="http://www.51auto.com/jiangsu/pabmdcig3f/?page="
    localfile="Href.txt"
    for i in range(1,5):
        print "current page is %d" % i
        myUrl = url + str(i)
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d" % i

if __name__=="__main__":
    main()
