# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
import time
import socket
#ocket.setdefaulttimeout(30)
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
        href = None
        for div in  BeautifulSoup(html).find_all('div',attrs={'class':'f_l list_02'}):
            for h2 in div.find_all('h2',attrs={'style':'white-space:nowrap'}):
                for a in h2.find_all('a'):
                    href = a.get('href')
                    if href: 
                        #and href not in dictionary:
                        #dictionary[href] = ''
                        ans = 'http://used.xcar.com.cn' + href
                         
                        print "====================================================================================================================================="
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
        new_car_prices = ''
        addrs = ''
        name = ''
        vehicle_info = ''
        release_time = ''
        telephone = ''
        trip_distance = ''
        licenses = ''
        is_seller = ''
        owner_readme = ''
        displacement = ''
        transmissions = ''
        vehicle_color = ''
        img_src = ''
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        j = 1
        for div in soup.find_all('div',attrs={'class':'specifics_l f_l'}):
            for div2 in div.find_all('div',attrs={'class':'specifics_title'}):
                for h1 in div2.find_all('h1'):
                    title = str(h1.get_text())
                for span in div2.find_all('span',attrs={'class':'time'}):
                    if len(str(span.get_text()).split('：'))>1:
                        release_time = str(span.get_text()).split('：')[1]
            for div3 in div.find_all('div',attrs={'class':'info_right f_r'}):
                for div4 in div3.find_all('div',attrs={'class':'info_cost'}):
                    #print str(div4.get_text()).split('：')
                    if len(str(div4.get_text()).split('：'))>1 and len(str(div4.get_text()).split('：')[1].split('\n'))>0:
                        prices = str(div4.get_text()).split('：')[1].split('\n')[0]
                        new_car_prices = str(div4.get_text()).split('：')[-1]
                for ul in div3.find_all('ul',attrs={'class':'datum_ul'}):
                    for li in ul.find_all('li'):
                        if j == 1:
                            if len(str(li.get_text()).split('：'))>1:
                                licenses = str(li.get_text()).split('：')[1]   
                        elif j == 2:
                            if len(str(li.get_text()).split('：'))>1:
                                displacement = str(li.get_text()).split('：')[1] 
                        elif j == 3:
                            if len(str(li.get_text()).split('：'))>1:
                                trip_distance = str(li.get_text()).split('：')[1]
                        elif j == 4:
                            if len(str(li.get_text()).split('：'))>1:
                                transmissions = str(li.get_text()).split('：')[1]
                        elif j == 5:
                            if len(str(li.get_text()).split('：'))>1:
                                vehicle_color = str(li.get_text()).split('：')[1]
                        elif j == 6:
                            if len(str(li.get_text()).split('：'))>1:
                                environmental_protection_standard = str(li.get_text()).split('：')[1]     
                        j += 1
                for div5 in div3.find_all('div',attrs={'class':'details_one'}):
                    for img in div5.find_all('img'):    
                        img_src = 'http://used.xcar.com.cn' + img.get('src')
                    for span in div5.find_all('span',attrs={'class':'name'}):
                        name = str(span.get_text())
        k = 1
        for div in soup.find_all('div',attrs={'class':'details_list clearfix mt12'}):
            for td in div.find_all('td',attrs={'class':'td_128'}):
                if k == 1:
                    addrs = str(td.get_text())
                k += 1
        s = 1
        for div in soup.find_all('div',attrs={'class':'details_list2 clearfix mt12'}):
            if s == 1:
                for p in div.find_all('p'):
                    owner_readme = str(p.get_text())
            s += 1
        #print title,release_time,prices,new_car_prices
        #print licenses,displacement,trip_distance,transmissions,vehicle_color,environmental_protection_standard
        print img_src,name,addrs,owner_readme
        if img_src != '':
            print title,name,addrs,release_time,prices,new_car_prices,licenses,displacement,trip_distance,transmissions,vehicle_color,environmental_protection_standard,img_src,owner_readme,myUrl
            is_seller = u'个人'.encode('utf-8')
            res = [title,is_seller,name,addrs,release_time,prices,new_car_prices,licenses,displacement,trip_distance,transmissions,vehicle_color,environmental_protection_standard,img_src,owner_readme,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from xcar_sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    print "The data is not exists in the database..."
                    curs.execute("insert into xcar_sell_car_info(title,is_seller,name,addrs,release_time,prices,new_car_prices,licenses,displacement,trip_distance,transmissions,vehicle_color,environmental_protection_standard,img_src,owner_readme,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/personal/1743881.htm')

#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/personal/1760248.htm')

#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/shop/1464939.htm')


#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/shop/1650309.htm')



def main():
    url="http://used.xcar.com.cn/search/25-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-0?page="
    localfile="Href.txt"
    for i in xrange(1,50):
    #for i in range(1,5):
        myUrl = url + str(i)
        print "current page is %d " % i
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d " % i

if __name__=="__main__":
    main()
