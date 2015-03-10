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
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

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
        for div in BeautifulSoup(html).find_all('div',attrs={'class':'carlist_allcar'}):
            for h3 in div.find_all('h3',attrs={'class':'listcar_title'}):
                for a in h3.find_all('a'):
                    print "====================================================================================================================================="
                    ans = 'http://www.hx2car.com' + a.get('href')
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
        soup = BeautifulSoup(html)
        title = ''
        prices = ''
        addrs = u'江苏'.encode('utf-8')
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
        is_seller=u'个人'.encode('utf-8')
        company_type = u'公司'.encode('utf-8')
        dollar = u'￥'.encode('utf-8')
        j,k,m = 1,1,1
        for div in soup.find_all('div',attrs={'class':'car_infor'}):
            for div2 in div.find_all('div',attrs={'class':'infor_r'}):
                for h1 in div2.find_all('h1',attrs={'class':'carname'}):
                    title = str(h1.get_text()).strip()
                for p in div2.find_all('p',attrs={'class':'carprice'}):
                    for span in p.find_all('span'):
                        if m == 1:
                            prices = dollar + str(span.get_text())
                        m += 1
                for p in div2.find_all('p',attrs={'class':'cartel '}):
                    for span in p.find_all('span',attrs={'class':'context_car'}):
                        telephone = str(span.get_text())
                for p in div2.find_all('p',attrs={'class':'carplace'}):
                    for span in p.find_all('span',attrs={'class':'context_name'}):
                        for b in span.find_all('b'):
                             name = str(b.get_text())
                    else:
                        for span in p.find_all('span'):
                            for b in span.find_all('b'):
                                if u'江苏'.encode('utf-8') in str(b.get_text()):
                                    addrs = str(b.get_text())
                                else:
                                    addrs += str(b.get_text())
                for div3 in div2.find_all('div',attrs={'class':'car_message'}):
                    for ul in div3.find_all('ul',attrs={'class':'message_title'}):
                        for span in ul.find_all('span'):
                            if len(str(span.get_text()).split('：'))>1:
                                release_time = str(span.get_text()).split('：')[1]
        for div in soup.find_all('div',attrs={'class':'detail_r'}):
            for div2 in div.find_all('div',attrs={'class':'carowner'}):
                for p in div2.find_all('p',attrs={'class':'owner_area'}):
                    if company_type in str(p.get_text()):
                        is_seller = u'商户'.encode('utf-8')         
        for div in soup.find_all('div',attrs={'class':'car_introduce'}):
            for span in div.find_all('span'):
                owner_readme = str(span.get_text())
        #print title,telephone,name,addrs,prices,release_time,is_seller,owner_readme,myUrl
               
        if telephone != '':
            print title,telephone,name,addrs,prices,release_time,is_seller,owner_readme,myUrl
            #res = [title,telephone,name,addrs,prices,release_time,is_seller,owner_readme,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from huaxia_sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                is_seller = u'商家'.encode('utf-8')
                if not getrows:
                    res = [title,telephone,name,addrs,prices,release_time,is_seller,owner_readme,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into huaxia_sell_car_info(title,telephone,name,addrs,prices,release_time,is_seller,owner_readme,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                    curs.execute("update huaxia_sell_car_info set prices ='%s' where url ='%s'" % (prices,myUrl))
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://www.hx2car.com/details/141427181')

#print "=================================================================================="

#get_qiugou_info('http://www.hx2car.com/details/140451640')

#print "=================================================================================="

#get_qiugou_info('http://www.hx2car.com/details/141438759')



#print "=================================================================================="

#get_qiugou_info('http://www.hx2car.com/details/141127298')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4356447.html')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4458823.html')


def main():
    url = "http://www.hx2car.com/car/search.htm?carFlag=stores&more=l320000dzsejtyckbmg&currPage="
    localfile="Href.txt"
    for i in range(1,30):
        print "current page is %d" % i
        myUrl = url + str(i) + '#now_search_result'
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d" % i

if __name__=="__main__":
    main()
