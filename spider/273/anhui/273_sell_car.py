# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import socket 
#socket.setdefaulttimeout(30) 

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
        content = BeautifulSoup(html).find_all('a')
        pat = re.compile(r'http://\w+.273.cn/car/\d+.html')
        for item in content:
             href = pat.findall(str(item))
             if href:
                 #if href[0] not in dictionary:
                             #dictionary[href[0]] = ''
                             print "====================================================================================================================================="
                             print href[0]
                             get_qiugou_info(href[0])
                             print "======================================================================================================================================"

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
        soup = BeautifulSoup(html)
        title = ''
        prices = ''
        addrs = ''
        name = ''
        owner_readme = ''
        release_time = ''
        telephone = ''
        tele = u' 转 '.encode('utf-8')
        licenses = ''
        work_time = ''
        car_infos = ''
        trip_distance = ''
        emission_standard = ''
        j,k = 1,1
        for div in soup.find_all('div',attrs={'id':'detail_main_info'}):
            for h1 in div.find_all('h1'):
                for b in h1.find_all('b'):
                    title = str(b.get_text())
            for div2 in div.find_all('div',attrs={'class':'other clearfix'}):
                for div3 in div2.find_all('div',attrs={'class':'time'}):
                    for span in div3.find_all('span'):
                        if j == 1:
                            #print str(span.get_text())
                            regex1 = re.compile(r'\d+-\d+-\d+')
                            release_time = regex1.findall(str(span.get_text()))
                        j += 1
            for div4 in div.find_all('div',attrs={'class':'price_area'}):
                for p in div4.find_all('p',attrs={'class':'p1'}):
                    for strong in p.find_all('strong'):
                        prices = str(strong.get_text())
            for div5 in div.find_all('div',attrs={'class':'para'}):
                for li in div5.find_all('li'):
                    if k == 1:
                        for strong in li.find_all('strong'):
                            trip_distance = str(strong.get_text()) 
                    elif k == 2:
                        for strong in li.find_all('strong'):
                            licenses = str(strong.get_text())
                    elif k == 3:
                        for strong in li.find_all('strong'):
                            emission_standard = str(strong.get_text())
                    k += 1 
            for div6 in div.find_all('div',attrs={'class':'main_tel'}):
                for div7 in div6.find_all('div',attrs={'class':'work_time'}):
                    work_time = str(div7.get_text())
                for p in div6.find_all('p'):
                    for strong in p.find_all('strong'):
                        telephone += str(strong.get_text()) + tele 
        for div in soup.find_all('div',attrs={'class':'basic_info'}):
            for div2 in div.find_all('div',attrs={'class':'font_para'}):
                for ul in div2.find_all('ul'):
                    if len(str(ul.find('li').get_text()).split('：'))>1:
                        addrs = str(ul.find('li').get_text()).split('：')[1]
        for div in soup.find_all('div',attrs={'id':'trans_ad'}):
            for div2 in div.find_all('div',attrs={'class':'name'}):
                name = str(div2.get_text())
        for div in soup.find_all('div',attrs={'class':'con_rec'}):
            for div2 in div.find_all('div',attrs={'class':'sub_content'}):
                for p in div2.find_all('p'):
                    owner_readme += str(p.get_text())
        #print title,release_time[0],addrs,name,telephone.rstrip(tele),prices
        #print trip_distance,licenses,emission_standard,owner_readme
        is_seller = u'商家'.encode('utf-8')      
        if telephone != '':
            print title.strip(),is_seller,release_time[0],addrs,name,telephone.rstrip(tele),prices,trip_distance,licenses,emission_standard,owner_readme,myUrl
            #res = [title.strip(),is_seller,release_time[0],addrs,name,telephone.rstrip(tele),prices,trip_distance,licenses,emission_standard,owner_readme,myUrl]
            car_config = trip_distance + "|" + licenses + " | " + emission_standard
            info_src = "273"
            res = [title.strip(),car_config,name,telephone.rstrip(tele),addrs,release_time[0],prices,is_seller,owner_readme,info_src,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    print "The data is not exists in the database..."
                    #curs.execute("insert into 273_sell_car_info(title,is_seller,release_time,addrs,name,telephone,prices,trip_distance,licenses,emission_standard,owner_readme,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#get_qiugou_info('http://su.273.cn/car/15089399.html')

#print "=================================================================================="



def main():
    url="http://ah.273.cn/os1/?page="
    localfile="Href.txt"
    for i in range(1,5):
        print "current page is %d" % i
        myUrl = url + str(i)
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d" % i

if __name__=="__main__":
    main()
