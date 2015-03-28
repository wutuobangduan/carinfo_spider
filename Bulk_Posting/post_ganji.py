# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
from StringIO import StringIO
import gzip
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

#webdriver的模块  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import Select  
from selenium.common.exceptions import NoSuchElementException,WebDriverException,ElementNotVisibleException
import unittest,time,re,os 

from pyvirtualdisplay import Display

from urllib2 import Request,urlopen,URLError,HTTPError


import optparse



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

def get_car_info(vehicle_num):
    imgurls = [""]
    try:
        conn = MySQLdb.connect(host='',user='spider',passwd='',charset='utf8')
        curs = conn.cursor()
        conn.select_db('')
        curs.execute("select (select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address),vmc.vehicle_model_conf53 as environmental_standards,vmc.vehicle_model_conf48 as fuel_form,vmc.vehicle_model_conf5 as car_level  from vehicle_info vi,vehicle_model vm,vehicle_model_conf vmc where vi.vehicle_number='%s' and vm.id=vi.model_id and vmc.id=vi.model_id" % vehicle_num)
        getrows=curs.fetchall()
        if not getrows:
            result = []
        else:
            result = [getrows]

        curs.execute("select imgurl from vehicle_img where vehicle_number='%s'" % vehicle_num)
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

    #print "Usage: post_baixing.py -u yourbxUsername -p yourbxPassword"
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
    
    try:
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        #browser = webdriver.Firefox()
        #browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(30)
    except WebDriverException,e:
        print e
     
    if browser is not None:   
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("https://passport.ganji.com/login.php")
                browser.implicitly_wait(5)
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        
        #browser.find_element_by_id('login_tab_orig').click()
        browser.find_element_by_name('login_username').send_keys(options.username)
        browser.find_element_by_name('login_password').send_keys(options.password)
        #browser.find_element_by_name('setcookie').click()
        #time.sleep(10)
        browser.find_element_by_class_name('submit-box').find_element_by_tag_name('input').click()
        #print browser.find_element_by_id('login-name').text
        time.sleep(12)
        print 'test...'
    vehicle_nums = ["32010401000003900000204335","32010402000002950000204333","32010401000002920000204320","32010402000002720000204323","32010401000003590000204324"]
    for vehicle_num in vehicle_nums:
        if len(get_car_info(vehicle_num)) > 1:
            ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
        else:
            return False
       
        get_login_fails = 0
        while True:
            try:
                if get_login_fails > 10:
                    break
                browser.get("http://www.ganji.com/pub/pub.php?act=pub&method=load&cid=6&mcid=14&domain=nj&h=2&domain=nantong")
                browser.implicitly_wait(5)
                
            except:
                get_login_fails += 1
                print "get page info failed ... ",get_login_fails
            else:
                break
        

        print browser.find_element_by_id('top_banner').find_element_by_class_name('dh').text
        # ------------------ brands ---------------------
        
        printDelimiter()
        print u"品牌:",brand.decode('utf-8')
        print u"车系:",vehicle_series.decode('utf-8')
        print u"车型:",vehicle_model.decode('utf-8')
            #print browser.find_element_by_id('formTb').get_attribute('class')
        #except:
        #    print "raise exception..."
        #    return False
    
        # ------------ get brand name ----------------------------
#         browser.execute_script("document.getElementByClassName('brand  hc').setAttribute('style','z-index: 10; width: 625px; display: block;')")
#         browser.execute_script("document.getElementById('select-A').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-B').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-C').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-D').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-F').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-G').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-H').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-J').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-K').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-L').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-M').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-N').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-O').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-P').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-Q').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-R').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-S').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-T').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-W').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-X').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-Y').setAttribute('style','display:block;')")
#         browser.execute_script("document.getElementById('select-Z').setAttribute('style','display:block;')")
        
