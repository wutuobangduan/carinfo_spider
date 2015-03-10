# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import socket 
#socket.setdefaulttimeout(30) 
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
        dictionary = {}
        content = BeautifulSoup(html).find_all('a')
        pat = re.compile(r'http://\w+.ganji.com/ershouche/\d+x.htm')
        for item in content:
             href = pat.findall(str(item))
             if href:
                 #if href[0] not in dictionary:
                     if len(str(href[0]).split('/'))>2 and len(str(href[0]).split('/')[2].split('.'))>0:
                         #if str(href[0]).split('/')[2].split('.')[0] == 'changzhou':
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
        

        if myUrl.split('/')[2].split('.')[0] == 'changzhou':
            addrs = u'江苏常州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'su':
            addrs = u'江苏苏州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'nj':
            addrs = u'江苏南京'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'wx':
            addrs = u'江苏无锡'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'xuzhou':
            addrs = u'江苏徐州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'nantong':
            addrs = u'江苏南通'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'yangzhou':
            addrs = u'江苏扬州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'yancheng':
            addrs = u'江苏盐城'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'huaian':
            addrs = u'江苏淮安'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'lianyungang':
            addrs = u'江苏连云港'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'jstaizhou':
            addrs = u'江苏泰州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'suqian':
            addrs = u'江苏宿迁'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'zhenjiang':
            addrs = u'江苏镇江'.encode('utf-8')
        else:
            addrs = None
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
                release_time = '2015-' + str(i.get_text())
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
                    telephone = 'http://' + myUrl.split('/')[2].split('.')[0] + '.ganji.com' + str(img.get('src'))
            for li in div.find_all('li',attrs={'class':'fl'}):
                if len(str(li.get_text()).split('\n'))>1:
                    name = str(li.get_text()).split('\n')[1].replace(' ','')
        #print telephone.rstrip(',')
        #print name   
        #print title,release_time,telephone.rstrip(','),name,prices,brand_model,trip_distance,licenses,myUrl
        if telephone != '':
            print title,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl
            #res = [title,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from ganji_sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                is_seller=u'个人'.encode('utf-8')
                if not getrows:
                    curs.execute("select id from ganji_sell_car_info where telephone='%s'" % telephone.rstrip(','))
                    get_telephones = curs.fetchall()
                    if not get_telephones:
                        is_seller=u'个人'.encode('utf-8')
                    else:
                        is_seller=u'商家'.encode('utf-8')
                    res = [title,is_seller,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into ganji_sell_car_info(title,is_seller,release_time,telephone,name,addrs,prices,brand_model,trip_distance,licenses,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
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
    addr_list = ['nj','su','wx','xuzhou','changzhou','nantong','lianyungang','huaian','yancheng','yangzhou','zhenjiang','jstaizhou','suqian']
    for j in range(len(addr_list)):
        url = "http://" + addr_list[j] + ".ganji.com/ershouche/a1o"
        localfile="Href.txt"
        for i in range(1,10):
            print "current page is %d" % i
            myUrl = url + str(i)
            t = threading.Thread(target=grabHref(myUrl,localfile))
            t.start()
            print "current page is %d" % i

if __name__=="__main__":
    main()
