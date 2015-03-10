# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
import socket 
#socket.setdefaulttimeout(30) 
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
        pat = re.compile(r'/[a-zA-Z]+/\d+/\d+.html#pvareaid=\d+#pos=\d+')
        for div in BeautifulSoup(html).find_all('div',attrs={'class':'title'}):
            for a in div.find_all('a'):
                ans = 'http://www.che168.com/' + a.get('href')
                print ans
                get_qiugou_info(ans)


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
        title2 = ''
        prices = ''
        addrs = u'江苏'.encode('utf-8')
        name = ''
        release_time = ''
        owner_readme = ''
        telephone = ''
        trip_distance = ''
        licenses = ''
        reference_prices = ''
        
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        i = 1
#        display = Display(visible=0, size=(800, 600))
#        display.start()
#        browser = None
#        try:
#            browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8-linux-x86_64/bin/phantomjs') 
#        except WebDriverException,e:
#            print e
#        if browser is not None:
#            browser.get(myUrl)
#            try:
#                reference_price = browser.find_element_by_id('spanReferencePrice')
#            except NoSuchElementException,e:
##                print e
#            reference_prices = reference_price.text
        for div in soup.find_all('div',attrs={'class':'car-info'}):
            for h2 in div.find_all('h2'):
                title = str(h2.get_text())
            for span in div.find_all('span',attrs={'class':'fn-left'}):
                prices = str(span.get_text())
            for div2 in div.find_all('div',attrs={'class':'fn-left-box'}):
                if len(str(div2.get_text()).split('：'))>2:
                    if len(str(div2.get_text()).split('：')[1].split('\n'))>0:
                        trip_distance = str(div2.get_text()).split('：')[1].split('\n')[0]
                    if len(str(div2.get_text()).split('：')[2].split('\n'))>0:
                        licenses = str(div2.get_text()).split('：')[2].split('\n')[0]
            for div3 in div.find_all('div',attrs={'class':'code-tx'}):
                for span in div3.find_all('span',attrs={'class':'font22'}):     
                    telephone = str(span.get_text())
                for div4 in div3.find_all('div'):
                    for a in div4.find_all('a'):
                        if str(a.get_text()) != '':
                            i -= 1
                for div5 in div3.find_all('div'):
                    if i == 2:
                        name = str(div5.get_text())
                    elif i == 3:
                        if u'江苏'.encode('utf-8') in str(div5.get_text()):
                            addrs = str(div5.get_text()) 
                        else:
                            addrs += str(div5.get_text())  
                    i += 1
        for div in soup.find_all('div',attrs={'class':'section'}):
            for p in div.find_all('p',attrs={'class':'p-tx'}):
                owner_readme += str(p.get_text())       
        for div in soup.find_all('div',attrs={'class':'time'}):
            if len(str(div.get_text()).split('\n'))>1:
                release_time = str(div.get_text()).split('\n')[1].replace(' ','')
        #print release_time
        if telephone != '':
            print title,telephone,name,addrs,release_time,prices,reference_prices,trip_distance,licenses,owner_readme,myUrl
            #res = [telephone,name,addrs,title,prices,reference_prices,release_time,trip_distance,licenses,owner_readme,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                is_seller = u'商家'.encode('utf-8')
                if not getrows:
                    car_config = trip_distance + " | " + licenses
                    info_src = "che168"
                    res = [title,car_config,name,telephone,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
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

#get_qiugou_info('http://www.che168.com/dealer/70501/4268120.html#pvareaid=100520')

#print "=================================================================================="

#get_qiugou_info('http://www.che168.com/dealer/133939/4268079.html#pvareaid=100522')

#print "=================================================================================="

#get_qiugou_info('http://www.che168.com/dealer/101982/3200209.html#pvareaid=100521')


#print "=================================================================================="

#get_qiugou_info('http://www.che168.com/personal/4227508.html#pvareaid=100522')

def main():
    url="http://www.che168.com/jiangsu/a0_0ms2dgscncgpiltocsp"
    localfile="Href.txt"
    for i in range(1,5):
        myUrl = url + str(i)+'ex/'
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()

if __name__=="__main__":
    main()
