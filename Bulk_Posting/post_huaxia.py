# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO
import pickle
import cookielib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#from bs4 import BeautifulSoup
import tempfile
import chardet
import MySQLdb

import win32api, win32pdhutil, win32con   
import win32com.client  
from win32com.client import Dispatch  
import requests

#webdriver的模块  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import Select  
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import unittest,time,re,os 

from pyvirtualdisplay import Display

from urllib2 import Request,urlopen,URLError,HTTPError

import optparse

from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains

# from pymouse import PyMouse

import BeautifulSoup,mechanize


#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;


def check_exists_by_id(browser,id):
    try:
        browser.find_element_by_id(id)
    except:
        return False
    return True



def get_car_info(vehicle_nums):
    imgurls = [""]
    try:
        conn = MySQLdb.connect(host='',user='spider',passwd='spi',charset='utf8')
        curs = conn.cursor()
        conn.select_db('')
        curs.execute("select vi.vin,(select d.field_value from data_dictionary d where d.id=(select dd.parent_id from data_dictionary dd where dd.id=vm.brand)),(select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address),vmc.vehicle_model_conf53 as environmental_standards,vmc.vehicle_model_conf48 as fuel_form,vmc.vehicle_model_conf5 as car_level,vmc.vehicle_model_conf28 as seating_nums  from vehicle_info vi,vehicle_model vm,vehicle_model_conf vmc where vi.vehicle_number='%s' and vm.id=vi.model_id and vmc.id=vi.model_id" % vehicle_nums)
        getrows=curs.fetchall()
        if not getrows:
            result = []
        else:
            #print getrows
            result = [getrows]

        curs.execute("select imgurl from vehicle_img where vehicle_number='%s'" % vehicle_nums)
        get_imgurls = curs.fetchone()
        
        while get_imgurls is not None:
            ((vehicle_img),) = get_imgurls
            #print "http://imgw00.tc5u.cn/" + vehicle_img
            if len(vehicle_img)>5:
                imgurls.append("http://imgn00.tc5u.cn/" + vehicle_img)
            get_imgurls = curs.fetchone()

        result.append(imgurls)
        conn.commit()
        curs.close()
        conn.close()
        return result
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)


