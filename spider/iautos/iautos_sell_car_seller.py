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
        content = BeautifulSoup(html).find_all('a')
        pat = re.compile(r'http://www.iautos.cn/usedcar/\d+.html')
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
        licenses = ''
        car_infos = ''
        is_seller=u'个人'.encode('utf-8')
        license = u'首次上牌'.encode('utf-8')
        car_info = u'关键参数'.encode('utf-8')
        addr = u'地址'.encode('utf-8')
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        j = 1
        for div in soup.find_all('div',attrs={'class':'main'}):
            for div2 in div.find_all('div',attrs={'class':'cd-summary'}):
                for h2 in div2.find_all('h2',attrs={'class':'title clearfix'}):
                    for b in h2.find_all('b'):
                        title = str(b.get_text())
                    for span in h2.find_all('span'):
                        regex1 = re.compile(r'\d+-\d+-\d+')
                        if len(regex1.findall(str(span.get_text())))>0:
                            release_time = regex1.findall(str(span.get_text()))[0]
                for div3 in div2.find_all('div',attrs={'class':'summary-txt'}):
                    for div4 in div3.find_all('div',attrs={'class':'h136'}):
                        for span in div4.find_all('span',attrs={'class':'price'}):
                            prices = str(span.get_text())  
                        for dl in div4.find_all('dl'):
                            for dt in dl.find_all('dt'): 
                                if license in str(dt.get_text()):
                                    for dd in dl.find_all('dd'):
                                        licenses = str(dd.get_text())
                                elif car_info in str(dt.get_text()):
                                    for dd in dl.find_all('dd'):
                                        car_infos = str(dd.get_text())
                                elif addr in str(dt.get_text()):
                                    for dd in dl.find_all('dd'):
                                        addrs = str(dd.get_text())               
                    for div5 in div3.find_all('div',attrs={'class':'cd-call clearfix phone-show'}):
                        for p in div5.find_all('p',attrs={'class':'call-num'}):
                            telephone += str(p.get_text())+','
                        for div6 in div5.find_all('div',attrs={'class':'seller-name'}):
                            for span in div6.find_all('span'):
                                name += str(span.get_text()) + ' '
            for div7 in div.find_all('div',attrs={'class':'cd-details'}):
                for div8 in div7.find_all('div',attrs={'class':'postscript'}):
                    for p in div8.find_all('p'):
                        owner_readme += str(p.get_text()) + '\t'
        company_type = u'公司'.encode('utf-8')
        for div in soup.find_all('div',attrs={'class':'sidebar'}):
            for div2 in div.find_all('div',attrs={'class':'glb-dealer-info'}):
                for dl in div2.find_all('dl',attrs={'class':'clearfix'}):
                    for dt in dl.find_all('dt'):
                        if company_type in str(dt.get_text()):
                            is_seller=u'商家'.encode('utf-8')
                
        if telephone != '':
            print title,release_time,is_seller,name,telephone.rstrip(','),prices,licenses,car_infos,addrs,owner_readme,myUrl
            res = [title,release_time,is_seller,name,telephone.rstrip(','),prices,licenses,car_infos,addrs,owner_readme,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                is_seller = u'商家'.encode('utf-8')
                if not getrows:
                    car_config = licenses + " | " + car_infos
                    info_src = "iautos"
                    res = [title,car_config,name,telephone.rstrip(','),addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)   
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4471364.html')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4439887.html')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/3934131.html')



#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4399147.html')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4356447.html')

#print "=================================================================================="

#get_qiugou_info('http://www.iautos.cn/usedcar/4458823.html')


def main():
    url="http://so.iautos.cn/jiangsu/p"
    localfile="Href.txt"
    for i in range(1,5):
        print "current page is %d" % i
        myUrl = url + str(i)+'as1dsvepcatcpbnscac/'
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d" % i

if __name__=="__main__":
    main()