#         for brand_list_A in  browser.find_element_by_id('select-A').find_elements_by_tag_name('a'):
#             if brand in brand_list_A.get_attribute('_v'):
#                 brand_list_A.click()
#         for brand_list_X in  browser.find_element_by_id('select-X').find_elements_by_tag_name('a'):
#             if brand in brand_list_X.get_attribute('_v'):
                #browser.execute_script("document.getElementById('minorCategory').setAttribute('type','text')")
                #browser.find_element_by_id('id_minor_category').clear()
                #browser.find_element_by_id('id_minor_category').send_keys(brand.decode('utf-8'))
                #browser.find_element_by_id('id_minor_category').click()
                #browser.find_element_by_id('minorCategory').send_keys(Keys.ENTER)
                #print brand_list_X.get_attribute('_v')
                #brand_list_X.get('http://www.baixing.com/pub/detail_fill@pos=ft_pp@atype=click')
                #browser.execute_script("document.getElementById('minorCategory').setAttribute('value','%s')" % str(brand_list_X.get_attribute('_v')))
                #browser.find_element_by_id('minorCategory').send_keys(Keys.ENTER)
            
                #brand_list_X.click()
        
        browser.find_element_by_id('id_minor_category').clear()
        browser.find_element_by_id('id_minor_category').send_keys(brand.decode('utf-8'))
        try:
            browser.find_element_by_class_name('gj_sys_autoc_rs').find_element_by_tag_name('li').click()
        except:
            continue
        #browser.find_element_by_id('id_minor_category').send_keys(Keys.TAB)
        get_vehicle_series = browser.find_element_by_id('id_tag').find_element_by_class_name('downbox').find_elements_by_tag_name('li')
        first_vehicle_series = 0
        second_vehicle_series = 0
        verify_vehicle_series = 0
        for get_vehicle_serie in get_vehicle_series:
            if str(get_vehicle_serie.text).lower() == vehicle_series.lower() :
                get_vehicle_serie.click()
                first_vehicle_series = 1
                verify_vehicle_series = 1
                break
        if first_vehicle_series == 0:
            for get_vehicle_serie in get_vehicle_series:
                if str(get_vehicle_serie.text).lower()  in vehicle_series.lower() :
                    get_vehicle_serie.click()
                    second_vehicle_series = 1
                    verify_vehicle_series = 1
                    break
        if second_vehicle_series == 0 and first_vehicle_series == 0:
            for get_vehicle_serie in get_vehicle_series:
                if vehicle_series.lower()  in str(get_vehicle_serie.text).lower() :
                    get_vehicle_serie.click()
                    verify_vehicle_series = 1
                    break
        time.sleep(1)
        if verify_vehicle_series == 0:
            continue
        try:
            browser.find_element_by_id('car-input').send_keys(vehicle_model.decode('utf-8'))
            browser.find_element_by_id('car-input').send_keys(Keys.ENTER)
        except:
            print "There is no vehicle_model ..."
        
        
        #browser.find_element_by_id('pinPai').send_keys(brand.decode('utf-8'))
        #browser.find_element_by_id('pinPai').send_keys(Keys.ENTER)
        #browser.find_element_by_id('cheXic').send_keys(vehicle_series.decode('utf-8'))
        #browser.find_element_by_id('cheXic').send_keys(Keys.ENTER)
        #browser.find_element_by_id('cheXing').send_keys(vehicle_model.decode('utf-8'))
        
        #print browser.find_element_by_id('id_燃油类型').text
        
        # --------------------------------------------
        
        printDelimiter()
        print u"车身颜色",color.decode('utf-8')
        color_verify = ''
        browser.execute_script("document.getElementById('id_car_color').childNodes[1].setAttribute('class','comselect active')")
        get_vehicle_colors = browser.find_element_by_id('id_tr_car_color')
        vehicle_colors = get_vehicle_colors.find_element_by_class_name('downbox')
        vehicle_colors_list = vehicle_colors.find_elements_by_tag_name('li')
        for vehicle_color_list in vehicle_colors_list:
            vehicle_colors_a = vehicle_color_list.find_element_by_tag_name('a')
            if color in str(vehicle_colors_a.text):
                color_verify = str(vehicle_colors_a.text)
                print vehicle_colors_a.text
                vehicle_colors_a.click()
                time.sleep(3)
                break
        if color_verify == '':
            vehicle_colors_list[-1].find_element_by_tag_name('a').click()
            time.sleep(3)
            		
        # ----------- transmissions -------------------
        printDelimiter()
        print u"变速箱:",transmission.decode('utf-8')
        verify_transmission = ''
        get_transmissions = browser.find_element_by_id('id_tr_gearbox')
        transmissions = get_transmissions.find_elements_by_tag_name('label')
        for transmission_option in transmissions:
            if str(transmission_option.text) == transmission:
                transmission_option.find_element_by_tag_name('input').click()
                verify_transmission = str(transmission_option.text)
                print transmission_option.text
                break
        if verify_transmission == '':
            transmissions[-1].find_element_by_tag_name('input').click()
         
        
        
        # ----------- color ---------------------------
        printDelimiter()
        print u"有无事故:无"
        browser.find_element_by_id('id_accidents_0').click()
        
   
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

        # -------------- 首次上牌 ---------------
        printDelimiter()
        print u"首次上牌:",register_date
        register_date_i = 1
        if register_date is not None: 
            # --------- 上牌年份 -------------------
            printDelimiter()
            browser.execute_script("document.getElementById('id_license_date').setAttribute('class','comselect active')")
            get_register_dates_years = browser.find_element_by_id('id_license_date')
        
            register_dates_year = get_register_dates_years.find_element_by_class_name('downbox')
            register_dates_year_options = register_dates_year.find_elements_by_tag_name('li')
            for register_dates_year_option in register_dates_year_options:
                if str(register_dates_year_option.find_element_by_tag_name('a').text) == register_date_year:
                    register_dates_year_option.find_element_by_tag_name('a').click()
                    time.sleep(3)
                    print register_date_year
                    break
            
            # --------- 上牌月份 -------------------
            printDelimiter()
            browser.execute_script("document.getElementById('id_license_math').setAttribute('class','comselect active')")
            get_register_dates_months = browser.find_element_by_id('id_license_math')
            
            register_dates_month = get_register_dates_months.find_element_by_class_name('downbox')
            register_dates_month_options = register_dates_month.find_elements_by_tag_name('li')
            for register_dates_month_option in register_dates_month_options:
                if register_date_month[0] == '0':
                    if str(register_dates_month_option.find_element_by_tag_name('a').text) == register_date_month[1]:
                        register_dates_month_option.find_element_by_tag_name('a').click()
                        time.sleep(3)
                        print register_date_month
                        break
                else:
                    if str(register_dates_month_option.find_element_by_tag_name('a').text) == register_date_month:
                        register_dates_month_option.find_element_by_tag_name('a').click()
                        time.sleep(3)
                        print register_date_month
                        break

        # ------------- 年检到期 ---------------------
        printDelimiter()
        print u"年检到期:",inspection_date
        verify_inspection_date = ''
        if inspection_date is not None:
            # --------- 年检年份 -------------------
            printDelimiter()
            browser.execute_script("document.getElementById('id_insurance_year').setAttribute('class','comselect active')")
            get_inspection_dates_years = browser.find_element_by_id('id_insurance_year')
