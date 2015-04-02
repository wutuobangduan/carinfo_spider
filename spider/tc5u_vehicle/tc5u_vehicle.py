# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import chardet
import re
import MySQLdb
#import socket 
#socket.setdefaulttimeout(120) 
import threading
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException,TimeoutException

from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
from lxml import etree


def get_all_brand(url):
     user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
     heads = {'User-Agent':user_agent}
     req = urllib2.Request(url,headers=heads)
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
         soup = BeautifulSoup(html.decode('gbk').encode('utf-8'))
         for dl in soup.find_all('dl'):
             for dt in dl.find_all('dt'):
                 brand_name = ''
                 for div2 in dt.find_all('div'):
                     for a in div2.find_all('a'):
                         brand_name = str(a.get_text())
             for dd in dl.find_all('dd'):
                 j = 0
                 series_link = []
                 series_name = []
                 on_stop_sale = []
                 second_brand_name = []
                 for div2 in dd.find_all('div',attrs={'class':'h3-tit'}):
                     second_brand_name += [str(div2.get_text())]
                 for i in range(len(second_brand_name)):
                     series_link += [[]]
                     series_name += [[]]
                     on_stop_sale += [[]]
                 for ul in dd.find_all('ul',attrs={'class':'rank-list-ul'}):
                     for i in range(len(second_brand_name)):
                         if j == i:
                             for li in ul.find_all('li'):
                                 for h4 in li.find_all('h4'):
                                     for a in h4.find_all('a'):
                                         #print a
                                         series_link[i] += [a.get('href')]
                                         series_name[i] += [str(a.get_text())]
                                         on_stop_sale[i] += [a.get('class')]
                     j += 1
                 for i in range(len(second_brand_name)):
                     for k in range(len(series_link[i])):
                         print brand_name,second_brand_name[i],series_link[i][k],series_name[i][k],on_stop_sale[i][k]

#letter_list = ["A","B","C","D","F","G","H","J","K","L","M","N","O","P","Q","R","S","T","W","X","Y","Z"]
#for z in range(len(letter_list)):
#    url = "http://www.autohome.com.cn/grade/carhtml/" + letter_list[z] +".html"
#    get_all_brand(url)


