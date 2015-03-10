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
        dictionary = {}
        href = None
        for h4 in BeautifulSoup(html).find_all('h4',attrs={'class':'title'}):
            for a in h4.find_all('a'):
                if a.get('href')[1:3] == 'js': 
                    ans = 'http://2sc.sohu.com' + a.get('href')
                    if ans:
                        #dictionary[ans] = ''
                        print "====================================================================================================================================="
                        print ans
                        get_qiugou_info(ans)
                        print "======================================================================================================================================"

def get_qiugou_info(myUrl):
    proxy = {'http':'http://202.106.16.36:3128'}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)  
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
        vehicle_info = ''
        release_time = ''
        telephone = ''
        trip_distance = ''
        licenses = ''
        is_seller = ''
        owner_readme = ''
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        j = 1
        for div in soup.find_all('div',attrs={'class':'clearfix'}):
            for div2 in div.find_all('div',attrs={'class':'price-info-left fl'}):        
                for h2 in div2.find_all('h2',attrs={'class':'title'}):
                    title = str(h2.get_text()).replace('\t','').replace('\n','')
                for p in div2.find_all('p'):
                    if j == 1:
                        if len(str(p.get_text()).split('\n'))>4:
                            prices = str(p.get_text()).split('\n')[-4] + str(p.get_text()).split('\n')[-2].replace('\t','')
                    elif j == 3:
                        vehicle_info = str(p.get_text()).replace('\n','').replace('\t','')
                    j += 1
            for div3 in div.find_all('div',attrs={'class':'fl ml-10'}):
                if len(str(div3.get_text()).split('\n'))>7:
                    telephone = str(div3.get_text()).split('\n')[5]
                    if len(str(div3.get_text()).split('\n')[7].split('：'))>1:
                        name = str(div3.get_text()).split('\n')[7].split('：')[1]
        for div in soup.find_all('div',attrs={'class':'clearfix features'}):
            for span in div.find_all('span',attrs={'class':'shijian r'}):
                if len(str(span.get_text()).split('：'))>1:
                    release_time = str(span.get_text()).split('：')[1]
            for span2 in div.find_all('span',attrs={'class':'renzheng'}):
                    is_seller = str(span2.get_text()).replace('\n','').replace('\t','')
        for div in soup.find_all('div',attrs={'class':'usedCar-pd car-detail'}):
            for td in div.find_all('td',attrs={'style':'border-top:none; line-height: 22px;'}):
                owner_readme = str(td.get_text())
        addrs = u'江苏'.encode('utf-8')+title.split('-')[0]
        if telephone != '':
            print title,name,telephone,prices,vehicle_info,current_date,release_time,is_seller,owner_readme,myUrl
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    if telephone.startswith("400"):
                        is_seller = u'商家'.encode('utf-8')
                    info_src='sohu'
                    print "The data is not exists in the database..."
                    res = [title,vehicle_info,name,telephone,addrs,current_date + ' ' + release_time,prices,is_seller,owner_readme,info_src,myUrl]
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


#print "=================================================================================="

#get_qiugou_info('http://2sc.sohu.com/js-suzhou/buycar/carinfo_sohu_1288520.shtml#args=a0b0c0d0e0f0g3h0j0k0m0n0p0q0r320000s0t1')




def main():
    url="http://2sc.sohu.com/js/buycar/a0b0c0d0e0f0g1h0j0k0m0n0/pg"
    localfile="Href.txt"
    for i in range(1,5):
        myUrl = url + str(i)+'.shtml'
        print "current page is %d" % i
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()

if __name__=="__main__":
    main()
