# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
from pyvirtualdisplay import Display
from selenium import webdriver
import socket
#socket.setdefaulttimeout(30)

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

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
    dictionary = {}
    for content in BeautifulSoup(html).find_all('td',attrs={'class':'t'}):
        for a in content.find_all('a',attrs={'class':'t'}):
            #if str(a.get('href')) not in dictionary:
                if len(a.get('href').split('/'))>2 and len(str(a.get('href')).split('/')[2].split('.'))>0:
                    if str(a.get('href')).split('/')[2].split('.')[0] == 'bengbu':
                        #dictionary[str(a.get('href'))] = ''
                        print str(a.get('href'))
                        get_qiugou_info(str(a.get('href')))



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
        title2 = ''
        prices = ''
        addrs = u'安徽蚌埠'.encode('utf-8')
        name = ''
        release_time = ''
        owner_readme = ''
        telephone = ''
        for div in soup.find_all('div',attrs={'id':'content_sumary_right'}):
            for h1 in div.find_all('h1',attrs={'class':'h1'}):
                title = str(h1.get_text())
            for h2 in div.find_all('h2',attrs={'class':'h2'}):
                title2 = str(h2.get_text()).replace('\n','')
        for div in soup.find_all('div',attrs={'class':'content_price_left'}):
            for span in div.find_all('span',attrs={'class':'font_jiage'}):
                prices = str(span.get_text())
        for div in soup.find_all('p',attrs={'class':'lineheight_2'}):
            for a in div.find_all('a',attrs={'rel':'nofollow'}):
                name = str(a.get_text())
        for span in soup.find_all('span',attrs={'id':'t_phone','class':'font20'}):
            RG = re.compile(r'\d+-?\d*-?\d*')
            if len(RG.findall(str(span.get_text())))>0:
                telephone = RG.findall(str(span.get_text()))[0]
        for ul in soup.find_all('ul',attrs={'class':'mtit_con_left fl'}):
            for li in ul.find_all('li',attrs={'class':'time'}):
                release_time = str(li.get_text())
        for div in soup.find_all('div',attrs={'class':'benchepeizhi'}):
            owner_readme = str(div.get_text())
        print title,title2,prices,name,telephone,release_time,owner_readme,addrs
        
        
        if telephone != '':
            print title,title2,prices,name,telephone,release_time,addrs
            #res = [title,title2,prices,name,telephone,release_time,owner_readme,addrs,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    curs.execute("select id from sell_car_info where telephone_num='%s'" % telephone)
                    get_telephones = curs.fetchall()
                    if not get_telephones:
                        is_seller = u'个人'.encode('utf-8')
                    else:
                        is_seller = u'商家'.encode('utf-8')
                    info_src = '58'
                    res = [title,title2,name,telephone,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
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

#print "=================================================================================="


#print "=================================================================================="


#print "=================================================================================="

print "=================================================================================="

#print "=================================================================================="


#print "=================================================================================="

#get_qiugou_info('http://sh.58.com/ershouche/20647753356038x.shtml?PGTID=14213939221850.6898022816450731&ClickID=4')
def main():
    url="http://bengbu.58.com/ershouche/0/pn"
    localfile="Href.txt"
    for i in range(1,5):
        myUrl = url + str(i)
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()

if __name__=="__main__":
    main()
