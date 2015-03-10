# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
import time
import socket 
socket.setdefaulttimeout(30) 
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
    try:
        html = urllib2.urlopen(req).read()
    except httplib.IncompleteRead, e:
        print e.partial
    if html is not None:
        #dictionary = {}
        content = BeautifulSoup(html).find_all('a')
        pat = re.compile(r'http://huaian.ganji.com/ershouche/\d+x.htm')
        for item in content:
             href = pat.findall(str(item))
             if href:
                 #if href[0] not in dictionary:
                     if len(str(href[0]).split('/'))>2 and len(str(href[0]).split('/')[2].split('.'))>0:
                         if str(href[0]).split('/')[2].split('.')[0] == 'huaian':
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
    try:
        html = urllib2.urlopen(req).read()
    except urllib2.HTTPError,e:
        print e.code
        print e.reason
        print e.geturl()
    if html != '':
        soup = BeautifulSoup(html)
        title = ''
        prices = ''
        addrs = u'淮安'.encode('utf-8')
        name = ''
        brand_model = ''
        release_time = ''
        telephone = ''
        trip_distance = ''
        licenses = ''
 
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        j = 1
        for h1 in soup.find_all('h1',attrs={'class':'title-name'}):
            title = str(h1.get_text()).replace('\n','')
        for ul in soup.find_all('ul',attrs={'class':'title-info-l clearfix'}):
            for i in ul.find_all('i',attrs={'class':'f10 pr-5'}):
                release_time = str(i.get_text())
        for div in soup.find_all('div',attrs={'class':'basic-info'}):
            for ul in div.find_all('ul',attrs={'class':'veh-plbit-ul clearfix'}):
                for li in ul.find_all('li'):
                    for i in li.find_all('i',attrs={'class':'comNum ft30'}):
                        prices = str(i.get_text())
                    for span in li.find_all('span',attrs={'class':'fc-999 dettips ft-12'}):
                        prices += str(span.get_text()).replace('\n','').replace(' ','')
                    
                    if j == 2:
                        if len(str(li.get_text()).replace('\n','').replace(' ','').split('：'))>1:
                            brand_model = str(li.get_text()).replace('\n','').replace(' ','').split('：')[1]
                    elif j == 3:
                        if len(str(li.get_text()).replace('\n','').replace(' ','').split('：'))>1:
                            trip_distance = str(li.get_text()).replace('\n','').replace(' ','').split('：')[1]
                    elif j == 4:
                        if len(str(li.get_text()).replace('\n','').replace(' ','').split('：'))>1:
                            licenses = str(li.get_text()).replace('\n','').replace(' ','').split('：')[1]
                     
                    j += 1
            for span in div.find_all('span',attrs={'name':'img-phone','class':'telephone'}):
                telephone += str(span.get_text()).replace('\n','').replace(' ','') + ','
                for img in span.find_all('img'):
                    telephone = 'http://huaian.ganji.com' + str(img.get('src'))
            for li in div.find_all('li',attrs={'class':'fl'}):
                if len(str(li.get_text()).split('\n'))>1:
                    name = str(li.get_text()).split('\n')[1].replace(' ','')
        #print telephone.rstrip(',')
        #print name   
        #print title,release_time,telephone.rstrip(','),name,prices,brand_model,trip_distance,licenses,myUrl
        if telephone != '':
            print title,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl
            res = [title,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from ganji_sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    print "The data is not exists in the database..."
                    curs.execute("insert into ganji_sell_car_info(title,release_time,telephone,name,addrs,prices,brand_model,trip_distance,licenses,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1345408840x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1305811548x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1318837868x.htm')


#print "=================================================================================="

##get_qiugou_info('http://maanshan.ganji.com/ershouche/1339247794x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1338944828x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1336617045x.htm')




def main():
    url="http://huaian.ganji.com/ershouche/a1o"
    localfile="Href.txt"
    for i in range(1,30):
        myUrl = url + str(i)
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()

if __name__=="__main__":
    main()
