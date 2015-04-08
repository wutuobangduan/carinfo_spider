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
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import unittest,time,re,os 

from pyvirtualdisplay import Display

from urllib2 import Request,urlopen,URLError,HTTPError


import optparse
import datetime


#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;


def get_vehicle_nums():
    tm1 = datetime.date.today()
    day1 = tm1.isoformat() + ' 00:00:00'
    
    tm2 = datetime.date.today()-datetime.timedelta(days=1)
    day2 = tm2.isoformat() + ' 00:00:00'
    vehicle_nums = []
    try:
        conn = MySQLdb.connect(host='',user='',passwd='',charset='utf8')
        curs = conn.cursor()
        conn.select_db('')
        curs.execute("select vehicle_number from vehicle_info where address=762 and sell_time between '%s' and '%s' and is_del=0 and sync_status!=0 order by sell_time asc" % (day2,day1))
        get_vehicle_nums = curs.fetchone()
        
        while get_vehicle_nums is not None:
            ((vehicle_number),) = get_vehicle_nums
            #print "http://imgw00.tc5u.cn/" + vehicle_img
            vehicle_nums.append(vehicle_number)
            get_vehicle_nums = curs.fetchone()

        conn.commit()
        curs.close()
        conn.close()
        return vehicle_nums
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)

def get_car_info(vehicle_nums):
    imgurls = [""]
    try:
        conn = MySQLdb.connect(host='',user='',passwd='',charset='utf8')
        curs = conn.cursor()
        conn.select_db('')
        curs.execute("select (select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address),vmc.vehicle_model_conf53 as environmental_standards,vmc.vehicle_model_conf48 as fuel_form,vmc.vehicle_model_conf5 as car_level  from vehicle_info vi,vehicle_model vm,vehicle_model_conf vmc where vi.vehicle_number='%s' and vm.id=vi.model_id and vmc.id=vi.model_id" % vehicle_nums)
        getrows=curs.fetchall()
        if not getrows:
            result = []
        else:
            result = [getrows]

        curs.execute("select imgurl from vehicle_img where vehicle_number='%s'" % vehicle_nums)
        get_imgurls = curs.fetchone()
        
        while get_imgurls is not None:
            ((vehicle_img),) = get_imgurls
            #print "http://imgw00.tc5u.cn/" + vehicle_img
            imgurls.append("http://imgn00.tc5u.cn/" + vehicle_img)
            get_imgurls = curs.fetchone()

        result.append(imgurls)
        return result
        conn.commit()
        curs.close()
        conn.close()
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
        autoit = win32com.client.Dispatch("AutoItX3.Control")
        autoit.ControlClick(u"Plugin Container for Firefox", "","Button1")
        time.sleep(2)
    except:
        print "The Plugin Container for Firefox  is normal..."

    
    try:
        #chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #browser = webdriver.Chrome(chromedriver)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type',1)   #默认值0，就是直接连接；1就是手工配置代理。
        profile.set_preference('network.proxy.http','202.106.16.36')
        profile.set_preference('network.proxy.http_port', 3128)
        profile.update_preferences()
        browser = webdriver.Firefox(profile)
        try:
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            autoit.ControlClick(u"Firefox", "","Button1")
            time.sleep(2)
        except:
            print "The Firefox browser is normal..."
        #browser = webdriver.Firefox()
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(60)
        
    except WebDriverException,e:
        print e
     
    if browser is not None:
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://nanjing.baixing.com/oz/login")
                browser.implicitly_wait(10)
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        browser.find_element_by_id('id_identity').find_element_by_name('identity').clear()
        browser.find_element_by_id('id_identity').find_element_by_name('identity').send_keys(options.username.decode('gb2312'))
        browser.find_element_by_id('id_password').find_element_by_name('password').clear()
        browser.find_element_by_id('id_password').find_element_by_name('password').send_keys(options.password)
        time.sleep(5)
        browser.find_element_by_id('id_submit').submit()
        print browser.find_element_by_id('welcome-info').find_element_by_class_name('dropdown-topbar').text
     
        vehicle_nums = get_vehicle_nums()
        #vehicle_nums = ['32010401000003900000204335']
        #,'32010402000002950000204333','32010401000002920000204320','32010402000002720000204323','32010401000003590000204324','32010401000012150000204330','32010401000011450000204327','32010401000008520000204328','32010401000004250000204317','32010401000008490000204315']
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
            else:
                continue
            car_imgs = get_car_info(vehicle_num)[1]
            if len(car_imgs) < 2:
                continue
            get_post_page_fails = 0 
            while True:
                try:
                    if get_post_page_fails > 10:
                        break
                    browser.get("http://nanjing.baixing.com/fabu/ershouqiche/?")
                    browser.implicitly_wait(10)
                    time.sleep(3)
                except:
                    get_post_page_fails += 1
                    print "get page info failed ... ",get_post_page_fails
                else:
                    break
            #print chardet.detect(vehicle_model.decode('utf-8'))
            #print type(vehicle_model.decode('utf-8'))
            #print chardet.detect(volume.decode('ascii'))
            #print type(volume.decode('ascii'))
            #print volume[:3]
            
            #print len(volume)
            #print type(shown_miles)
            #print type(owner_price)
    
            
            # ------------------ brands ---------------------
            printDelimiter()
            print vehicle_num
            print u"品牌:",brand.decode('utf-8')
            try:
                div = browser.find_element_by_id('id_车品牌')
                get_brands = div.find_element_by_tag_name('select')
                brand_options = get_brands.find_elements_by_tag_name('option')
            except:
                get_post_pages = 0
                while True:
                    try:
                        if get_post_pages > 10:
                            break
                        browser.get("http://changshu.baixing.com/fabu/ershouqiche/?")
                        browser.implicitly_wait(10)
                        time.sleep(3)
                    except:
                        get_post_pages += 1
                        print "get page info failed ... ",get_post_pages
                    else:
                        break
                div = browser.find_element_by_id('id_车品牌')
                get_brands = div.find_element_by_tag_name('select')
                brand_options = get_brands.find_elements_by_tag_name('option')
            first_brand = 0
            second_brand = 0
            verify_brand = 0
            for brand_option in brand_options:
                #print option.text,type(option.text),chardet.detect(str(option.text))
                if str(brand_option.text).lower() == brand.lower():     
                    print brand_option.text
                    brand_option.click()
                    first_brand = 1
                    verify_brand = 1
                    time.sleep(3)
                    break
            if first_brand == 0:
                for brand_option in brand_options:
                    if str(brand_option.text).lower() in brand.lower():
                        print brand_option.text
                        brand_option.click()
                        second_brand = 1
                        verify_brand = 1
                        time.sleep(3)
                        break
            if first_brand == 0 and second_brand == 0:
                for brand_option in brand_options:
                    if brand.lower() in str(brand_option.text).lower():
                        print brand_option.text
                        brand_option.click()
                        verify_brand = 1
                        time.sleep(3)
                        break
            if verify_brand == 0:
                continue
            try:
                browser.find_element_by_id('moreinfo').find_element_by_class_name('button-show').click()