def get_qiugou_info(myUrl):
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
            soup = BeautifulSoup(html.decode('gbk').encode('utf-8'))
            for dl in soup.find_all('dl'):
                for dt in dl.find_all('dt'):
                    brand_name = ''
                    for div2 in dt.find_all('div'):
                        for a in div2.find_all('a'):
                            brand_name = str(a.get_text())
                for dd in dl.find_all('dd'):
                    j = 0
                    series_link = []
                    series_name = []
                    on_stop_sale = []
                    second_brand_name = []
                    will_be_onsale = []
                    for div2 in dd.find_all('div',attrs={'class':'h3-tit'}):
                        second_brand_name += [str(div2.get_text())]
                    for i in range(len(second_brand_name)):
                        series_link += [[]]
                        series_name += [[]]
                        on_stop_sale += [[]]
                        will_be_onsale += [[]]
                    for ul in dd.find_all('ul',attrs={'class':'rank-list-ul'}):
                        for i in range(len(second_brand_name)):
                            if j == i:
                                for li in ul.find_all('li'):
                                    for h4 in li.find_all('h4'):
                                        for a in h4.find_all('a'):
                                            #print a
                                            series_link[i] += [a.get('href')]
                                            series_name[i] += [str(a.get_text())]
                                            on_stop_sale[i] += [a.get('class')]
                                        for cont in h4.find_all('i',attrs={'class':'icon icon-jseason'}):
                                            will_be_onsale[i] += [cont.get('title')]
                                        else:
                                            for a in h4.find_all('a'):
                                                will_be_onsale[i] += [None]
                        j += 1
                    for i in range(len(second_brand_name)):
                        for k in range(len(series_link[i])):
                            print brand_name,second_brand_name[i],series_link[i][k],will_be_onsale[i][k],series_name[i][k],on_stop_sale[i][k]
                            res_brand = [brand_name,'',myUrl.split('/')[-1].split('.')[0]]
                            try:
                                conn = MySQLdb.connect(host='192.168.2.201',user='insert_tc5u',passwd='dp')
                                curs = conn.cursor()
                                conn.select_db('tc_platform')
                                print "check the brand whether exists..."
                                curs.execute("select brand_id from tc_vehicle_brand where brand_name='%s'" % brand_name)
                                getbrand=curs.fetchall()
                                if not getbrand:
                                    print "insert tc_vehicle_brand..."
                                    curs.execute("insert into tc_vehicle_brand(brand_name,brand_alias,brand_initial) values(%s,%s,%s)",res_brand)
                                
                                print "select brand_id..."
                                curs.execute("select brand_id from tc_vehicle_brand where brand_name='%s'" % brand_name)
                                brand_id=curs.fetchone() 
                                print "select brand_id is ",brand_id
                                res_series1 = [0,int(brand_id[0]),second_brand_name[i],'']
                                print "check the second brand whether exists..."
                                curs.execute("select series_id from tc_vehicle_series where `series_name`='%s' and `brand_id`=%s" % (second_brand_name[i],int(brand_id[0])))
                                getsecondbrand = curs.fetchone()
                                print "check second brand id is ", getsecondbrand
                                if not getsecondbrand:
                                    print "insert tc_vehicle_series the second brand..."
                                    curs.execute("insert into tc_vehicle_series(series_parent_id,brand_id,series_name,series_alias) values(%s,%s,%s,%s)",res_series1)
                                
                                print "select second_brand series_id..."
                                curs.execute("select series_id from tc_vehicle_series where brand_id=%s and series_name ='%s' " % (int(brand_id[0]),second_brand_name[i]))
                                series_parent_id = curs.fetchone()
                                print "select second brand id is : ",series_parent_id
                                sale_state1 = u'停售'.encode('utf-8')
                                sale_state2 = u'在售'.encode('utf-8')
                                sale_state3 = u'将上市'.encode('utf-8')
                                res_series2 = [int(series_parent_id[0]),int(brand_id[0]),series_name[i][k],series_link[i][k],'',sale_state1]
                                res_series3 = [int(series_parent_id[0]),int(brand_id[0]),series_name[i][k],series_link[i][k],'',sale_state2] 
                                res_series4 = [int(series_parent_id[0]),int(brand_id[0]),series_name[i][k],series_link[i][k],'',sale_state3]
                                print "check the series whether exists..."
                                curs.execute("select series_id from tc_vehicle_series where series_name = '%s' and brand_id= %s" % (series_name[i][k],int(brand_id[0])))
                                getseries = curs.fetchall()
                                if not getseries:
                                    print "insert tc_vehicle_series the series...."
                                    if on_stop_sale[i][k] is not None:
                                        curs.execute("insert into tc_vehicle_series(series_parent_id,brand_id,series_name,series_link,series_alias,sale_state) values(%s,%s,%s,%s,%s,%s)",res_series2)
                                    else:
                                        if will_be_onsale[i][k] is None:
                                            curs.execute("insert into tc_vehicle_series(series_parent_id,brand_id,series_name,series_link,series_alias,sale_state) values(%s,%s,%s,%s,%s,%s)",res_series3)
                                        else:
                                            curs.execute("insert into tc_vehicle_series(series_parent_id,brand_id,series_name,series_link,series_alias,sale_state) values(%s,%s,%s,%s,%s,%s)",res_series4)
                                if on_stop_sale[i][k] is None and will_be_onsale[i][k] is None:
                                    print "select the model series_id ..."
                                    curs.execute("select series_id from tc_vehicle_series where series_name = '%s' and brand_id= %s" % (series_name[i][k],int(brand_id[0])))
                                    series_id = curs.fetchone()
                                    print "select model series_id is : ",series_id
                                    (all_year_patterns,all_vehicle_model_names,all_vehicle_model_ids) = handle_onsale_vehicle_model(series_link[i][k])
                                    print len(all_year_patterns),'=======length=======',len(all_vehicle_model_names),'=====================',len(all_vehicle_model_ids)
                                    if len(all_year_patterns)<1:
                                        localfile = open("no_ok_link.txt","a")
                                        localfile.write(str(series_link[i][k]))
                                        localfile.write("\r\n")
                                        localfile.close()
                                    for y in range(len(all_year_patterns)):
                                        res_models = [all_vehicle_model_names[y],int(brand_id[0]),int(series_id[0]),int(series_parent_id[0]),series_name[i][k],brand_name,all_year_patterns[y],all_vehicle_model_ids[y]]
                                        print "check whether the vehicle_model exists..."
                                        #curs.execute("select vehicle_model_id from tc_vehicle_model where vehicle_name = '%s' and brand_id=%s and series_id=%s and series_id_top=%s" % (all_vehicle_model_names[y],int(brand_id[0]),int(series_id[0]),int(getsecondbrand[0])
                                        curs.execute("select vehicle_model_id from tc_vehicle_model where che168_model_id=%s" % all_vehicle_model_ids[y])
                                        getmodels = curs.fetchone()
                                        if not getmodels:
                                            print "insert tc_vehicle_model the models..."
                                            curs.execute("insert into tc_vehicle_model(vehicle_name,brand_id,series_id,series_id_top,series_name,brand_name,vehicle_selltime,che168_model_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",res_models)
                                        else:
                                            localfile = open("che168_model.txt","a")
                                            localfile.write(str(getmodels[0]))
                                            localfile.write("\r\n")
                                            localfile.close()
                                elif on_stop_sale[i][k] is not None:
                                    user_agent1 = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
                                    heads1 = {'User-Agent':user_agent1}
                                    req1 = urllib2.Request(series_link[i][k],headers=heads1)
                                    html1 = ''
                                    fails1 = 0  
                                    while True:
                                        try:
                                            if fails1 >= 10:
                                                break
                                            response1 = urllib2.urlopen(req1,timeout=30)
                                            html1 = response1.read()
                                        except:
                                            fails1 += 1
                                            print "Handing brand,the network may be not Ok,please wait...",fails1
                                        else:
                                            break
                                    if html1 != '':
                                        print series_link[i][k]
                                        print chardet.detect(html1)
                                        soup1 = BeautifulSoup(html1.decode('gbk','ignore').encode('utf-8'))
                                        for stop_link in soup1.find_all(attrs={'class':'link-sale'}):
                                            if stop_link.get('href') is not None:
                                                print stop_link.get('href')
                                                
                                                print "select the model series_id ..."
                                                curs.execute("select series_id from tc_vehicle_series where series_name = '%s' and brand_id= %s" % (series_name[i][k],int(brand_id[0])))
                                                series_id = curs.fetchone()
                                                print "select model series_id is : ",series_id
                                                stop_series_link = ''
                                                if len(series_link[i][k].split('#')) > 0:
                                                    stop_series_link = series_link[i][k].split('#')[0]+'sale.html' 
                                                if stop_series_link != '':
                                                    (all_year_patterns,all_vehicle_model_names,all_vehicle_model_ids) = handle_stopsale_vehicle_model(stop_series_link)
                                                    print len(all_year_patterns),'=======length=======',len(all_vehicle_model_names),'=====================',len(all_vehicle_model_ids)
                                                    if len(all_year_patterns)<1:
                                                        localfile = open("no_ok_link1.txt","a")
                                                        localfile.write(str(series_link[i][k]))
                                                        localfile.write("\r\n")
                                                        localfile.close()
                                                    for y in range(len(all_year_patterns)):
                                                        res_models = [all_vehicle_model_names[y],int(brand_id[0]),int(series_id[0]),int(series_parent_id[0]),series_name[i][k],brand_name,all_year_patterns[y],all_vehicle_model_ids[y]]
                                                        print "check whether the vehicle_model exists..."
                                                        #curs.execute("select vehicle_model_id from tc_vehicle_model where vehicle_name = '%s' and brand_id=%s and series_id=%s and series_id_top=%s" % (all_vehicle_model_names[y],int(brand_id[0]),int(series_id[0]),int(getsecondbrand[0])
                                                        curs.execute("select vehicle_model_id from tc_vehicle_model where che168_model_id=%s" % all_vehicle_model_ids[y])
                                                        getmodels = curs.fetchone()
                                                        if not getmodels:
                                                            print "insert tc_vehicle_model the models..."
                                                            curs.execute("insert into tc_vehicle_model(vehicle_name,brand_id,series_id,series_id_top,series_name,brand_name,vehicle_selltime,che168_model_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",res_models)
                                                        else:
                                                            localfile = open("che168_model1.txt","a")
                                                            localfile.write(str(getmodels[0]))
                                                            localfile.write("\r\n")
                                                            localfile.close() 
                                conn.commit()
                                curs.close()
                                conn.close()
                            except MySQLdb.Error,e:
                                print "Error %d %s" % (e.args[0],e.args[1])
                                sys.exit(1)
                            
                            #  begin to handle vehicle_model....
                            #  ======================================================
                            
                            #if on_stop_sale[i][k] is None:
                                