#             print get_register_dates.find_element_by_tag_name('input').get_attribute('value')
#             print get_register_dates.find_element_by_tag_name('input').get_attribute('class')
#             
            inspection_dates_year = get_inspection_dates_years.find_element_by_class_name('downbox')
            inspection_dates_year_options = inspection_dates_year.find_elements_by_tag_name('li')
            for inspection_dates_year_option in inspection_dates_year_options:
                if str(inspection_dates_year_option.find_element_by_tag_name('a').text) == inspection_date_year:
                    inspection_dates_year_option.find_element_by_tag_name('a').click()
                    time.sleep(3)
                    verify_inspection_date = inspection_date_year
                    print inspection_date_year
                    break
            
            # --------- 年检月份 -------------------
            printDelimiter()
            browser.execute_script("document.getElementById('id_insurance_month').setAttribute('class','comselect active')")
            get_inspection_dates_months = browser.find_element_by_id('id_insurance_month')
            
            inspection_dates_month = get_inspection_dates_months.find_element_by_class_name('downbox')
            inspection_dates_month_options = inspection_dates_month.find_elements_by_tag_name('li')
            for inspection_dates_month_option in inspection_dates_month_options:
                if inspection_date_month[0] == '0':
                    if str(inspection_dates_month_option.find_element_by_tag_name('a').text) == inspection_date_month[1]:
                        inspection_dates_month_option.find_element_by_tag_name('a').click()
                        time.sleep(3)
                        print inspection_date_month
                        break
                else:
                    if str(inspection_dates_month_option.find_element_by_tag_name('a').text) == inspection_date_month:
                        inspection_dates_month_option.find_element_by_tag_name('a').click()
                        time.sleep(3)
                        print inspection_date_month
                        break
            
            if verify_inspection_date == '':
                browser.find_element_by_id('insurance').click()
                time.sleep(3)
                
            
         
        # ------------- 交强险到期 ---------------------
        printDelimiter()
        verify_force_insurance_date = ''
        print u"交强险到期:",force_insurance_date
        if force_insurance_date is not None:
            # --------- 交强险年份 -------------------
            printDelimiter()
            browser.execute_script("document.getElementById('id_strong_insurance_year').setAttribute('class','comselect active')")
            get_force_insurance_dates_years = browser.find_element_by_id('id_strong_insurance_year')
        
            force_insurance_dates_year = get_force_insurance_dates_years.find_element_by_class_name('downbox')
            force_insurance_dates_year_options = force_insurance_dates_year.find_elements_by_tag_name('li')
            for force_insurance_dates_year_option in force_insurance_dates_year_options:
                if str(force_insurance_dates_year_option.find_element_by_tag_name('a').text) == force_insurance_date_year:
                    force_insurance_dates_year_option.find_element_by_tag_name('a').click()
                    time.sleep(3)
                    verify_force_insurance_date = force_insurance_date_year
                    print force_insurance_date_year
                    break
            
            # --------- 交强险月份 -------------------
            printDelimiter()
            browser.execute_script("document.getElementById('id_strong_insurance_month').setAttribute('class','comselect active')")
            get_force_insurance_dates_months = browser.find_element_by_id('id_strong_insurance_month')
            
            force_insurance_dates_month = get_force_insurance_dates_months.find_element_by_class_name('downbox')
            force_insurance_dates_month_options = force_insurance_dates_month.find_elements_by_tag_name('li')
            for force_insurance_dates_month_option in force_insurance_dates_month_options:
                if force_insurance_date_month[0] == '0':
                    if str(force_insurance_dates_month_option.find_element_by_tag_name('a').text) == force_insurance_date_month[1]:
                        force_insurance_dates_month_option.find_element_by_tag_name('a').click()
                        time.sleep(3)
                        print force_insurance_date_month
                        break
                else:
                    if str(force_insurance_dates_month_option.find_element_by_tag_name('a').text) == force_insurance_date_month:
                        force_insurance_dates_month_option.find_element_by_tag_name('a').click()
                        time.sleep(3)
                        print force_insurance_date_month
                        break
            
            if verify_force_insurance_date == '':
                browser.find_element_by_id('strong_insurance').click()
                time.sleep(3)
                
        
        # ------------- 行驶里程 ---------------------
        printDelimiter()
        print u"行驶里程:",shown_miles
        browser.find_element_by_id('id_tr_road_haul').find_element_by_tag_name('input').send_keys(shown_miles.decode('utf-8'))
        print u"车主报价:",owner_price
        browser.find_element_by_id('id_tr_price').find_element_by_tag_name('input').send_keys(str(owner_price))
        browser.find_element_by_id('id_transfer_fee').click()
        
        # ------------- 一句话广告 ----------------------
        printDelimiter()
        advertisement = u"淘车乐认证首付30%"
        print u"一句话广告:",advertisement
        browser.find_element_by_id('id_ad_title').send_keys(advertisement.decode('utf-8'))
        
        # ------------- 补充说明 -------------------------
        printDelimiter()
        print u"补充说明"
        detail_info = u"""
   淘车乐微信：“南通淘车乐二手车”（微信号：nt930801） ，海量车源在线看。
   淘车乐服务 ：二手车寄售、二手车购买、二手车零首付贷款、二手车评估认证。
   淘车乐地址：南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)
  公交路线 ：可乘坐3路、10路、600路、602路到果园站下车。沿城港路走30米左转进入兴泰路走200米。
  淘车乐，帮您实现有车生活。"""
        browser.find_element_by_id('id_description').send_keys(detail_info.decode('utf-8'))
        
        # ------------- 联系人、联系方式 -------------------------
        printDelimiter()
        print u"联系人、联系方式"
        contact_person = '南通淘车乐'
        contact_telephone = '17712233652'
        browser.find_element_by_name('person').send_keys(contact_person.decode('utf-8'))
        browser.find_element_by_id('id_agent_1').click()
        browser.find_element_by_id('id_phone').send_keys(contact_telephone.decode('utf-8'))
        
        # -------------- 看出地点 -----------------------------
        printDelimiter()
        print u"看车地点"
        address_options = browser.find_element_by_id('id_district_id').find_elements_by_tag_name('option')
        for address_option in address_options:
            if str(address_option.text) == u'港闸':
                address_option.click()
                break
        
        
        
        
        # ------------- 上传车辆图片 ------------------
        autoit = win32com.client.Dispatch("AutoItX3.Control")
        car_imgs = get_car_info(vehicle_num)[1]
		# ------------- 1.车辆封面照 ------------------
        for i in range(0,2):
            print car_imgs[i]
            browser.find_element_by_id('SWFUpload_0').click()
            
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",5)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
            time.sleep(2)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(8)
        
        
        # ------------- 2.卖场二维码 ------------------
        print "two-dimensional bar code"
        browser.find_element_by_id('SWFUpload_0').click()
        #ControlFocus("title","text",controlID) Edit1=Edit instance 1
        autoit.ControlFocus(u"打开", "","Edit1")
        #Wait 10 seconds for the Upload window to appear
        autoit.WinWait("[CLASS:#32770]","",5)
        # Set the File name text on the Edit field
        autoit.ControlSetText(u"打开", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\nantong\\nantong.jpg")
        time.sleep(2)
        #Click on the Open button
        autoit.ControlClick(u"打开", "","Button1")
        time.sleep(8)
        
        if len(car_imgs)>15:
            for i in range(2,15):
                print car_imgs[i]
                browser.find_element_by_id('SWFUpload_0').click()
                
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"打开", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",5)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                time.sleep(2)
                #Click on the Open button
                autoit.ControlClick(u"打开", "","Button1")
                time.sleep(8)
        else:
            for i in range(2,len(car_imgs)):
                print car_imgs[i]
                browser.find_element_by_id('SWFUpload_0').click()
                
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"打开", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",5)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                time.sleep(2)
                #Click on the Open button
                autoit.ControlClick(u"打开", "","Button1")
                time.sleep(8)
		
       
        #return True
        time.sleep(5)
        print "finished ..... "
        #browser.find_element_by_id('pub_submit').submit()
        #time.sleep(10)
        #browser.quit()
        


if __name__ == "__main__":   
    #loginTobaixing()
    post_cardata()
