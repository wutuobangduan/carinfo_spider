# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import chardet
import re
import MySQLdb
import logging
import socket 
#socket.setdefaulttimeout(30) 
import threading
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException

import gzip
import cookielib
import optparse
import time
import datetime
from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

from lxml import etree
import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO
import pytesseract
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import Select

def main():
    parser = optparse.OptionParser()
    parser.add_option("-u","--username",action="store",type="string",default='',dest="username",help="Your baixing Username")
    parser.add_option("-p","--password",action="store",type="string",default='',dest="password",help="Your baixing password")
    parser.add_option("-d","--address",action="store",type="string",default='',dest="address",help="Your address")
    (options, args) = parser.parse_args()
    logging.basicConfig(filename = '/data/python/tc5u_statistic/58_tc/58_statistic.log',level = logging.INFO, filemode = 'a', format = '%(asctime)s - %(levelname)s: %(message)s') 
    if options.username == '' or options.password == '' or options.address == '':
        print "Usage: post_baixing.py -u yourbxUsername -p yourbxPassword -d youraddress"
        logging.warning("Usage: post_baixing.py -u yourbxUsername -p yourbxPassword -d youraddress")
        return False

    try:
        browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8-linux-x86_64/bin/phantomjs') 
    except WebDriverException,e:
        print e
        logging.error(e)
        return False
    if browser is not None:
        get_page_fails = 0
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://passport.58.com/login")
                browser.implicitly_wait(10)
                wait = ui.WebDriverWait(browser,30)
            except:
                get_page_fails += 1
                print "get page info failed ... %d" % get_page_fails
                logging.warning("get page info failed ... %d" % get_page_fails)
            else:
                break

        wait.until(EC.element_to_be_clickable((By.ID,'login_tab_orig')))
        browser.find_element_by_id('login_tab_orig').click()
        time.sleep(1)
        #print browser.find_element_by_class_name('logpic').text
        browser.find_element_by_id('username').clear()
        browser.find_element_by_id('username').send_keys(options.username.decode('utf-8'))
        #print options.password
        browser.find_element_by_id('password').clear()
        browser.find_element_by_id('password').send_keys(options.password)
        wait.until(EC.element_to_be_clickable((By.ID,'btnSubmit')))
        browser.find_element_by_id('btnSubmit').click()
        time.sleep(1)
        try:
            print browser.find_element_by_id('login-name').text
        except:
            print "continue wait ..."
        
        load_page_fails = 0
        wait = None
        while True:
            try:
                if load_page_fails > 10:
                    break
                browser.get("http://vip.58.com/app/mci/")
                browser.implicitly_wait(10)
                wait = ui.WebDriverWait(browser,30)
            except:
                load_page_fails += 1
                print "get car page view info failed ... %d" % load_page_fails
                logging.warning("get car page view info failed ... %d" % load_page_fails)
            else:
                break
        if options.address == 'nanjing':
            addrs = u'江苏南京'.encode('utf-8')
        elif options.address == 'changshu':
            addrs = u'江苏常熟'.encode('utf-8')
        elif options.address == 'jiangyin':
            addrs = u'江苏江阴'.encode('utf-8')
        elif options.address ==  'huaian':
            addrs = u'江苏淮安'.encode('utf-8')
        elif options.address == 'yangzhou':
            addrs = u'江苏扬州'.encode('utf-8')
        elif options.address == 'yixing':
            addrs = u'江苏宜兴'.encode('utf-8')
        elif options.address == 'taizhou':
            addrs = u'江苏泰州'.encode('utf-8')
        elif options.address == 'yancheng':
            addrs = u'江苏盐城'.encode('utf-8')
        elif options.address == 'zhenjiang':
            addrs = u'江苏镇江'.encode('utf-8')
        elif options.address == 'nantong':
            addrs = u'江苏南通'.encode('utf-8')
        elif options.address == 'suzhou':
            addrs = u'江苏苏州'.encode('utf-8')
        elif options.address == 'suqian':
            addrs = u'江苏宿迁'.encode('utf-8')
        yesterday = datetime.date.today()-datetime.timedelta(days=1)
        if wait is not None:
            page_nums = 0
            browser.switch_to.frame(browser.find_element_by_id('ContainerFrame'))
            while page_nums < 10:
                try:
                    car_info_options = browser.find_element_by_id('fang_vip_content').find_elements_by_class_name('s_02')
                except:
                    break
                #for car_info_option in car_info_options:
                try:
                    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                    curs = conn.cursor()
                    conn.select_db('spider')
                    for i in range(len(car_info_options)):
                        car_info = None
                        title = ''
                        config = ''
                        release_time = ''
                        if yesterday.isoformat() in str(car_info_options[i].find_element_by_tag_name('em').text):
                            print car_info_options[i].find_element_by_tag_name('em').text
                            release_time = str(car_info_options[i].find_element_by_tag_name('em').text)
                            page_view = str(browser.find_element_by_id('fang_vip_content').find_elements_by_class_name('infor_tab')[i].find_elements_by_tag_name('li')[2].find_element_by_tag_name('a').text)
                            car_info = str(browser.find_element_by_id('fang_vip_content').find_elements_by_class_name('infor_tab')[i].find_elements_by_tag_name('li')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('div').text).split('\n')
                            if car_info is not None:
                                #print len(car_info)
                                title = car_info[0]
                                config = car_info[1]
                                print title
                                print config
                                res = [title,config,release_time,page_view,addrs]
                                res2 = [release_time,addrs]
                                curs.execute("select id from vehicle_statistic_info where release_time=%s and addrs=%s",res2)
                                getrows = curs.fetchall()
                                if not getrows:
                                    curs.execute("insert into vehicle_statistic_info(title,car_config,release_time,page_view,addrs) values(%s,%s,%s,%s,%s)",res)
                                else:
                                    print "the data is already in the database,time: %s,address: %s" % (release_time,addrs)
                                    logging.info("the data is already in the database,time: %s,address: %s" % (release_time,addrs))
                        else:
                            print "The car statistics date is not yesterday,the time is %s" % str(car_info_options[i].find_element_by_tag_name('em').text)
                            logging.debug("The car statistics date is not yesterday,the time is %s" % str(car_info_options[i].find_element_by_tag_name('em').text))
                    conn.commit()
                    curs.close()
                    conn.close()
                except MySQLdb.Error,e:
                    print "Error %d %s" % (e.args[0],e.args[1])
                    logging.error("Error %d %s" % (e.args[0],e.args[1]))
                    sys.exit(1)
                page_nums += 1
                try:
                    browser.find_elements_by_class_name('paging_first')[1].click()
                except:
                    print "There is no page for page view statistic..."
                    logging.warning("There is no page for page view statistic...")
                    break
        wait1 = None
        load_tuiguang_page_fails = 0
        while True:
            try:
                if load_tuiguang_page_fails > 10:
                    break
                browser.get("http://vip.58.com/app/tuiguangdetail/")
                browser.implicitly_wait(10)
                wait1 = ui.WebDriverWait(browser,30)
            except:
                load_tuiguang_page_fails += 1
                print "get tuiguang detail page info failed ... %d" % load_tuiguang_page_fails
                logging.warning("get tuiguang detail page info failed ... %d" % load_tuiguang_page_fails)
            else:
                break
        if wait1 is not None:
            page_number = 0
            browser.switch_to.frame(browser.find_element_by_id('ContainerFrame'))
            while page_number < 10:
                try:
                    details_table_options = browser.find_element_by_class_name('details-table').find_elements_by_tag_name('tr')
                except:
                    break
                try:
                    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                    curs = conn.cursor()
                    conn.select_db('spider')
                    for i in range(1,len(details_table_options)):
                        detail_type = ''
                        banlance_changelog = ''
                        release_time = ''
                        detail = ''
                        remaining_amount = ''
                        account_type = ''
                        if yesterday.isoformat() in str(details_table_options[i].find_elements_by_tag_name('td')[0].text):
                            print details_table_options[i].find_elements_by_tag_name('td')[0].text
                            release_time = str(details_table_options[i].find_elements_by_tag_name('td')[0].text)
                            detail_type = str(details_table_options[i].find_elements_by_tag_name('td')[1].text)
                            balance_changelog = str(details_table_options[i].find_elements_by_tag_name('td')[2].text)
                            detail = str(details_table_options[i].find_elements_by_tag_name('td')[3].text)
                            remaining_amount = str(details_table_options[i].find_elements_by_tag_name('td')[4].text)
                            account_type = str(details_table_options[i].find_elements_by_tag_name('td')[5].text)
                            res1 = [release_time,detail_type,balance_changelog,detail,remaining_amount,account_type,addrs]
                            res3 = [release_time,addrs]
                            curs.execute("select id from tuiguang_detail where release_time=%s and addrs=%s",res3)
                            getrows1 = curs.fetchall()
                            if not getrows1:
                                curs.execute("insert into tuiguang_detail(release_time,detail_type,balance_changelog,detail,remaining_amount,account_type,addrs) values(%s,%s,%s,%s,%s,%s,%s)",res1)
                            else:
                                print "the data is already in the database,time: %s,address: %s" % (release_time,addrs)
                                logging.info("the data is already in the database,time: %s,address: %s" % (release_time,addrs))
                        else:
                            print "The date is not yesterday,the time is %s" % str(details_table_options[i].find_elements_by_tag_name('td')[0].text)
                            logging.debug("The date is not yesterday,the time is %s" % str(details_table_options[i].find_elements_by_tag_name('td')[0].text))
                    conn.commit()
                    curs.close()
                    conn.close()
                except MySQLdb.Error,e:
                    print "Error %d %s" % (e.args[0],e.args[1])
                    logging.error("Error %d %s" % (e.args[0],e.args[1]))
                    sys.exit(1)
                page_number += 1
                try:
                    browser.find_element_by_class_name('pager-jf').find_element_by_class_name('next').click()
                except:
                    print "There is no next page for tuiguang detail..."
                    logging.warning("There is no next page for tuiguang detail...")
                    break
       

if __name__=="__main__":
    main()