def handle_onsale_vehicle_model(url):
    proxy = {'http':'http://202.106.16.36:3128'}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
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
            print "Handing onsale,the network may be not Ok,please wait...",fails
        else:
            break
    if html != '':
        j = 1
        soup = BeautifulSoup(html)
        stop_sale_link = None
        all_year_patterns,all_vehicle_model_names,all_vehicle_model_ids = [],[],[]
        onsale_year_patterns,onsale_vehicle_model_names,onsale_vehicle_model_ids = [],[],[]
        for div in soup.find_all('div',attrs={'id':'navTop'}):
            for li in div.find_all('li',attrs={'class':'nav-item'}):              
                if j == 2:
                    for a in li.find_all('a'):
                        vehicle_config_url = a.get('href') 
                        print "onsale config link is >>>> ",a.get('href')
                        (onsale_year_patterns,onsale_vehicle_model_names,onsale_vehicle_model_ids) = handle_vehicle_config(vehicle_config_url) 
                        get_data_fails = 0
                        while True:
                            if len(onsale_year_patterns) == 0:
                                get_data_fails += 1
                                print "get onsale config failed...",get_data_fails
                                (onsale_year_patterns,onsale_vehicle_model_names,onsale_vehicle_model_ids) = handle_vehicle_config(vehicle_config_url)
                                if len(onsale_year_patterns)>0:
                                    break
                                handle_onsale_vehicle_model(url)
                                get_data_fails += 1
                            else:
                                break
                                
                            if get_data_fails>=10:
                                break
                j += 1
        for div in soup.find_all('div',attrs={'class':'subnav-title'}):
            for div2 in div.find_all('div',attrs={'class':'other-car'}):
                for a in div2.find_all('a',attrs={'class':'link-sale'}):
                    stop_sale_link = "http://www.autohome.com.cn" + a.get('href')
                    print "stop sale link is ...",stop_sale_link
                    (stopsale_year_patterns,stopsale_vehicle_model_names,stopsale_vehicle_model_ids) = handle_stopsale_vehicle_model(stop_sale_link)
        
        print "onsale vehicle's stopsale link is >>>",stop_sale_link
        if len(onsale_year_patterns)>0:
            if stop_sale_link is not None:
                all_year_patterns += onsale_year_patterns
                all_vehicle_model_names += onsale_vehicle_model_names
                all_vehicle_model_ids += onsale_vehicle_model_ids
                for i in range(len(stopsale_year_patterns)):
                    all_year_patterns += stopsale_year_patterns[i]
                all_vehicle_model_names += stopsale_vehicle_model_names
                all_vehicle_model_ids += stopsale_vehicle_model_ids
            else:
                all_year_patterns += onsale_year_patterns
                all_vehicle_model_names += onsale_vehicle_model_names
                all_vehicle_model_ids += onsale_vehicle_model_ids
        return (all_year_patterns,all_vehicle_model_names,all_vehicle_model_ids)
        #for i in range(len(all_year_patterns)):
        #    print all_year_patterns[i],all_vehicle_model_names[i]
        
