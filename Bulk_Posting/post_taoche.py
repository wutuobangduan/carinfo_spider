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
    imgurls = ["","C:\\Users\\Administrator\\Desktop\\image\\nantong\\nantong.jpg"]
    try:
        conn = MySQLdb.connect(host='',user='spider',passwd='',charset='utf8')
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
                browser.get("http://i.yiche.com/authenservice/login.aspx")
                browser.implicitly_wait(5)              
                #pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        time.sleep(1)
        browser.find_element_by_id('txt_LoginName').send_keys(options.username.decode('gb2312'))
        browser.find_element_by_id('txt_Password').send_keys(options.password)
        if browser.find_element_by_id('li_code').get_attribute('style') == "display: none;":
            print "There is no need to input validate code ..."
        else:
            validate_code = raw_input("Please input the validate code : ")
            browser.find_element_by_id('txt_Code').send_keys(validate_code.decode('utf-8'))
        
        browser.find_element_by_id('btn_Login').click()
        time.sleep(5)
        print 'test...'
        #print browser.find_element_by_class_name('fistinfor').find_element_by_tag_name('strong').text
#         print browser.find_element_by_class_name('index-4sname').text
        vehicle_nums = ["32010401000008490000204315","32010401000004250000204317","32010401000008520000204328","32010401000012150000204330","32010401000003590000204324","32010401000003900000204335","32010401000002920000204320","32010401000011450000204327"]
        #vehicle_nums = ["32010401000008490000204315"]
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((vin,brand_initial,brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
            else:
                return False
            while True:
                try:
                    if get_publish_page_fails > 10:
                        break
                    browser.get("http://maiche.taoche.com/sellcar/")
                    browser.implicitly_wait(5)
                    all_cookies = browser.get_cookies()
                    #pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
                except:
                    get_publish_page_fails += 1
                    print "get page info failed ... ",get_publish_page_fails
                else:
                    break
            time.sleep(5)
            # ------------------ brands ---------------------
            printDelimiter()
            print u"品牌首字母:",brand_initial
            print u"品牌:",brand.decode('utf-8')
            print u"车系:",vehicle_series.decode('utf-8')
            print u"车型:",vehicle_model.decode('utf-8')
            browser.find_element_by_id('divCarSelect').find_element_by_id('divMasterBrand').find_element_by_tag_name('span').click()
            #browser.execute_script("document.getElementById('Mast_Brand').setAttribute('style','display: block;')")
            time.sleep(3)
            brand_initials = browser.find_element_by_id('Mast_Brand').find_element_by_class_name('pinpzm').find_elements_by_tag_name('a')
            for brand_init in brand_initials:
                if str(brand_init.text) == brand_initial:
                    print brand_init.text
                    brand_init.click()
                    break
                elif str(brand_init.text) in brand_initial:
                    print brand_init.text
                    brand_init.click()
                    break
                elif brand_initial in str(brand_init.text):
                    print brand_init.text
                    brand_init.click()
                    break
            brand_id = "divMasterBrand" + str(brand_initial)
            brand_options = browser.find_element_by_id(brand_id).find_elements_by_tag_name('a')
            verify_brand = 0
            for brand_option in brand_options:
                if brand.lower() in str(brand_option.text).lower():
                    print brand_option.text
                    brand_option.click()
                    verify_brand = 1
                    break
            time.sleep(1)
            if verify_brand == 0:
                continue
            vehicle_series_options = browser.find_element_by_id('divSerial').find_elements_by_tag_name('a')
            first_vehicle_series = 0
            second_vehicle_series = 0
            verify_vehicle_series = 0
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
            vehicle_models_options = browser.find_element_by_id('divCar').find_elements_by_tag_name('a')
            verify_vehicle_models = ''
            transmission_eng = ''
            transmission_verify = ''
            is_exist = 0
            if transmission == '手动':
                transmission_eng = 'MT'
            elif transmission == '自动':
                transmission_eng = 'AT'
            else:
                transmission_verify = '自动'
                transmission_eng = 'AT'
            print transmission,'   ',transmission_eng
            vehicle_models_divs = browser.find_element_by_id('divCar').find_elements_by_class_name('pinp_main_zm')
            for vehicle_models_div in vehicle_models_divs:
                if vehicle_style == str(vehicle_models_div.find_element_by_tag_name('i').text).replace(' ',''):
                    vehicle_models_options = vehicle_models_div.find_elements_by_tag_name('a')
                    for vehicle_models_option in vehicle_models_options:
                        if volume in str(vehicle_models_option.get_attribute('title')):
                            if transmission_verify != '':
                                if transmission in str(vehicle_models_option.get_attribute('title')) or transmission_eng in str(vehicle_models_option.get_attribute('title')) or transmission_verify in str(vehicle_models_option.get_attribute('title')):
                                    print vehicle_models_option.get_attribute('title')
                                    vehicle_models_option.click()
                                    verify_vehicle_models = str(vehicle_models_option.get_attribute('title'))
                                    is_exist = 1 
                                    break
                          
                          
                        else:
                            if transmission in str(vehicle_models_option.get_attribute('title')) or transmission_eng in str(vehicle_models_option.get_attribute('title')):
                                print vehicle_models_option.get_attribute('title')
                                vehicle_models_option.click()
                                verify_vehicle_models = str(vehicle_models_option.get_attribute('title'))
                                is_exist = 1 
                                break
                    if verify_vehicle_models == '':
                        for vehicle_models_option in vehicle_models_options:
                            if volume in str(vehicle_models_option.get_attribute('title')):
                                vehicle_models_option.click()
                                print vehicle_models_option.get_attribute('title')
                                is_exist = 1 
                                break
            if is_exist == 0:
                continue 
             
             
            # ----------------  里程、售价 ------------------------
            printDelimiter()
            print u'里程：',shown_miles
            browser.find_element_by_id('txtDrivingMileage').send_keys(shown_miles.decode('utf-8'))
            print u'售价：',owner_price
            browser.find_element_by_id('txtDisplayPrice').send_keys(str(owner_price))
            browser.find_element_by_id('chkIsIncTransfer').click()
            
             
            # ---------------- 车身颜色 ----------------------------
            printDelimiter()
            print u'车身颜色：',color.decode('utf-8')
            color_verify = ''
            color_options = browser.find_element_by_id('divColor').find_elements_by_tag_name('a')
            for color_option in color_options:
                if color in str(color_option.text):
                    color_option.click()
                    color_verify = str(color_option.text)
                    print color_option.text
                    break
            if color_verify == '':
                color_options[-1].click()
                print color_options[-1].text
                
            # --------------- 车牌所在地 -------------------------------
            printDelimiter()
            print u'车牌所在地：',address.decode('utf-8')
            browser.find_element_by_id('divCityArea').find_element_by_tag_name('span').click()
            province_options = browser.find_element_by_id('divCityArea').find_element_by_class_name('dqleftbox').find_elements_by_tag_name('a')
            for province_option in province_options:
                if u'江苏' == str(province_option.text):
                    province_option.click()
                    break
            city_options = browser.find_element_by_id('divCityArea').find_element_by_class_name('linka_right').find_elements_by_tag_name('a')
            for city_option in city_options:
                if address == str(city_option.text):
                    city_option.click()
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
                #browser.execute_script("document.getElementById('sh_registe_div').setAttribute('style','display: block;')")
                browser.find_element_by_id('txtBuyCarDate').click()
                register_date_year_options = browser.find_element_by_id('divBuyCarDateYear').find_elements_by_tag_name('a')
                for register_date_year_option in register_date_year_options:
                    if register_date_year in str(register_date_year_option.text):
                        register_date_year_option.click()
                        print register_date_year_option.text
                        break
                     
                register_dates_month_options = browser.find_element_by_id('divBuyCarDateMonth').find_elements_by_tag_name('a')
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
            print u"补充说明"
            detail_info = u"""
    淘车乐微信：“南通淘车乐二手车”（微信号：nt930801） ，海量车源在线看。
    淘车乐服务 ：二手车寄售、二手车购买、二手车零首付贷款、二手车评估认证。
    淘车乐地址：南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)
    公交路线 ：可乘坐3路、10路、600路、602路到果园站下车。沿城港路走30米左转进入兴泰路走200米。
    淘车乐，帮您实现有车生活。
            """
            browser.find_element_by_id('txtStateDescription').send_keys(detail_info.decode('utf-8'))
            
            # ------------ 联系人 -------------------------------
            printDelimiter()
            print u"联系人：刘经理"
            browser.find_element_by_id('txtSName').send_keys(u'刘经理')
            
            browser.find_element_by_id('divShowMore').find_element_by_tag_name('span').click()
            
            # -------------- 年检有效期 ---------------------------
            printDelimiter()
            print u'年检有效期 ：',inspection_date
            if inspection_date is not None:
                verify_inspection_date = ''
                #browser.execute_script("document.getElementById('sh_registe_div').setAttribute('style','display: block;')")
                browser.find_element_by_id('txtExamineExpireDate').click()
                inspection_date_year_options = browser.find_element_by_id('divExamineExpireYear').find_elements_by_tag_name('a')
                for inspection_date_year_option in inspection_date_year_options:
                    if inspection_date_year in str(inspection_date_year_option.text):
                        inspection_date_year_option.click()
                        verify_inspection_date = str(inspection_date_year_option.text)
                        print inspection_date_year_option.text
                        break
                if verify_inspection_date == '':
                    inspection_date_year_options[-1].click()
                    print inspection_date_year_options[-1].text
                else:
                    inspection_dates_month_options = browser.find_element_by_id('divExamineExpireMonth').find_elements_by_tag_name('a')
                    for inspection_dates_month_option in inspection_dates_month_options:
                        if inspection_date_month[0] == '0':
                            if inspection_date_month[1] in str(inspection_dates_month_option.text):
                                inspection_dates_month_option.click()
                                time.sleep(1)
                                print inspection_date_month
                                break
                        else:
                            if inspection_date_month in str(inspection_dates_month_option.text):
                                inspection_dates_month_option.click()
                                time.sleep(1)
                                print inspection_date_month
                                break
                    
                    
            # -------------- 交强险有效期 ---------------------------
            printDelimiter()
            print u'交强险有效期：',force_insurance_date
            if force_insurance_date is not None:
                verify_force_insurance_date = ''
                #browser.execute_script("document.getElementById('sh_registe_div').setAttribute('style','display: block;')")
                browser.find_element_by_id('txtExamineExpireDate').click()
                force_insurance_date_year_options = browser.find_element_by_id('divExamineExpireYear').find_elements_by_tag_name('a')
                for force_insurance_date_year_option in force_insurance_date_year_options:
                    if force_insurance_date_year in str(force_insurance_date_year_option.text):
                        force_insurance_date_year_option.click()
                        verify_force_insurance_date = str(force_insurance_date_year_option.text)
                        print force_insurance_date_year_option.text
                        break
                if verify_force_insurance_date == '':
                    force_insurance_date_year_options[-1].click()
                    print force_insurance_date_year_options[-1].text
                else:
                    force_insurance_dates_month_options = browser.find_element_by_id('divExamineExpireMonth').find_elements_by_tag_name('a')
                    for force_insurance_dates_month_option in force_insurance_dates_month_options:
                        if force_insurance_date_month[0] == '0':
                            if force_insurance_date_month[1] in str(force_insurance_dates_month_option.text):
                                force_insurance_dates_month_option.click()
                                time.sleep(1)
                                print force_insurance_date_month
                                break
                        else:
                            if force_insurance_date_month in str(force_insurance_dates_month_option.text):
                                force_insurance_dates_month_option.click()
                                time.sleep(1)
                                print force_insurance_date_month
                                break
            
            # --------------- 定期保养、车辆用途 ----------------------
            printDelimiter()
            browser.find_element_by_id('divMaintainRecord').find_element_by_tag_name('a').click()
            browser.find_element_by_id('divCarType').find_element_by_tag_name('a').click()
            
            # ------------- 上传车辆图片 ------------------
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            car_imgs = get_car_info(vehicle_num)[1]
     		# ------------- 1.车辆封面照 ------------------
             
            for i in range(3):
                print car_imgs[i]
                first_element_fails = 0
                while True:
                    if first_element_fails > 5:
                        break
                    if check_exists_by_id(browser,'flashcon'):
                        photo_id = browser.find_element_by_id('flashcon')
                        try:
                            photo_id.find_element_by_tag_name('object').click() 
                        except:
                            time.sleep(10)
                            photo_id.find_element_by_tag_name('object').click()
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
                time.sleep(5)
    #         
    #         
            # ------------- 2.卖场二维码 ------------------
            print "two-dimensional bar code"
            print car_imgs[i]
            second_element_fails = 0
            while True:
                if second_element_fails > 5:
                    break
                if check_exists_by_id(browser,'flashcon'):
                    photo_id = browser.find_element_by_id('flashcon')
                    try:
                        photo_id.find_element_by_tag_name('object').click() 
                    except:
                        time.sleep(10)
                        photo_id.find_element_by_tag_name('object').click() 
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
            time.sleep(5)
              
            if len(car_imgs)>11: 
                for i in range(3,11): 
                    print car_imgs[i]
                    third_element_fails = 0
                    while True:
                        if third_element_fails > 5:
                            break
                        if check_exists_by_id(browser,'flashcon'):
                            photo_id = browser.find_element_by_id('flashcon')
                            try:
                                photo_id.find_element_by_tag_name('object').click() 
                            except:
                                time.sleep(10)
                                photo_id.find_element_by_tag_name('object').click()
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
                    time.sleep(5)
            else:
                for i in range(3,len(car_imgs)): 
                    print car_imgs[i]
                    third_element_fails = 0
                    while True:
                        if third_element_fails > 5:
                            break
                        if check_exists_by_id(browser,'flashcon'):
                            photo_id = browser.find_element_by_id('flashcon')
                            try:
                                photo_id.find_element_by_tag_name('object').click() 
                            except:
                                time.sleep(10)
                                photo_id.find_element_by_tag_name('object').click()
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
                    time.sleep(5)
             
            time.sleep(3)
            print "finished ..... "
#             #browser.find_element_by_id('btnOK').submit()
#             #time.sleep(10)
#             #browser.quit()
              


if __name__ == "__main__":   
    post_cardata()
