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
import time

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
        conn = MySQLdb.connect(host='',user='spider',passwd='spider',charset='utf8')
        curs = conn.cursor()
        conn.select_db('')
        curs.execute("select vi.vin,(select d.field_value from data_dictionary d where d.id=(select dd.parent_id from data_dictionary dd where dd.id=vm.brand)),(select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address),vmc.vehicle_model_conf53 as environmental_standards,vmc.vehicle_model_conf48 as fuel_form,vmc.vehicle_model_conf5 as car_level  from vehicle_info vi,vehicle_model vm,vehicle_model_conf vmc where vi.vehicle_number='%s' and vm.id=vi.model_id and vmc.id=vi.model_id" % vehicle_nums)
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
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        browser.implicitly_wait(5)
        browser.set_page_load_timeout(30)
    except WebDriverException,e:
        print e
    if browser is not None:
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://2sc.sohu.com/ctb/")
                browser.implicitly_wait(5)              
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        time.sleep(1)
        browser.find_element_by_id('passport').send_keys(options.username.decode('gb2312'))
        browser.find_element_by_id('passwd').send_keys(options.password)        
        browser.find_element_by_id('isRemember').click()
        browser.find_element_by_class_name('dlbtn').click()
        time.sleep(8)
        print 'test...'
        try:
            print browser.find_element_by_class_name('ctbtop').find_element_by_tag_name('h2').text
        except:
            time.sleep(2)
            print "the page is loaded too slow,continue ..."
        vehicle_nums = ["32050501000006730000204012","32050501000007480000204898","32050501000007480000204900","32050501000007480000204905","32050501000009060000204539","32050501000006290000204531","32050501000006290000204561","32050501000006290000204569","32050501000006230000204359","32050501000006290000204568","32050501000006460000204366"]
        #vehicle_nums = ["32010401000008520000204328"]
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((vin,brand_initial,brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
            else:
                return False
             
             
            while True:
                try:
                    if get_publish_page_fails > 10:
                        break
                    browser.get("http://2sc.sohu.com/ctb/uscar-carAdd.do")
                    browser.implicitly_wait(5)
                    wait = ui.WebDriverWait(browser,30)
                except:
                    get_publish_page_fails += 1
                    print "get page info failed ... ",get_publish_page_fails
                else:
                    break
             
#             # ------------------ vin ------------------------
#             print "vin is : ",vin.decode('utf-8')
#             browser.find_element_by_id('carVIN').send_keys(vin.decode('utf-8'))
            time.sleep(2) 
            # ------------------ brands ---------------------
            printDelimiter()
            print u"品牌首字母:",brand_initial
            print u"品牌:",brand.decode('utf-8')
            print u"车系:",vehicle_series.decode('utf-8')
            print u"车型:",vehicle_model.decode('utf-8')
            try: 
                #browser.execute_script("document.getElementsByClassName('menu-list select-brand').setAttribute('style','display: block; height: 376px;')")
                browser.find_element_by_id('selBrandSpan').click()
            except:
                print "can not open the brand list ..."
                continue
            time.sleep(2)
            brand_lists = browser.find_element_by_class_name('car-list').find_elements_by_tag_name('li')
            verify_brand = 0
            first_brand = 0
            second_brand = 0
            for brand_list in brand_lists:
                if str(brand_list.find_element_by_tag_name('i').text) == brand_initial:
                    brand_options = brand_list.find_elements_by_tag_name('a')     
                    for brand_option in brand_options:
                        if str(brand_option.text).lower() == brand.lower():
                            print brand_option.text
                            verify_brand = 1
                            brand_option.click()
                            first_brand = 1
                            break
                    if first_brand == 0:
                        for brand_option in brand_options:
                            if str(brand_option.text).lower() in brand.lower():
                                print brand_option.text
                                verify_brand = 1
                                brand_option.click()
                                second_brand = 1
                                break
                    if first_brand == 0 and second_brand == 0:
                        for brand_option in brand_options:
                            if brand.lower() in str(brand_option.text).lower():
                                print brand_option.text
                                verify_brand = 1
                                brand_option.click()
                                break
            time.sleep(2)
            if verify_brand == 0:
                continue
            
            # ----------------- vehicle series ----------------------
            wait.until(EC.element_to_be_clickable((By.ID,'selModelSpan')))
            try:
                browser.find_element_by_id('selModelSpan').click()
            except:
                print "can not open the vehicle series list ... "
                continue
            
            first_vehicle_series = 0
            second_vehicle_series = 0
            verify_vehicle_series = 0
            vehicle_series_options = browser.find_element_by_id('modelLayer').find_elements_by_tag_name('a')
            for vehicle_series_option in vehicle_series_options:
                if str(vehicle_series_option.text).lower() == vehicle_series.lower():
                    print vehicle_series_option.text
                    vehicle_series_option.click()
                    first_vehicle_series = 1
                    verify_vehicle_series = 1
                    break
            if first_vehicle_series == 0:
                for vehicle_series_option in vehicle_series_options:
                    if str(vehicle_series_option.text).lower() in vehicle_series.lower():
                        print vehicle_series_option.text
                        vehicle_series_option.click()
                        second_vehicle_series = 1
                        verify_vehicle_series = 1
                        break
            if first_vehicle_series == 0 and second_vehicle_series == 0:
                for vehicle_series_option in vehicle_series_options:
                    if vehicle_series.lower() in str(vehicle_series_option.text).lower():
                        print vehicle_series_option.text
                        vehicle_series_option.click()
                        verify_vehicle_series = 1
                        break
            time.sleep(1)
            if verify_vehicle_series == 0:
                continue
            # ------------------- vehicle model ------------------------------
            wait.until(EC.element_to_be_clickable((By.ID,'tohand')))
            try:
                browser.find_element_by_id('tohand').click()
            except:
                print "can not open the input window ..."
                continue
            time.sleep(3)
            browser.find_element_by_id('handYearValue').send_keys(vehicle_model.decode('utf-8'))

            # ---------------- 车身颜色 ----------------------------
            printDelimiter()
            print u'车身颜色：',color.decode('utf-8')
            wait.until(EC.element_to_be_clickable((By.ID,'tohandcolor')))
            browser.find_element_by_id('tohandcolor').click()
            time.sleep(2)
            browser.find_element_by_id('handColorValue').send_keys(color.decode('utf-8'))
            
            # ---------------- 排量 ----------------------------------
            printDelimiter()
            print u'排量：',volume.decode('utf-8')
            wait.until(EC.element_to_be_clickable((By.ID,'tohandpailiang')))
            browser.find_element_by_id('tohandpailiang').click()
            time.sleep(2)
            browser.find_element_by_id('handpailingValue').send_keys(volume.decode('utf-8')[:-1])
            if volume.decode('utf-8')[-1] == "T":
                browser.find_element_by_id('jinqi').click()
            
            # ----------------- 变速箱 ---------------------------------
            printDelimiter()
            print u'变速箱：',transmission.decode('utf-8')
            transmission_options = browser.find_element_by_id('transmission').find_elements_by_tag_name('a')
            if transmission == '手动':
                transmission_options[1].click()
            else:
                transmission_options[0].click()
                
            # ----------------- 车辆所在地 --------------------------------
            printDelimiter()
            province = u"江苏"
            city = u"苏州"
            print u'省份：%s,城市：%s' % (province,city)
            browser.find_element_by_id('carProvince').find_element_by_class_name('menu-name').click()
            time.sleep(2)
            province_options = browser.find_element_by_id('carProvince').find_elements_by_tag_name('a')
            for province_option in province_options:
                if province in str(province_option.text):
                    province_option.click()
                    print province_option.text
                    break
            time.sleep(2)
            browser.find_element_by_id('carCity').find_element_by_class_name('menu-name').click()
            time.sleep(2)
            city_options = browser.find_element_by_id('carCity').find_elements_by_tag_name('a')
            for city_option in city_options:
                if city in str(city_option.text):
                    city_option.click()
                    print city_option.text
                    break
                
             
            # ----------------  里程、售价 ------------------------
            printDelimiter()
            print u'里程：',shown_miles
            browser.find_element_by_id('mileage').clear()
            browser.find_element_by_id('mileage').send_keys(str(float(shown_miles.decode('utf-8'))*10000).split('.')[0])
            print u'售价：',owner_price
            browser.find_element_by_id('sale_price').clear()
            browser.find_element_by_id('sale_price').send_keys(str(owner_price))
            browser.find_element_by_id('transfer_fee_flag').click()
             
            # ----------------- 购买来源、车辆使用性质、保养记录、外观成色、内饰状况 ------------------------------
            printDelimiter()
            print u'购买来源：新车,车辆使用性质：非运营'
            browser.find_element_by_id('carsource').find_elements_by_tag_name('a')[0].click()
            browser.find_element_by_id('carnuture').find_elements_by_tag_name('a')[0].click()
            browser.find_element_by_id('carmaintain').find_elements_by_tag_name('a')[0].click()
            browser.find_element_by_id('carinterior').find_elements_by_tag_name('a')[0].click()
            
            
             
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
                #browser.execute_script("document.getElementById('sh_registe_div').setAttribute('style','display: block;')")
                browser.find_element_by_id('firstTimeYear').find_element_by_class_name('menu-name').click()
                time.sleep(2)
                register_date_year_options = browser.find_element_by_id('firstTimeYear').find_elements_by_tag_name('a')
                for register_date_year_option in register_date_year_options:
                    if register_date_year in str(register_date_year_option.text):
                        register_date_year_option.click()
                        print register_date_year_option.text
                        break
                
                browser.find_element_by_id('firstTimeMonth').find_element_by_class_name('menu-name').click()
                time.sleep(2)     
                register_dates_month_options = browser.find_element_by_id('firstTimeMonth').find_elements_by_tag_name('a')
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
            else:
                browser.find_element_by_id('firstTimeYear').find_element_by_class_name('menu-name').click()
                time.sleep(2)
                try:
                    browser.find_element_by_id('firstTimeYear').find_elements_by_tag_name('a')[1].click()
                except:
                    print "can not select the register date..."
                    continue
            
            
              
            # ------------- 补充说明 -------------------------
            printDelimiter()
            print u"补充说明"
            detail_info = u"""    淘车乐微信：“南通淘车乐二手车”（微信号：nt930801） ，海量车源在线看。
    淘车乐服务 ：二手车寄售、二手车购买、二手车零首付贷款、二手车评估认证。
    淘车乐地址：南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)
    公交路线 ：可乘坐3路、10路、600路、602路到果园站下车。沿城港路走30米左转进入兴泰路走200米。
    淘车乐，帮您实现有车生活。"""
            browser.find_element_by_id('remark').send_keys(detail_info.decode('utf-8'))
            print u"一句话广告"
            browser.find_element_by_id('onewordad').send_keys(u'淘车乐认证首付30%')
          
            # -------------- 外观成色 ----------------------------
            printDelimiter()
            print u"外观成色"
            if register_date is not None:
                if int(register_date_year) >= time.localtime()[0]-1:
                    browser.find_element_by_id('carlook').find_elements_by_tag_name('a')[0].click()
                else:
                    browser.find_element_by_id('carlook').find_elements_by_tag_name('a')[1].click()
            
            # ---------------选择店铺及联系方式 ----------------------------
            printDelimiter()
            print u"店铺及联系方式。。"  
            browser.find_element_by_id('address-list').find_elements_by_tag_name('input')[0].click()
            browser.find_element_by_id('salesman-list').find_elements_by_tag_name('input')[0].click()
            
            # ------------- 上传车辆图片 ------------------
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            car_imgs = get_car_info(vehicle_num)[1]
     		
            for i in range(len(car_imgs)): 
                print car_imgs[i]
                wait.until(EC.element_to_be_clickable((By.ID,'SWFUpload_0')))
                browser.find_element_by_id('SWFUpload_0').click()
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
                time.sleep(5)
             
            time.sleep(3)
            print "finished ..... "
#             try:
#                 browser.find_element_by_id('submitInfoBtn').submit()
#             except:
#                 time.sleep(5)
#                 browser.find_element_by_id('submitInfoBtn').submit()
#                 
#             #time.sleep(10)
#             #browser.quit()
              


if __name__ == "__main__":   
    post_cardata()