def handle_stopsale_vehicle_model(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    html = ''
    fails = 0
    while True:
        try:
            if fails>=10:
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing stopsale,the network may be not Ok,please wait...",fails
        else:
            break
    if html != '':
        j = 1
        stopsale_year_pattern = []
        stopsale_year_patterns = []
        stopsale_vehicle_model_names = []
        stopsale_vehicle_model_ids = []
        if chardet.detect(html)['encoding'] == 'GB2312':
            soup = BeautifulSoup(html.decode('gbk').encode('utf-8'))
        else:
            handle_stopsale_vehicle_model(url)
        for div in soup.find_all('div',attrs={'class':'car_detail'}):
            n = len(stopsale_year_patterns)
            for div2 in div.find_all('div',attrs={'class':'header'}):
                for div3 in div2.find_all('div',attrs={'class':'car_price'}):
                    for span in div3.find_all('span',attrs={'class':'years'}):
                        stopsale_year_pattern += [re.compile(r'[0-9]{4}').findall(str(span.get_text()))]
            for div2 in div.find_all('div',attrs={'class':'modelswrap'}):
                for div3 in div2.find_all('div',attrs={'class':'tabwrap'}):
                    for tr in div3.find_all('tr'):
                        for td in tr.find_all('td',attrs={'class':'name_d'}):
                            stopsale_vehicle_model_names += [str(td.get_text())]
                            for a in td.find_all('a'):
                                stopsale_vehicle_model_ids += [a.get('href').split('/')[-2]]
                        #for td in tr.find_all('td',attrs={'class':'info_d'}):
                        #    for a in td.find_all('a'):
                        #        if u'参数配置'.encode('utf-8') in str(a.get_text()):
                        #            stopsale_url = "http://www.autohome.com.cn/" +a.get('href')
                        #            print stopsale_url
                        #            #(stopsale_year_pattern,stopsale_vehicle_model_name) = handle_vehicle_config(stopsale_url)
            for i in range(n,len(stopsale_vehicle_model_names)):
                stopsale_year_patterns += [stopsale_year_pattern[-1]]
            #if len(stopsale_year_pattern)>0:
            #    stopsale_year_patterns += stopsale_year_pattern
        #for i in range(len(stopsale_year_patterns)):
        #    print stopsale_year_patterns[i],stopsale_vehicle_model_names[i],stopsale_vehicle_model_ids[i]
        return (stopsale_year_patterns,stopsale_vehicle_model_names,stopsale_vehicle_model_ids)
            


def handle_vehicle_config(url):
        j = 1
        vehicle_model_names = []
        year_patterns = []
        vehicle_model_ids = []
        #soup = BeautifulSoup(html)
        #for div in soup.find_all('div',attrs={'class':'filtrate-list'}):
        #    for label in div.find_all('label',attrs={'for':'Year00'}):
        #        year_pattern = str(label.get_text())
        #print year_pattern
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = None
        fails = 0
        try:
            browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8/bin/phantomjs') 
            browser.set_page_load_timeout(30)
            #browser.implicitly_wait(30)
            #print "==============Check Whether the browser is online....",browser.is_online(),"======================"
            print "=================open browser======================="
        except WebDriverException,e:
            print e
        if browser is not None:
            while True:
                try:
                    if fails >= 10:
                        break
                    
                    browser.get(url)
                except TimeoutException as e:
                    fails += 1
                    print "The selenium PhantomJs is timeout,wait...",fails
                    print e
                else:
                    break

            release_content = None
            try:
                #release_content = browser.find_elements_by_class_name('carbox')
                release_content = browser.find_elements_by_xpath('//div[@class="carbox"]/div')
                vehicle_model_id = browser.find_elements_by_xpath('//div[@class="carbox"]/div/a')
            except NoSuchElementException,e:
                print e
        #for div in soup.find_all('div',attrs={'id':'config_nav'}):
        #    for table in div.find_all('table',attrs={'class':'tbset'}):
        #        for tr in table.find_all('tr'):
        #            for td in tr.find_all('td'):
        #                for div2 in td.find_all('div',attrs={'class':'carbox'}):
        #                    for div3 in div2.find_all('div'):
        #                        for a in div3.find_all('a'):
        #                            print year_pattern,a.get_text()
            for i in range(len(release_content)):
                pat = re.compile(r'[0-9]{4}')
                year_pattern = pat.findall(str(release_content[i].text))
                if len(year_pattern)>0:
                    year_patterns += [year_pattern[0]]
                    vehicle_model_names += [str(release_content[i].text)]
                    vehicle_model_ids += [str(vehicle_model_id[i].get_attribute("href")).split('/')[-2]]
        #for s in range(len(year_patterns)):
        #    print year_patterns[s],vehicle_model_names[s],vehicle_model_ids[s]
        print year_patterns,vehicle_model_names,vehicle_model_ids
        return (year_patterns,vehicle_model_names,vehicle_model_ids)
    


#print "=================================================================================="

#handle_stopsale_vehicle_model('http://www.autohome.com.cn/692/sale.html')
#print "=================================================================================="
#handle_stopsale_vehicle_model('http://www.autohome.com.cn/470/sale.html')
#print "=================================================================================="

#print "=================================================================================="
#handle_onsale_vehicle_model('http://www.autohome.com.cn/692/#levelsource=000000000_0&pvareaid=101594')
#
#print "=================================================================================="
#handle_onsale_vehicle_model('http://www.autohome.com.cn/504/#levelsource=000000000_0&pvareaid=101594')
#
#print "=================================================================================="
#
#handle_onsale_vehicle_model('http://www.autohome.com.cn/923/#levelsource=000000000_0&pvareaid=101594')
#
#print "=================================================================================="
#
#
#print "=================================================================================="
#handle_vehicle_config('http://car.autohome.com.cn/config/series/692.html')

#print "=================================================================================="
#handle_vehicle_config('http://car.autohome.com.cn/config/series/2745.html')

#print "=================================================================================="
#handle_vehicle_config('http://car.autohome.com.cn/config/series/923.html')


#get_qiugou_info('http://www.autohome.com.cn/car/')



def main():
    letter_list = ["A","B","C","D","F","G","H","J","K","L","M","N","O","P","Q","R","S","T","W","X","Y","Z"]
    for z in range(len(letter_list)):
        url = "http://www.autohome.com.cn/grade/carhtml/" + letter_list[z] +".html"  
        get_qiugou_info(url)

if __name__=="__main__":
    main()