def post_cardata():
    printDelimiter()
    parser = optparse.OptionParser()
    parser.add_option("-u","--username",action="store",type="string",default='',dest="username",help="Your baixing Username")
    parser.add_option("-p","--password",action="store",type="string",default='',dest="password",help="Your baixing password")
    (options, args) = parser.parse_args()
    if options.username == '' or options.password == '':
        print "Usage: post_baixing.py -u yourbxUsername -p yourbxPassword"
        return False
    browser = None
    get_page_fails = 0
    get_publish_page_fails = 0
    try:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        #browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        browser.implicitly_wait(5)
        browser.set_page_load_timeout(30)
    except WebDriverException,e:
        print e
    if browser is not None:
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://www.hx2car.com/sys/login.htm")
                browser.implicitly_wait(5)              
                #pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        time.sleep(1)
        browser.find_element_by_id('login_name').send_keys(options.username.decode('gb2312'))
        browser.find_element_by_id('password_m').send_keys(options.password)

        browser.find_element_by_class_name('Button4').click()
        time.sleep(5)
        print 'test...'
        #print browser.find_element_by_class_name('fistinfor').find_element_by_tag_name('strong').text
        vehicle_nums = ["32010401000008490000204315","32010401000004250000204317","32010401000008520000204328","32010401000012150000204330","32010401000003590000204324","32010401000003900000204335","32010401000002920000204320","32010401000011450000204327"]
        #vehicle_nums = ["32010401000008490000204315"]
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((vin,brand_initial,brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level,seating_nums),)=get_car_info(vehicle_num)[0]
            else:
                return False
            while True:
                try:
                    if get_publish_page_fails > 10:
                        break
                    browser.get("http://www.hx2car.com/car/addcar.htm")
                    browser.implicitly_wait(5)
                    all_cookies = browser.get_cookies()
                    #pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
                except:
                    get_publish_page_fails += 1
                    print "get page info failed ... ",get_publish_page_fails
                else:
                    break
            time.sleep(5)
            
            # --------------- 车身级别 ---------------------
            printDelimiter()
            print u'车辆种类：',car_level.decode('utf-8')
            car_level_options = browser.find_element_by_id('bigTypeul').find_elements_by_tag_name('a')
            if 'SUV' in car_level:
                for car_level_option in car_level_options:
                    if str(car_level_option.text) == 'SUV':
                        print car_level_option.text
                        car_level_option.click()
                        break
            else:
                for car_level_option in car_level_options:
                    print car_level_option.text
                    car_level_option.click()
                    break
            
            
            # ------------------ brands ---------------------
            printDelimiter()
            print u"品牌首字母:",brand_initial
            print u"品牌:",brand.decode('utf-8')
            print u"车系:",vehicle_series.decode('utf-8')
            print u"车型:",vehicle_model.decode('utf-8')
            browser.execute_script("document.getElementById('car_brand_div').setAttribute('style','display: block;')")
            browser.find_element_by_id('carSrial_0').send_keys(brand.decode('utf-8'))
            time.sleep(0.5)
            try:
                browser.find_element_by_class_name('ac_results').find_element_by_tag_name('li').click()
            except:
                continue
            time.sleep(3)
            
            # ------------------- vehicle_series ------------------------
            vehicle_series_fails = 0
            while True:
                try:
                    if vehicle_series_fails > 5:
                        break
                    browser.execute_script("document.getElementById('car_searial_div').setAttribute('style','display: block;')")
                except:
                    vehicle_series_fails += 1
                    time.sleep(5)
                else:
                    break
                
            get_vehicle_model_fails = 0
            verify_vehicle_serie1 = 0
            verify_vehicle_serie2 = 0
            verify_vehicle_serie3 = 0
            while verify_vehicle_serie1 == 0 and verify_vehicle_serie2 == 0 and verify_vehicle_serie3 == 0 and get_vehicle_model_fails <3:            
                vehicle_series_options = browser.find_element_by_id('car_searial_div').find_element_by_class_name('letterall').find_elements_by_tag_name('a')         
                verify_vehicle_serie_fails = 0
                while verify_vehicle_serie1 == 0 and verify_vehicle_serie2 == 0 and verify_vehicle_serie3 == 0 and verify_vehicle_serie_fails < 5:
                    for vehicle_series_option in vehicle_series_options:
                        if str(vehicle_series_option.text).lower() == vehicle_series.lower():
                            print vehicle_series_option.text
                            vehicle_series_option.click()
                            verify_vehicle_serie1 = 1
                            break
                    if verify_vehicle_serie1 == 0:
                        for vehicle_series_option in vehicle_series_options:
                            if str(vehicle_series_option.text).lower() in vehicle_series.lower():
                                print vehicle_series_option.text
                                vehicle_series_option.click()
                                verify_vehicle_serie2 = 1
                                break
                    if verify_vehicle_serie1 == 0 and verify_vehicle_serie2 == 0:
                        for vehicle_series_option in vehicle_series_options:
                            if vehicle_series.lower() in str(vehicle_series_option.text).lower():
                                print vehicle_series_option.text
                                vehicle_series_option.click()
                                verify_vehicle_serie3 = 1
                                break
                    time.sleep(5)
                    verify_vehicle_serie_fails += 1
                get_vehicle_model_fails += 1
            
            if verify_vehicle_serie1 == 0 and verify_vehicle_serie2 == 0 and verify_vehicle_serie3 == 0:
                if check_exists_by_id(browser, 'brandStr'):
                    browser.find_element_by_id('brandStr').send_keys(vehicle_series.decode('utf-8'))
                else:
                    time.sleep(5)
                    try:
                        browser.find_element_by_id('brandStr').send_keys(vehicle_series.decode('utf-8'))
                    except:
                        continue
            else:
                # -------------------- vehicle model ---------------------------
                if check_exists_by_id(browser, 'typeStr'):
                    try:
                        browser.find_element_by_id('typeStr').send_keys(vehicle_model.decode('utf-8'))
                    except:
                        time.sleep(5)
                        browser.find_element_by_id('typeStr').send_keys(vehicle_model.decode('utf-8'))
                    if check_exists_by_id(browser,'car_type_div_head'):
                        browser.find_element_by_id('car_type_div_head').find_element_by_tag_name('a').click()
                else:
                    time.sleep(3)
                    if check_exists_by_id(browser, 'typeStr'):
                        browser.find_element_by_id('typeStr').send_keys(vehicle_model.decode('utf-8'))
                        if check_exists_by_id(browser,'car_type_div_head'):
                            browser.find_element_by_id('car_type_div_head').find_element_by_tag_name('a').click()
            
              
              
            # ----------------  里程、售价 ------------------------
            printDelimiter()
            print u'里程：',shown_miles
            browser.find_element_by_id('journey').send_keys(shown_miles.decode('utf-8'))
            print u'售价：',owner_price
            browser.find_element_by_id('money').send_keys(str(owner_price))
             
              
              
            # ---------------- 车身颜色 ----------------------------
            printDelimiter()
            print u'车身颜色：',color.decode('utf-8')
            color_verify = ''
            color_options = browser.find_element_by_id('colorul').find_elements_by_tag_name('a')
            for color_option in color_options:
                if color in str(color_option.text):
                    if u'黑色' == str(color_option.text):
                        print "color pass ..."
                        color_verify = u'黑色'
                    else:
                        color_option.click()
                        color_verify = str(color_option.text)
                        print color_option.text
                        break
            if color_verify == '':
                color_options[-1].click()
                print color_options[-1].text
                
            # --------------- 变速箱 --------------------------------
            printDelimiter()
            print u'变速箱类型：',transmission.decode('utf-8')
            transmission_options = browser.find_element_by_id('carAutoul').find_elements_by_tag_name('a')
            for transmission_option in transmission_options:
                if transmission in str(transmission_option.text):
                    if u'自动档' == str(transmission_option.text):
                        print "transmission pass ..."
                    else: 
                        transmission_option.click()
                        print transmission_option.text
                        break
                
            # --------------- 燃油类型 ------------------------------
            printDelimiter()
            print u'燃油类型：',fuel_form.decode('utf-8')
            fuel_form_options = browser.find_element_by_id('oilWearul').find_elements_by_tag_name('a')
            for fuel_form_option in fuel_form_options:
                if fuel_form in str(fuel_form_option.text):
                    if u'汽油' == str(fuel_form_option.text):
                        print "oil pass ..."
                    else:
                        fuel_form_option.click()
                        print fuel_form_option.text
                        break
                elif str(fuel_form_option.text) in fuel_form:
                    if u'汽油' == str(fuel_form_option.text):
                        print "oil pass ..."
                    else:
                        fuel_form_option.click()
                        print fuel_form_option.text
                        break
            

            # ------------- 上牌日期、保险、交强险、商业险 ---------------------
               
            if register_date is not None:
                register_date_year = str(register_date).split('-')[0]
                register_date_month = str(register_date).split('-')[1]
            else:
                register_date_year = ''
                register_date_month = ''
                
            if inspection_date is not None:
                inspection_date_year = str(inspection_date).split('-')[0]
                inspection_date_month = str(inspection_date).split('-')[1]
            else:
                inspection_date_month = ''
                inspection_date_year = ''
            if force_insurance_date is not None:
                force_insurance_date_year = str(force_insurance_date).split('-')[0]
                force_insurance_date_month = str(force_insurance_date).split('-')[1]
            else:
                force_insurance_date_year = ''
                force_insurance_date_month = ''
            if insurance_date is not None:
                insurance_date_year = str(insurance_date).split('-')[0]
                insurance_date_month = str(insurance_date).split('-')[1]
            else:
                insurance_date_year = ''
                insurance_date_month = ''
            # -------------- 首次上牌 ---------------------------
            printDelimiter()
            print u'首次上牌：',register_date
            if register_date is not None:
                browser.execute_script("document.getElementById('useYeardiv').setAttribute('style','display: block;')")
                #browser.find_element_by_id('txtBuyCarDate').click()
                register_date_year_options = browser.find_element_by_id('useYeardiv').find_elements_by_tag_name('a')
                for register_date_year_option in register_date_year_options:
                    if register_date_year in str(register_date_year_option.text):
                        register_date_year_option.click()
                        print register_date_year_option.text
                        break
                
                browser.execute_script("document.getElementById('useMonthdiv').setAttribute('style','display: block;')")     
                register_dates_month_options = browser.find_element_by_id('useMonthdiv').find_elements_by_tag_name('a')
                for register_dates_month_option in register_dates_month_options:
                    if register_date_month[0] == '0':
                        if register_date_month[1] in str(register_dates_month_option.text):
                            register_dates_month_option.click()
                            time.sleep(1)
                            print register_date_month
                            break
                    else:
                        if register_date_month in str(register_dates_month_option.text):
                            register_dates_month_option.click()
                            time.sleep(1)
                            print register_date_month
                            break
                
            # ------------- 补充说明 -------------------------
            printDelimiter()
            #print u"补充说明"
            detail_info = u"""
    淘车乐微信：“南通淘车乐二手车”（微信号：nt930801） ，海量车源在线看。
    淘车乐服务 ：二手车寄售、二手车购买、二手车零首付贷款、二手车评估认证。
    淘车乐地址：南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)
    公交路线 ：可乘坐3路、10路、600路、602路到果园站下车。沿城港路走30米左转进入兴泰路走200米。
    淘车乐，帮您实现有车生活。
            """
            browser.find_element_by_id('desc').send_keys(detail_info.decode('utf-8'))
             
  
            # -------------- 年检有效期 ---------------------------
            printDelimiter()
            print u'年检有效期 ：',inspection_date
            if inspection_date is not None:
                verify_inspection_date = ''
                browser.execute_script("document.getElementById('inspectionYeardiv').setAttribute('style','height: auto; display: block;')")
                inspection_date_year_options = browser.find_element_by_id('inspectionYeardiv').find_elements_by_tag_name('a')
                for inspection_date_year_option in inspection_date_year_options:
                    if inspection_date_year in str(inspection_date_year_option.get_attribute('value')):
                        inspection_date_year_option.click()
                        verify_inspection_date = str(inspection_date_year_option.get_attribute('value'))
                        print inspection_date_year_option.text
                        break
                if verify_inspection_date == '':
                    print "There is no yearly check ..."
                    
                else:
                    browser.execute_script("document.getElementById('inspectionMonthdiv').setAttribute('style','display: block;')")
                    inspection_dates_month_options = browser.find_element_by_id('inspectionMonthdiv').find_elements_by_tag_name('a')
                    for inspection_dates_month_option in inspection_dates_month_options:
                        if inspection_date_month[0] == '0':
                            if inspection_date_month[1] in str(inspection_dates_month_option.get_attribute('value')):
                                inspection_dates_month_option.click()
                                time.sleep(1)
                                print inspection_date_month
                                break
                        else:
                            if inspection_date_month in str(inspection_dates_month_option.get_attribute('value')):
                                inspection_dates_month_option.click()
                                time.sleep(1)
                                print inspection_date_month
                                break
                     
                     
            # -------------- 交强险有效期 ---------------------------
            printDelimiter()
            print u'交强险有效期：',force_insurance_date
            if force_insurance_date is not None:
                verify_force_insurance_date = ''
                browser.execute_script("document.getElementById('insuranceYeardiv').setAttribute('style','height: auto; display: block;')")
                #browser.find_element_by_id('txtExamineExpireDate').click()
                force_insurance_date_year_options = browser.find_element_by_id('insuranceYeardiv').find_elements_by_tag_name('a')
                for force_insurance_date_year_option in force_insurance_date_year_options:
                    if force_insurance_date_year in str(force_insurance_date_year_option.get_attribute('value')):
                        force_insurance_date_year_option.click()
                        verify_force_insurance_date = str(force_insurance_date_year_option.get_attribute('value'))
                        print force_insurance_date_year_option.get_attribute('value')
                        break
                if verify_force_insurance_date == '':
                    print "There is no force insurance check..."
                else:
                    browser.execute_script("document.getElementById('insuranceMonthdiv').setAttribute('style','display: block;')")
                    force_insurance_dates_month_options = browser.find_element_by_id('insuranceMonthdiv').find_elements_by_tag_name('a')
                    for force_insurance_dates_month_option in force_insurance_dates_month_options:
                        if force_insurance_date_month[0] == '0':
                            if force_insurance_date_month[1] in str(force_insurance_dates_month_option.get_attribute('value')):
                                force_insurance_dates_month_option.click()
                                time.sleep(1)
                                print force_insurance_date_month
                                break
                        else:
                            if force_insurance_date_month in str(force_insurance_dates_month_option.get_attribute('value')):
                                force_insurance_dates_month_option.click()
                                time.sleep(1)
                                print force_insurance_date_month
                                break
            
            # -------------------- 过户、按揭 --------------------
            printDelimiter()
            print u"是否可过户：能，是否可按揭：能" 
            #browser.find_element_by_id('transferul').find_element_by_tag_name('a').click()
            browser.find_element_by_id('mortgageul').find_element_by_tag_name('a').click()
            
            # -------------------- 排放类型 ------------------------------
            printDelimiter()
            verify_environmental_standards = 0
            print u'排放类型：',environmental_standards.decode('utf-8')
            environmental_standards_options = browser.find_element_by_id('standardul').find_elements_by_tag_name('a')
            if u'国I' == environmental_standards: 
                for environmental_standards_option in environmental_standards_options:
                    if u'国一' in str(environmental_standards_option.text):
                        environmental_standards_option.click()
                        print environmental_standards_option.text
                        verify_environmental_standards = 1
                        break
            elif u'国II' == environmental_standards:
                for environmental_standards_option in environmental_standards_options:
                    if u'国二' in str(environmental_standards_option.text):
                        environmental_standards_option.click()
                        print environmental_standards_option.text
                        verify_environmental_standards = 1
                        break
            elif u'国III' == environmental_standards:
                for environmental_standards_option in environmental_standards_options:
                    if u'国三' == str(environmental_standards_option.text):
                        environmental_standards_option.click()
                        print environmental_standards_option.text
                        verify_environmental_standards = 1
                        break
            elif u'国III+OBD' == environmental_standards:
                for environmental_standards_option in environmental_standards_options:
                    if u'国三+OBD' == str(environmental_standards_option.text):
                        environmental_standards_option.click()
                        print environmental_standards_option.text
                        verify_environmental_standards = 1
                        break
            elif u'国IV' in environmental_standards:
                for environmental_standards_option in environmental_standards_options:
                    if u'国四' in str(environmental_standards_option.text):
                        environmental_standards_option.click()
                        print environmental_standards_option.text
                        verify_environmental_standards = 1
                        break
            elif u'国V' in environmental_standards:
                for environmental_standards_option in environmental_standards_options:
                    if u'国五' in str(environmental_standards_option.text):
                        environmental_standards_option.click()
                        print environmental_standards_option.text
                        verify_environmental_standards = 1
                        break
            
            # ----------------- 是否同步到百姓、是否用400转接 ----------------------
            browser.find_element_by_id('tobaixing').click()
            browser.find_element_by_id('binding400').click()  
            
            # ----------------- 更多信息 ------------------------------------
            browser.find_element_by_id('openMsg').click()
            # ------------------座位数、有无事故------------------------
            print u"座位数：",seating_nums.decode('utf-8')
            browser.find_element_by_id('seats').send_keys(seating_nums.decode('utf-8'))
            print u"无事故"
            browser.find_element_by_id('wusg').click()
            print u"4S店保养"
            browser.find_element_by_id('4s').click()
            print u"车辆手续"
            browser.find_element_by_id('registration').click()
            browser.find_element_by_id('drivingLicense').click()
            browser.find_element_by_id('taxCertificate').click()
            browser.find_element_by_id('invoice').click()
            browser.find_element_by_id('maintenance').click()
                  
            # ------------- 上传车辆图片 ------------------
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            car_imgs = get_car_info(vehicle_num)[1]
     		# ------------- 1.车辆封面照 ------------------
              
            for i in range(2):
                print car_imgs[i]
                first_element_fails = 0
                while True:
                    if first_element_fails > 5:
                        break
                    if check_exists_by_id(browser,'uploadTd'):
                        image_id = browser.find_element_by_id('uploadTd')
                        try:
                            image_id.find_element_by_tag_name('object').click() 
                        except:
                            time.sleep(5)
                            image_id.find_element_by_tag_name('object').click() 
                        break
                    else:
                        first_element_fails += 1
                        print "load page info failed %d,please wait ..." % first_element_fails
                        time.sleep(3)
                                  
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"打开", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",5)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                time.sleep(3)
                #Click on the Open button
                autoit.ControlClick(u"打开", "","Button1")
                time.sleep(12)
      
            # ------------- 2.卖场二维码 ------------------
            print "two-dimensional bar code"
            print car_imgs[i]
            second_element_fails = 0
            while True:
                if second_element_fails > 5:
                    break
                if check_exists_by_id(browser,'uploadTd'):
                    image_id = browser.find_element_by_id('uploadTd')
                    try:
                        image_id.find_element_by_tag_name('object').click() 
                    except:
                        time.sleep(5)
                        image_id.find_element_by_tag_name('object').click() 
                    break
                else:
                    second_element_fails += 1
                    print "load page info failed %d,please wait ..." % second_element_fails
                    time.sleep(3)        
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",5)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\nantong\\nantong.jpg")
            time.sleep(3)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(12)
               
            if len(car_imgs)>11: 
                for i in range(2,15): 
                    print car_imgs[i]
                    third_element_fails = 0
                    while True:
                        if third_element_fails > 5:
                            break
                        if check_exists_by_id(browser,'uploadTd'):
                            image_id = browser.find_element_by_id('uploadTd')
                            try:
                                image_id.find_element_by_tag_name('object').click()
                            except:
                                time.sleep(5)
                                image_id.find_element_by_tag_name('object').click()
                            break
                        else:
                            third_element_fails += 1
                            print "load page info failed %d,please wait ..." % third_element_fails
                            time.sleep(3)          
                    #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                    autoit.ControlFocus(u"打开", "","Edit1")
                    #Wait 10 seconds for the Upload window to appear
                    autoit.WinWait("[CLASS:#32770]","",5)
                    # Set the File name text on the Edit field
                    autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                    time.sleep(3)
                    #Click on the Open button
                    autoit.ControlClick(u"打开", "","Button1")
                    time.sleep(12)
            else:
                for i in range(2,len(car_imgs)): 
                    print car_imgs[i]
                    third_element_fails = 0
                    while True:
                        if third_element_fails > 5:
                            break
                        if check_exists_by_id(browser,'uploadTd'):
                            image_id = browser.find_element_by_id('uploadTd')
                            try:
                                image_id.find_element_by_tag_name('object').click()
                            except:
                                time.sleep(5)
                                image_id.find_element_by_tag_name('object').click()
                            break
                        else:
                            third_element_fails += 1
                            print "load page info failed %d,please wait ..." % third_element_fails
                            time.sleep(3)                
                    #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                    autoit.ControlFocus(u"打开", "","Edit1")
                    #Wait 10 seconds for the Upload window to appear
                    autoit.WinWait("[CLASS:#32770]","",5)
                    # Set the File name text on the Edit field
                    autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                    time.sleep(3)
                    #Click on the Open button
                    autoit.ControlClick(u"打开", "","Button1")
                    time.sleep(12) 
            
            time.sleep(3)
            print "finished ..... "
            submit_fails = 0
            while True:
                try:
                    if submit_fails > 5:
                        break
                    #browser.find_element_by_class_name('addcar_submit_btn').find_element_by_tag_name('a').submit()
                except:
                    submit_fails += 1
                    time.sleep(5)
                    #browser.find_element_by_class_name('addcar_submit_btn').find_element_by_tag_name('a').submit()
                else:
                    break
            #time.sleep(10)
            #browser.quit()
               


if __name__ == "__main__":   
    post_cardata()