#             moreinfo = browser.find_element_by_id('moreinfo')
#             span = moreinfo.find_element_by_class_name('button-show')
#             span.click()
            except:
                print "There is no need to click ..."
            #print browser.find_element_by_id('id_燃油类型').text
            
            # --------------------------------------------
            printDelimiter()
            print u"title、行驶里程、价格、排量、燃油类型、排放标准"
            browser.find_element_by_id('id_title').find_element_by_tag_name('input').clear()
            browser.find_element_by_id('id_title').find_element_by_tag_name('input').send_keys(u'淘车乐认证 ' + vehicle_model.decode('utf-8'))
            browser.find_element_by_id('id_行驶里程').find_element_by_tag_name('input').clear()
            browser.find_element_by_id('id_行驶里程').find_element_by_tag_name('input').send_keys(shown_miles.decode('utf-8'))
            browser.find_element_by_id('id_价格').find_element_by_tag_name('input').clear()
            browser.find_element_by_id('id_价格').find_element_by_tag_name('input').send_keys(str(owner_price))
            browser.find_element_by_id('id_排量').find_element_by_tag_name('input').clear()
            browser.find_element_by_id('id_排量').find_element_by_tag_name('input').send_keys(str(volume[:3]))
            browser.find_element_by_id('id_燃油类型').find_element_by_tag_name('input').clear()
            browser.find_element_by_id('id_燃油类型').find_element_by_tag_name('input').send_keys(fuel_form.decode('utf-8'))      
            browser.find_element_by_id('id_排放标准').find_element_by_tag_name('input').clear()
            browser.find_element_by_id('id_排放标准').find_element_by_tag_name('input').send_keys(environmental_standards.decode('utf-8'))  
            detail_info = """  淘车乐24小时连锁卖场
  上班太忙，没时间看车？淘车乐晚间车市开幕啦，24小时随时看车
 260项检测，无事故，无泡水，无差价
 
 [ 淘车乐承诺 ] 重大事故车、泡水车，包退款。
    
 [ 淘车乐质保 ] 免费质保，终身免费电话咨询4000780786
    
 [ 关注淘车乐 ] 复制 www.ic5u.com 或百度一下“淘车无忧”去官网查看更多...
  搜索订阅号“南京淘车乐”或“tcl282”关注我们官方微信
    
  ------------------关于淘车乐--------------
    
  淘车乐是淘车无忧的旗下连锁卖场，是全国最大O2O二手车交易平台，为您提供最好的二手车购买体验：
    
 “认证好车” — 严格筛选车源，经淘车乐认证车源，放心购买。 
    
 “专业检测” — 专业评估师执行260项检测标准。
    
 “金融服务” —分期、O首付、贷款一条龙服务。 
    
 “诚实质保” — 提供免费质保。
    
 “服务24h”— 作为您忠实的朋友，淘车乐24小时随时听候调遣。
    
  更多信息可访问淘车无忧(www.ic5u.com)"""
            browser.find_element_by_id('id_content').find_element_by_tag_name('textarea').clear()
            browser.find_element_by_id('id_content').find_element_by_tag_name('textarea').send_keys(detail_info.decode('utf-8'))
    		
            # ----------- transmissions -------------------
            printDelimiter()
            print u"变速箱:",transmission.decode('utf-8')
            get_transmissions = browser.find_element_by_id('id_变速箱')
            transmissions = get_transmissions.find_element_by_tag_name('select')
            transmission_options = transmissions.find_elements_by_tag_name('option')
            for transmission_option in transmission_options:
                if str(transmission_option.text) != '' and str(transmission_option.text) in transmission:
                    print transmission_option.text
                    transmission_option.click()
                    time.sleep(3)
            
            # ----------- color ---------------------------
            printDelimiter()
            print u"车身颜色:",color.decode('utf-8')
            color_verify = ''
            get_colors = browser.find_element_by_id('id_车辆颜色')
            colors = get_colors.find_element_by_tag_name('select')
            color_options = colors.find_elements_by_tag_name('option')
            for color_option in color_options:
                if str(color_option.text) != '' and str(color_option.text) in color:
                    color_verify = str(color_option.text)
                    print color_option.text
                    color_option.click()
                    time.sleep(3)
         
            if color_verify == '':
                color_options[-1].click()   
                time.sleep(3)
    
            # ----------- car_level -------------------------
            printDelimiter()
            print u"车身级别:",car_level.decode('utf-8')
            car_level_verify = ''
            get_car_levels = browser.find_element_by_id('id_类型')
            car_levels = get_car_levels.find_element_by_tag_name('select')
            car_level_options = car_levels.find_elements_by_tag_name('option')
            for car_level_option in car_level_options:
                if str(car_level_option.text) != '' and str(car_level_option.text) in car_level:
                    car_level_verify = str(car_level_option.text)
                    print car_level_option.text
                    car_level_option.click()
                    time.sleep(3)
    
            if car_level_verify == '':
                car_level_options[-1].click()
                time.sleep(3)
       
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
            if register_date is not None:
                get_register_dates = browser.find_element_by_id('id_年份')
                register_dates_year = get_register_dates.find_element_by_name('年份[0]')
                register_dates_year_options = register_dates_year.find_elements_by_tag_name('option')
                for register_dates_year_option in register_dates_year_options:
                    if register_date_year in str(register_dates_year_option.text):
                        print "首次上牌年份：",register_dates_year_option.text
                        register_dates_year_option.click()
                        time.sleep(1)
                        break
                register_dates_month = get_register_dates.find_element_by_name('年份[1]')
                register_dates_month_options = register_dates_month.find_elements_by_tag_name('option')
                for register_dates_month_option in register_dates_month_options:
                    register_dates_month_str = re.findall('\d+',str(register_dates_month_option.text))
                    if len(register_dates_month_str)>0:
                        if register_date_month[0] == '0':
                            if register_date_month[1] == register_dates_month_str[0]:
                                print u"首次上牌月份：",register_dates_month_option.text
                                register_dates_month_option.click()
                                time.sleep(1)
                                break
                        else:
                            if register_date_month == register_dates_month_str[0]:
                                print u"首次上牌月份：",register_dates_month_option.text
                                register_dates_month_option.click()
                                time.sleep(1)
                                break
            # ------------- 年检到期 ---------------------
            printDelimiter()
            print u"年检到期:",inspection_date
            if inspection_date is not None:
                get_inspection_dates = browser.find_element_by_id('id_年检')
                inspection_dates_year = get_inspection_dates.find_element_by_name('年检[0]')
                inspection_dates_year_options = inspection_dates_year.find_elements_by_tag_name('option')
                for inspection_dates_year_option in inspection_dates_year_options:
                    if inspection_date_year in str(inspection_dates_year_option.text):
                        inspection_dates_year_option.click()
                        time.sleep(1)
                        break
                inspection_dates_month = get_inspection_dates.find_element_by_name('年检[1]')
                inspection_dates_month_options = inspection_dates_month.find_elements_by_tag_name('option')
                for inspection_dates_month_option in inspection_dates_month_options:
                    inspection_dates_month_str = re.findall('\d+',str(inspection_dates_month_option.text))
                    if len(inspection_dates_month_str)>0:
                        if inspection_date_month[0] == '0':
                            if inspection_date_month[1] == inspection_dates_month_str[0]:
                                print u"年检到期月份：",inspection_dates_month_option.text
                                inspection_dates_month_option.click()
                                time.sleep(1)
                                break
                        else:
                            if inspection_date_month == inspection_dates_month_str[0]:
                                print u"年检到期月份：",inspection_dates_month_option.text
                                inspection_dates_month_option.click()
                                time.sleep(1)
                                break
            
            # ------------- 交强险到期 ---------------------
            printDelimiter()
            print u"交强险到期:",force_insurance_date
            if force_insurance_date is not None:
                get_force_insurance_dates = browser.find_element_by_id('id_交强险')
                force_insurance_dates_year = get_force_insurance_dates.find_element_by_name('交强险[0]')
                force_insurance_dates_year_options = force_insurance_dates_year.find_elements_by_tag_name('option')
                for force_insurance_dates_year_option in force_insurance_dates_year_options:
                    if force_insurance_date_year in str(force_insurance_dates_year_option.text):
                        force_insurance_dates_year_option.click()
                        time.sleep(1)
                        break
                force_insurance_dates_month = get_force_insurance_dates.find_element_by_name('交强险[1]')
                force_insurance_dates_month_options = force_insurance_dates_month.find_elements_by_tag_name('option')
                for force_insurance_dates_month_option in force_insurance_dates_month_options:
                    force_insurance_dates_month_str = re.findall('\d+',str(force_insurance_dates_month_option.text))
                    if len(force_insurance_dates_month_str)>0:
                        if force_insurance_date_month[0] == '0':
                            if force_insurance_date_month[1] == force_insurance_dates_month_str[0]:
                                print u"交强险到期月份：",force_insurance_dates_month_option.text
                                force_insurance_dates_month_option.click()
                                time.sleep(1)
                                break
                        else:
                            if force_insurance_date_month == force_insurance_dates_month_str[0]:
                                print u"交强险到期月份：",force_insurance_dates_month_option.text
                                force_insurance_dates_month_option.click()
                                time.sleep(1)
                                break
    
            # ------------- 商业险到期 ---------------------
            printDelimiter()
            print u"商业险到期:",insurance_date
            if insurance_date is not None:
                get_insurance_dates = browser.find_element_by_id('id_商业险')
                insurance_dates_year = get_insurance_dates.find_element_by_name('商业险[0]')
                insurance_dates_year_options = insurance_dates_year.find_elements_by_tag_name('option')
                for insurance_dates_year_option in insurance_dates_year_options:
                    if insurance_date_year in str(insurance_dates_year_option.text):
                        insurance_dates_year_option.click()
                        time.sleep(1)
                        break
                insurance_dates_month = get_insurance_dates.find_element_by_name('商业险[1]')
                insurance_dates_month_options = insurance_dates_month.find_elements_by_tag_name('option')
                for insurance_dates_month_option in insurance_dates_month_options:
                    insurance_dates_month_str = re.findall('\d+',str(insurance_dates_month_option.text))
                    if len(insurance_dates_month_str)>0:
                        if insurance_date_month[0] == '0':
                            if insurance_date_month[1] == insurance_dates_month_str[0]:
                                print u"商业险到期月份：",insurance_dates_month_option.text
                                insurance_dates_month_option.click()
                                time.sleep(1)
                                break
                        else:
                            if insurance_date_month == insurance_dates_month_str[0]:
                                print u"商业险到期月份：",insurance_dates_month_option.text
                                insurance_dates_month_option.click()
                                time.sleep(1)
                                break
            # ------------- 承担过户费 ---------------------
            printDelimiter()
            print u"承担过户费"
            browser.find_element_by_id('id_承担过户费').find_element_by_tag_name('input').click()
    
            # ------------- 行驶证 ---------------------
            printDelimiter()
            print u"行驶证"
            browser.find_element_by_id('id_行驶证').find_element_by_tag_name('input').click()
                 
            # ------------- 登记证 ---------------------
            printDelimiter()
            print u"登记证"
            browser.find_element_by_id('id_登记证').find_element_by_tag_name('input').click()
    
            # ------------- 购车发票 ---------------------
            printDelimiter()
            print u"购车发票"
            browser.find_element_by_id('id_购车发票').find_element_by_tag_name('input').click()
    
            # ------------- 维修记录 ---------------------
            printDelimiter()
            print u"维修记录"
            browser.find_element_by_id('id_维修记录').find_element_by_tag_name('input').click()
    
            # ------------- 购置税 ---------------------
            printDelimiter()
            print u"购置税"
            browser.find_element_by_id('id_购置税').find_element_by_tag_name('input').click()
    
            # ------------- 重大事故 ---------------------
            printDelimiter()
            print u"重大事故"
            accident = browser.find_element_by_id('id_重大事故')
            accident_res = accident.find_elements_by_tag_name('input')
            accident_res[1].click()
    
            # ------------- 能否过户 ---------------------
            printDelimiter()
            print u"能否过户"
            browser.find_element_by_id('id_能否过户').find_element_by_tag_name('input').click()
            
            # ------------- 能否按揭 ---------------------
            printDelimiter()
            print u"能否按揭"
            browser.find_element_by_id('id_能否按揭').find_element_by_tag_name('input').click()
            
            # ------------- 上传车辆图片 ------------------
            autoit = win32com.client.Dispatch("AutoItX3.Control")
    		# ------------- 1.车辆封面照 ------------------
            car_imgs = get_car_info(vehicle_num)[1]
            print "cover image..."
            for i in range(2):
                browser.find_element_by_id('SWFUpload_0').click()
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"打开", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",10)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                time.sleep(3)
                #Click on the Open button
                autoit.ControlClick(u"打开", "","Button1")
                time.sleep(6)
            
            print "two-dimensional bar code"
            browser.find_element_by_id('SWFUpload_0').click()
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",10)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\nanjing\\nanjing.jpg")
            time.sleep(3)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(6)
    		
            print "advertisement1"
            browser.find_element_by_id('SWFUpload_0').click()
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",10)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\fangan.jpg")
            time.sleep(3)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(6)
            
            print "advertisement2"
            browser.find_element_by_id('SWFUpload_0').click()
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",10)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\A501.jpg")
            time.sleep(3)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(6)
            
            print "upload two-dimensional bar code finished ..."
            for i in range(2,len(car_imgs)):
                print car_imgs[i]
                browser.find_element_by_id('SWFUpload_0').click()
                
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"打开", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",10)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                time.sleep(3)
                #Click on the Open button
                autoit.ControlClick(u"打开", "","Button1")
                time.sleep(6)
    		#autoit.WinWait(u"打开", "", 5)  
            #autoit.WinActivate(u"打开")          
            #autoit.ControlSetText(u"打开","","[CLASS:Edit; INSTANCE:1]",car_imgs[0])
            #time.sleep(2)		
            #autoit.ControlClick(u"打开","",u"保存(&S)")  
            #autoit.ControlClick(u"打开","",u"打开(&O)") #附件上传动作  
            #os.system("C:\\Users\\Administrator\\Desktop\\test_auto.exe")
            #for i in range(len(car_imgs)):
    
            #print "just for test..."
            #return True
            time.sleep(3)
            browser.find_element_by_id('fabu-form-submit').submit()
            time.sleep(8)
        browser.quit()



if __name__ == "__main__":   
    #loginTobaixing()
    post_cardata()
