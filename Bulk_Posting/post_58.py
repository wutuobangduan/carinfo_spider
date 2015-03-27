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
from selenium.common.exceptions import NoSuchElementException,WebDriverException,StaleElementReferenceException
import unittest,time,re,os 

from pyvirtualdisplay import Display

from urllib2 import Request,urlopen,URLError,HTTPError

import optparse

from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0



#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;



def get_car_info(vehicle_num):
    imgurls = []
    try:
        conn = MySQLdb.connect(host='',user='',passwd='',charset='utf8')
        curs = conn.cursor()
        conn.select_db('')
        curs.execute("select (select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address),vmc.vehicle_model_conf53 as environmental_standards,vmc.vehicle_model_conf48 as fuel_form,vmc.vehicle_model_conf5 as car_level  from vehicle_info vi,vehicle_model vm,vehicle_model_conf vmc where vi.vehicle_number='%s' and vm.id=vi.model_id and vmc.id=vi.model_id" % vehicle_num)
        getrows=curs.fetchall()
        if not getrows:
            result = []
        else:
            #print getrows
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
    get_post_fails = 0
    try:
#         chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
#         os.environ["webdriver.chrome.driver"] = chromedriver
#         browser = webdriver.Chrome(chromedriver)
        browser = webdriver.Ie(executable_path="C:\Program Files\Internet Explorer\IEDriverServer.exe")
        
        #browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
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
                browser.get("http://passport.58.com/login")
                browser.implicitly_wait(10)
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        #time.sleep(5)
        try:
            browser.find_element_by_id('login_tab_orig').click()
            time.sleep(0.5)
            browser.find_element_by_id('username').send_keys(options.username.decode('gb2312'))
            browser.find_element_by_id('password').send_keys(options.password)
            browser.find_element_by_id('coks').click()
            browser.find_element_by_id('btnSubmit').click()
            time.sleep(5)
        except:
            print "there is no need to login..."
            print browser.find_element_by_id('login-name').text
        
        print 'test...'
        print browser.find_element_by_id('login').text
        
        vehicle_nums = ["32010401000003900000204335","32010402000002950000204333","32010401000002920000204320","32010402000002720000204323","32010401000003590000204324"]
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
            else:
                return False
            while True:
                try:
                    if get_post_fails > 10:
                        break
                    browser.get("http://post.58.com/172/29/s5")
                    browser.implicitly_wait(10)
                    wait = ui.WebDriverWait(browser,30)
                except:
                    get_post_fails += 1
                    print "get page info failed ... ",get_post_fails
                else:
                    break
            time.sleep(5)
            # ------------------ brands ---------------------
            printDelimiter()
            print u"品牌:",brand.decode('utf-8')
            print u"车系:",vehicle_series.decode('utf-8')
            print u"车型:",vehicle_model.decode('utf-8')
            #wait.until(lambda browser: browser.find_element_by_id('pinPai'))
            browser.find_element_by_id('pinPai').clear()
            browser.find_element_by_id('pinPai').send_keys(brand.decode('utf-8'))
            
            time.sleep(5)
            try:
                browser.find_element_by_id('Searchitem').find_element_by_tag_name('a').click()
            except:
                continue
            time.sleep(3)
            #wait.until(lambda browser: browser.find_element_by_id('cheXiWin'))
                    
            get_vehicle_series = browser.find_element_by_id('chexiFidercon')
            get_vehicle_series_dd = get_vehicle_series.find_elements_by_tag_name('dd')
            #vehicle_series = u'伊兰特'.encode('utf-8')
            first_vehicle_series = 0
            second_vehicle_series = 0
            for get_vehicle_serie_dd in  get_vehicle_series_dd[1:]:
                print get_vehicle_serie_dd.find_element_by_tag_name('a').text
                print chardet.detect(str(get_vehicle_serie_dd.find_element_by_tag_name('a').text))
                if str(get_vehicle_serie_dd.find_element_by_tag_name('a').text).lower() == vehicle_series.lower():
                    get_vehicle_serie_dd.find_element_by_tag_name('a').click()
                    first_vehicle_series = 1
                    break
            if first_vehicle_series == 0:
                for get_vehicle_serie_dd in  get_vehicle_series_dd[1:]:
                    print get_vehicle_serie_dd.find_element_by_tag_name('a').text
                    print chardet.detect(str(get_vehicle_serie_dd.find_element_by_tag_name('a').text))
                    if str(get_vehicle_serie_dd.find_element_by_tag_name('a').text).lower() in vehicle_series.lower():
                        get_vehicle_serie_dd.find_element_by_tag_name('a').click()
                        second_vehicle_series = 1
                        break
            if second_vehicle_series == 0 and  first_vehicle_series == 0:
                for get_vehicle_serie_dd in  get_vehicle_series_dd[1:]:
                    print get_vehicle_serie_dd.find_element_by_tag_name('a').text
                    print chardet.detect(str(get_vehicle_serie_dd.find_element_by_tag_name('a').text))
                    if vehicle_series.lower() in str(get_vehicle_serie_dd.find_element_by_tag_name('a').text).lower():
                        get_vehicle_serie_dd.find_element_by_tag_name('a').click()
                        break
            time.sleep(1)
            try:
                browser.find_element_by_id('cheXing').clear()
                browser.find_element_by_id('cheXing').send_keys(vehicle_model.decode('utf-8'))
            except:
                time.sleep(2)
                print "There is no vehicle model exists ..."
            #browser.find_element_by_id('cheXing').send_keys(Keys.ENTER)
    
            # --------------------------------------------
             
            printDelimiter()
            print u"车身颜色",color.decode('utf-8')
            color_verify = ''
            browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
            time.sleep(3)
            #wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'p_yanse')))           
            get_vehicle_colors = browser.find_element_by_name('yanse_xianshi')
            vehicle_colors = get_vehicle_colors.find_elements_by_tag_name('span')
            get_color_fails = 0
            if len(vehicle_colors) < 17:
                browser.switch_to.default_content()
                time.sleep(5)
                browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
                time.sleep(2)
                vehicle_colors = browser.find_element_by_name('yanse_xianshi').find_elements_by_tag_name('span')
            while True:
                try:
                    if get_color_fails > 5:
                        break
                    for vehicle_color in vehicle_colors:   
                        if color in str(vehicle_color.text):
                            color_verify = str(vehicle_color.text)
                            print vehicle_color.text
                            vehicle_color.click()
                            time.sleep(3)
                            break
                        elif str(vehicle_color.text) in color:
                            color_verify = str(vehicle_color.text)
                            print vehicle_color.text
                            vehicle_color.click()
                            time.sleep(3)
                            break
                except:
                    time.sleep(2)
                    get_color_fails += 1
                    print "select color again ... ",get_color_fails
                    browser.switch_to.default_content()
                    time.sleep(3)
                    browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
                    time.sleep(2)
                    vehicle_colors = browser.find_element_by_name('yanse_xianshi').find_elements_by_tag_name('span')
                else:
                    break
            if color_verify == '':
                while True:
                    try:
                        if get_color_fails > 8:
                            break
                        vehicle_colors[-1].click()
                        time.sleep(3)
                    except:
                        get_color_fails += 1
                        browser.switch_to.default_content()
                        time.sleep(5)
                        browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
                        time.sleep(2)
                        vehicle_colors = browser.find_element_by_name('yanse_xianshi').find_elements_by_tag_name('span')
                    else:
                        break
            browser.switch_to.default_content()
            time.sleep(2)
    
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
     
            # -------------- 首次上牌 ---------------
            printDelimiter()
            browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
            time.sleep(2)
            print u"首次上牌:",register_date
            if register_date is not None: 
                # --------- 上牌年份 -------------------
                get_register_dates_years = browser.find_element_by_name('y_shangpai')       
                register_dates_year_options = get_register_dates_years.find_elements_by_tag_name('option')
                for register_dates_year_option in register_dates_year_options:
                    if str(register_dates_year_option.text) == register_date_year:
                        register_dates_year_option.click()
                        time.sleep(3)
                        print register_date_year
                        break
                 
                # --------- 上牌月份 -------------------
                get_register_dates_months = browser.find_element_by_name('m_shangpai')
                register_dates_month_options = get_register_dates_months.find_elements_by_tag_name('option')
                for register_dates_month_option in register_dates_month_options:
                    if register_date_month[0] == '0':
                        if str(register_dates_month_option.text) == register_date_month[1]:
                            register_dates_month_option.click()
                            time.sleep(3)
                            print register_date_month
                            break
                    else:
                        if str(register_dates_month_option.text) == register_date_month:
                            register_dates_month_option.click()
                            time.sleep(3)
                            print register_date_month
                            break
            browser.switch_to.default_content()
            time.sleep(2)
    
            # ------------- 是否保养 ---------------------------
            printDelimiter()
            browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
            time.sleep(2)
            print u"是否保养：是,有无事故：无"
            browser.find_element_by_name('p_baoyang').find_element_by_tag_name('span').click()
            browser.find_element_by_name('p_shiguqk').find_element_by_tag_name('span').click()
            browser.switch_to.default_content()
            time.sleep(2)
            
            # ------------- 年检到期 ---------------------
            printDelimiter()
            browser.switch_to.frame(browser.find_element_by_id('carframe_id'))
            time.sleep(2)
            print u"年检到期:",inspection_date
            verify_inspection_date = ''
            if inspection_date is not None:
                # --------- 年检年份 -------------------
                printDelimiter()
                get_inspection_dates_years = browser.find_element_by_name('y_nianjian')
                inspection_dates_year_options = get_inspection_dates_years.find_elements_by_tag_name('option')
                for inspection_dates_year_option in inspection_dates_year_options:
                    if str(inspection_dates_year_option.text) == inspection_date_year:
                        inspection_dates_year_option.click()
                        time.sleep(3)
                        verify_inspection_date = inspection_date_year
                        print inspection_date_year
                        break
                 
                # --------- 年检月份 -------------------
                printDelimiter()
                get_inspection_dates_months = browser.find_element_by_name('m_nianjian')             
                inspection_dates_month_options = get_inspection_dates_months.find_elements_by_tag_name('option')
                for inspection_dates_month_option in inspection_dates_month_options:
                    if inspection_date_month[0] == '0':
                        if str(inspection_dates_month_option.text) == inspection_date_month[1]:
                            inspection_dates_month_option.click()
                            time.sleep(3)
                            print inspection_date_month
                            break
                    else:
                        if str(inspection_dates_month_option.text) == inspection_date_month:
                            inspection_dates_month_option.click()
                            time.sleep(3)
                            print inspection_date_month
                            break
                 
            if verify_inspection_date == '':
                get_inspection_dates_years = browser.find_element_by_name('y_nianjian')
                inspection_dates_year_options = get_inspection_dates_years.find_elements_by_tag_name('option')
                inspection_dates_year_options[-1].click()
                time.sleep(3)
              
            # ------------- 交强险到期 ---------------------
            printDelimiter()
            verify_force_insurance_date = ''
            print u"交强险到期:",force_insurance_date
            if force_insurance_date is not None:
                # --------- 交强险年份 -------------------
                printDelimiter()
                get_force_insurance_dates_years = browser.find_element_by_name('y_jiaoqiangxian')         
                force_insurance_dates_year_options = get_force_insurance_dates_years.find_elements_by_tag_name('option')
                for force_insurance_dates_year_option in force_insurance_dates_year_options:
                    if str(force_insurance_dates_year_option.text) == force_insurance_date_year:
                        force_insurance_dates_year_option.click()
                        time.sleep(3)
                        verify_force_insurance_date = force_insurance_date_year
                        print force_insurance_date_year
                        break
                 
                # --------- 交强险月份 -------------------
                printDelimiter()
                get_force_insurance_dates_months = browser.find_element_by_name('m_jiaoqiangxian')
                force_insurance_dates_month_options = get_force_insurance_dates_months.find_elements_by_tag_name('option')
                for force_insurance_dates_month_option in force_insurance_dates_month_options:
                    if force_insurance_date_month[0] == '0':
                        if str(force_insurance_dates_month_option.text) == force_insurance_date_month[1]:
                            force_insurance_dates_month_option.click()
                            time.sleep(3)
                            print force_insurance_date_month
                            break
                    else:
                        if str(force_insurance_dates_month_option.text) == force_insurance_date_month:
                            force_insurance_dates_month_option.click()
                            time.sleep(3)
                            print force_insurance_date_month
                            break
                 
            if verify_force_insurance_date == '':
                get_force_insurance_dates_years = browser.find_element_by_name('y_jiaoqiangxian')         
                force_insurance_dates_year_options = get_force_insurance_dates_years.find_elements_by_tag_name('option')
                force_insurance_dates_year_options[-1].click()
                time.sleep(3)
            
            # ------------- 商业险到期 ---------------------
            printDelimiter()
            verify_insurance_date = ''
            print u"商业险到期:",insurance_date
            if insurance_date is not None:
                # --------- 商业险年份 -------------------
                printDelimiter()
                get_insurance_dates_years = browser.find_element_by_name('y_shangyexian')         
                insurance_dates_year_options = get_insurance_dates_years.find_elements_by_tag_name('option')
                for insurance_dates_year_option in insurance_dates_year_options:
                    if str(insurance_dates_year_option.text) == insurance_date_year:
                        insurance_dates_year_option.click()
                        time.sleep(3)
                        verify_insurance_date = insurance_date_year
                        print insurance_date_year
                        break
                 
                # --------- 商业险月份 -------------------
                printDelimiter()
                get_insurance_dates_months = browser.find_element_by_name('m_shangyexian')
                insurance_dates_month_options = get_insurance_dates_months.find_elements_by_tag_name('option')
                for insurance_dates_month_option in insurance_dates_month_options:
                    if insurance_date_month[0] == '0':
                        if str(insurance_dates_month_option.text) == insurance_date_month[1]:
                            insurance_dates_month_option.click()
                            time.sleep(3)
                            print insurance_date_month
                            break
                    else:
                        if str(insurance_dates_month_option.text) == insurance_date_month:
                            insurance_dates_month_option.click()
                            time.sleep(3)
                            print insurance_date_month
                            break
                 
            if verify_insurance_date == '':
                get_insurance_dates_years = browser.find_element_by_name('y_shangyexian')         
                insurance_dates_year_options = get_insurance_dates_years.find_elements_by_tag_name('option')
                insurance_dates_year_options[-1].click()
                time.sleep(3)
            browser.switch_to.default_content()
            time.sleep(2)
            
            
    
            # ---------- 行驶里程、转让价格、一句话广告 ----------------
            print u"行驶里程:",shown_miles
            browser.find_element_by_id('rundistance').clear()
            browser.find_element_by_id('rundistance').send_keys(shown_miles.decode('utf-8'))
            print u"车主报价:",owner_price
            browser.find_element_by_id('MinPrice').clear()
            browser.find_element_by_id('MinPrice').send_keys(str(owner_price))
            browser.find_element_by_id('guohufeiyong').click()
            browser.find_element_by_id('titleEnd').clear()
            browser.find_element_by_id('titleEnd').send_keys(u'淘车乐认证首付30%')
            
            # ------------- 补充说明 -------------------------
            printDelimiter()
            print u"补充说明"
            detail_info = u"""淘车乐微信：“南通淘车乐二手车”（微信号：nt930801） ，海量车源在线看。
   淘车乐服务 ：二手车寄售、二手车购买、二手车零首付贷款、二手车评估认证。
   淘车乐地址：南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)
  公交路线 ：可乘坐3路、10路、600路、602路到果园站下车。沿城港路走30米左转进入兴泰路走200米。
  淘车乐，帮您实现有车生活。"""
            browser.find_element_by_id('Content').clear()
            browser.find_element_by_id('Content').send_keys(detail_info.decode('utf-8'))
            
            
            # ------------- 联系人、联系方式、联系地址 -------------------------
            printDelimiter()
            print u"联系人、联系方式、联系地址"
            contact_person = u'南通淘车乐'
            contact_telephone = '17712233652'
            addrs = u'南京市秦淮区大明路282号'
            browser.find_element_by_id('goblianxiren').clear()
            browser.find_element_by_id('goblianxiren').send_keys(contact_person.decode('utf-8'))
            faburens = browser.find_elements_by_name('faburen')
            for faburen in faburens:
                faburen.click()
            browser.find_element_by_id('Phone').clear()
            browser.find_element_by_id('Phone').send_keys(contact_telephone.decode('utf-8'))
            browser.find_element_by_id('caraddress').clear()
            browser.find_element_by_id('caraddress').send_keys(addrs.decode('utf-8'))
    
           
            # ------------- 上传车辆图片 ------------------
            
            #browser.execute_script("document.getElementById('uploadImgcontainer').setAttribute('style','display: block;')")
            #browser.execute_script("document.getElementById('upload_Tip').setAttribute('style','display: block; margin-bottom: 14px;')")
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            car_imgs = get_car_info(vehicle_num)[1]
            first_upload_image_fails = 0
            second_upload_image_fails = 0
            
     		# ------------- 1.车辆封面照 ------------------
            for i in range(1):
                print car_imgs[i]
                while True:
                    try:
                        if first_upload_image_fails > 5:
                            break
                        wait.until(EC.element_to_be_clickable((By.ID,'htmlImgUp')))
                        browser.find_element_by_id('htmlImgUp').click()
                    except:
                        first_upload_image_fails += 1
                        print "upload cover image failed ... ",first_upload_image_fails
                        time.sleep(3)
                    else:
                        break            
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"选择要加载的文件", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",5)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"选择要加载的文件", "", "Edit1", car_imgs[i])
                time.sleep(2)
                #Click on the Open button
                autoit.ControlClick(u"选择要加载的文件", "","Button1")
                time.sleep(8)
            
            
            # ------------- 2.卖场二维码 ------------------
            print "two-dimensional bar code"
            while True:
                try:
                    if second_upload_image_fails > 5:
                        break
                    wait.until(EC.element_to_be_clickable((By.ID,'htmlImgUp')))
                    browser.find_element_by_id('htmlImgUp').click()
                except:
                    second_upload_image_fails += 1
                    print "upload cover image failed ... ",second_upload_image_fails
                    time.sleep(3)
                else:
                    break   
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"选择要加载的文件", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",5)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"选择要加载的文件", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\nantong\\nantong.jpg")
            time.sleep(2)
            #Click on the Open button
            autoit.ControlClick(u"选择要加载的文件", "","Button1")
            time.sleep(8)
            
            if len(car_imgs)>8: 
                for i in range(2,8):
                    third_upload_image_fails = 0 
                    print car_imgs[i]
                    while True:
                        try:
                            if third_upload_image_fails > 5:
                                break
                            wait.until(EC.element_to_be_clickable((By.ID,'htmlImgUp')))
                            browser.find_element_by_id('htmlImgUp').click()
                        except:
                            third_upload_image_fails += 1
                            print "upload car detail image failed ... ",third_upload_image_fails
                            time.sleep(3)
                        else:
                            break               
                    #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                    autoit.ControlFocus(u"选择要加载的文件", "","Edit1")
                    #Wait 10 seconds for the Upload window to appear
                    autoit.WinWait("[CLASS:#32770]","",5)
                    # Set the File name text on the Edit field
                    autoit.ControlSetText(u"选择要加载的文件", "", "Edit1", car_imgs[i])
                    time.sleep(2)
                    #Click on the Open button
                    autoit.ControlClick(u"选择要加载的文件", "","Button1")
                    time.sleep(8)
            else:
                for i in range(2,len(car_imgs)):
                    third_upload_image_fails = 0 
                    print car_imgs[i]
                    while True:
                        try:
                            if third_upload_image_fails > 5:
                                break
                            wait.until(EC.element_to_be_clickable((By.ID,'htmlImgUp')))
                            browser.find_element_by_id('htmlImgUp').click()
                        except:
                            third_upload_image_fails += 1
                            print "upload car detail image failed ... ",third_upload_image_fails
                            time.sleep(3)
                        else:
                            break 
                                
                    #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                    autoit.ControlFocus(u"选择要加载的文件", "","Edit1")
                    #Wait 10 seconds for the Upload window to appear
                    autoit.WinWait("[CLASS:#32770]","",5)
                    # Set the File name text on the Edit field
                    autoit.ControlSetText(u"选择要加载的文件", "", "Edit1", car_imgs[i])
                    time.sleep(2)
                    #Click on the Open button
                    autoit.ControlClick(u"选择要加载的文件", "","Button1")
                    time.sleep(8)
           
            time.sleep(5)
            print "finished ..... "
            #browser.find_element_by_id('fabu').submit()
            #time.sleep(10)
            #browser.quit()
              


if __name__ == "__main__":   
    post_cardata()
