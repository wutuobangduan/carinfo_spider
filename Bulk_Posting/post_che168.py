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
    except NoSuchElementException:
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

def binary(file1):
#     print img_src
#     opener = urllib2.build_opener()
#     cookies = {}
#     opener.addheaders.append(("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"))
#     opener.addheaders.append(("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"))
#     opener.addheaders.append(("Accept-Encoding","gzip, deflate, sdch"))
#     opener.addheaders.append(("Accept-Language","zh-CN,zh;q=0.8"))
#     opener.addheaders.append(("Connection","keep-alive"))
#     opener.addheaders.append(("Host","dealer.che168.com"))
#     cookie_str = ''
#     for cookie in all_cookies:
#         cookie_str += cookie['name'] + "=" + cookie['value'] + ";"
#     print cookie_str
#     opener.addheaders.append(("Cookie","%s" % cookie_str)) 
    #print opener
#     fails = 0
#     while True:
#         try:
#             if fails >= 10:
#                 break
#             response = opener.open(img_src,timeout=30)
#             #print response.info().get_header('Set-Cookie')
#             html = response.read()
#         except:
#             fails += 1
#             print "Handing validate code,the network may be not Ok,please wait...",fails
#         else:
#             break
    #print html
#     file1 = StringIO(html)
    #print file1
    img = Image.open(file1)
    #print img.info,img.size,img.format
    img = img.convert("RGBA")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] == 0 and pixdata[x, y][2] == 0 and pixdata[x, y][3] == 0:
                pixdata[x, y] = (255,255,255,255)
            if pixdata[x, y][1] == 255 and pixdata[x, y][2] == 255 and pixdata[x, y][3] == 204:
                pixdata[x, y] = (255,255,255,255)
            if pixdata[x, y][1] < 220 or pixdata[x, y][2] < 220:
                pixdata[x, y] = (0, 0, 0,255)
            else:
                pixdata[x, y] = (255, 255, 255,255)
    return img



def division(img):        
    #global nume
    nume=0
    font=[]
    for i in range(4):
        x = 5 + i*9
        y = 5 
        temp = img.crop((x, y, x+9,y+12))
        temp.save("C:\Python27\Bulk_Posting\che168_temp\%d.png" % nume)
        nume=nume+1
        font.append(temp)
    return font


def recognize(img):
    fontMods = []
    image_num = ['0','00','000','0000','00000','1','11','111','1111','11111','2','22','222','2222','22222','3','33','333','3333','33333','4','44','444','4444','44444','5','55','555','5555','55555','6','66','666','6666','66666','7','77','777','7777','77777','8','88','888','8888','88888','9','99','999','9999','99999']
    for i in image_num:
        fontMods.append((str(i), Image.open("C:\Python27\Bulk_Posting\che168_fonts\%s.png" % i)))
    result=""
    font=division(img)
     
    for i in font:
        target=i
        points = []
        for mod in fontMods:
            diffs = 0
            for yi in range(12):
                for xi in range(9):     
                    if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                        diffs += 1
            
            points.append((diffs, mod[0]))
        points.sort()
        if "0" in points[0][1]:
            result += "0"
        elif "1" in points[0][1]:
            result += "1"
        elif "2" in points[0][1]:
            result += "2"
        elif "3" in points[0][1]:
            result += "3"
        elif "4" in points[0][1]:
            result += "4"
        elif "5" in points[0][1]:
            result += "5"
        elif "6" in points[0][1]:
            result += "6"
        elif "7" in points[0][1]:
            result += "7"
        elif "8" in points[0][1]:
            result += "8"
        elif "9" in points[0][1]:
            result += "9"
        
    return result    


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
                browser.get("http://dealer.che168.com/login.html")
                browser.implicitly_wait(5)              
                #pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        time.sleep(1)
        browser.find_element_by_id('userName').send_keys(options.username.decode('gb2312'))
        browser.find_element_by_id('userPWD').send_keys(options.password)
        validate_code_url = str(browser.find_element_by_id('imgValidCode').get_attribute('src'))
        validate_code_img = browser.find_element_by_id('imgValidCode')
        ActionChains(browser).context_click(validate_code_img).perform()
        time.sleep(1)
        win32api.keybd_event(40,0,0,0)
        time.sleep(1)
        win32api.keybd_event(13,0,0,0)
        time.sleep(1)
        #ActionChains(browser).move_by_offset(0,100).perform()
        #ActionChains(browser).click().perform()
        win32api.keybd_event(40,0,win32con.KEYEVENTF_KEYUP,0)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        autoit = win32com.client.Dispatch("AutoItX3.Control")
        #ControlFocus("title","text",controlID) Edit1=Edit instance 1
        autoit.ControlFocus(u"另存为", "","Edit1")
        #Wait 10 seconds for the Upload window to appear
        autoit.WinWait("[CLASS:#32770]","",5)
        # Set the File name text on the Edit field
        autoit.ControlSetText(u"另存为", "", "Edit1", "CreateImgCode.gif")
        time.sleep(3)
        #Click on the Open button
        autoit.ControlClick(u"另存为", "","Button1")
        time.sleep(5)
        autoit.ControlClick(u"确认另存为","","Button1")
        time.sleep(5)
        img_src = "C:\Users\Administrator\Downloads\CreateImgCode.gif" 
        #urllib.urlretrieve(validate_code_url, "captcha.png")
        #browser.save_screenshot("screenshot.png")
        all_cookies = browser.get_cookies()
        
        images = binary(img_src)
        num = recognize(images)
        print num
#         numbers = raw_input("please input the validate code: ")
        browser.find_element_by_id('yzPwd').send_keys(num)
        browser.find_element_by_id('in2week').click()
        browser.find_element_by_class_name('btn_lgn').click()
        time.sleep(8)
        print 'test...'
        print browser.find_element_by_class_name('index-4sname').text
        vehicle_nums = ["32010401000008490000204315","32010401000004250000204317","32010401000008520000204328","32010401000012150000204330","32010401000003590000204324","32010401000003900000204335","32010401000002920000204320","32010401000011450000204327"]
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((vin,brand_initial,brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
            else:
                return False
            
            
            while True:
                try:
                    if get_publish_page_fails > 10:
                        break
                    browser.get("http://dealer.che168.com/car/publish/")
                    browser.implicitly_wait(5)
                    all_cookies = browser.get_cookies()
                    #pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
                except:
                    get_publish_page_fails += 1
                    print "get page info failed ... ",get_publish_page_fails
                else:
                    break
            
#             # ------------------ vin ------------------------
#             print "vin is : ",vin.decode('utf-8')
#             browser.find_element_by_id('carVIN').send_keys(vin.decode('utf-8'))
            
            # ------------------ brands ---------------------
            printDelimiter()
            print u"品牌首字母:",brand_initial
            print u"品牌:",brand.decode('utf-8')
            print u"车系:",vehicle_series.decode('utf-8')
            print u"车型:",vehicle_model.decode('utf-8')
            
            browser.execute_script("document.getElementById('sh_sltCar_div').setAttribute('style','display: block;')")
            time.sleep(3)
            brand_initials = browser.find_element_by_id('leftzm').find_elements_by_tag_name('a')
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
            brand_options = browser.find_element_by_id('sltBrandList').find_elements_by_tag_name('a')
            for brand_option in brand_options:
                if str(brand_option.text).lower() == brand.lower():
                    print brand_option.text
                    brand_option.click()
                    break
                elif str(brand_option.text).lower() in brand.lower():
                    print brand_option.text
                    brand_option.click()
                    break
                elif brand.lower() in str(brand_option.text).lower():
                    print brand_option.text
                    brand_option.click()
                    break
            #time.sleep(1)
            vehicle_series_options = browser.find_element_by_id('sltSerise').find_elements_by_tag_name('a')
            first_vehicle_series = 0
            second_vehicle_series = 0
            for vehicle_series_option in vehicle_series_options:
                if str(vehicle_series_option.text).lower() == vehicle_series.lower():
                    print vehicle_series_option.text
                    vehicle_series_option.click()
                    first_vehicle_series = 1
                    break
            if first_vehicle_series == 0:
                for vehicle_series_option in vehicle_series_options:
                    if str(vehicle_series_option.text).lower() in vehicle_series.lower():
                        print vehicle_series_option.text
                        vehicle_series_option.click()
                        second_vehicle_series = 1
                        break
            if first_vehicle_series ==0 and second_vehicle_series == 0:
                for vehicle_series_option in vehicle_series_options:
                    if vehicle_series.lower() in str(vehicle_series_option.text).lower():
                        print vehicle_series_option.text
                        vehicle_series_option.click()
                        break
            time.sleep(1)
            vehicle_models_options = browser.find_element_by_id('sltSpecList').find_elements_by_tag_name('a')
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
            for vehicle_models_option in vehicle_models_options:
                if vehicle_style in str(vehicle_models_option.get_attribute('title')) and volume in str(vehicle_models_option.get_attribute('title')):
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
                    if vehicle_style in str(vehicle_models_option.get_attribute('title')) and volume in str(vehicle_models_option.get_attribute('title')):
                        vehicle_models_option.click()
                        print vehicle_models_option.get_attribute('title')
                        is_exist = 1 
                        break
            if is_exist == 0:
                continue 
            
            
            # ----------------  里程、售价 ------------------------
            printDelimiter()
            print u'里程：',shown_miles
            browser.find_element_by_id('carMileage').send_keys(shown_miles.decode('utf-8'))
            print u'售价：',owner_price
            browser.find_element_by_id('carPrice').send_keys(str(owner_price))
            istranses = browser.find_elements_by_name('istrans')
            for istrans in istranses:
                try:
                    istrans.click()
                except:
                    time.sleep(5)
            
            # ---------------- 车身颜色 ----------------------------
            printDelimiter()
            print u'车身颜色：',color.decode('utf-8')
            color_verify = ''
            color_options = browser.find_element_by_id('carColor').find_elements_by_tag_name('a')
            for color_option in color_options:
                if color in str(color_option.text):
                    color_option.click()
                    color_verify = str(color_option.text)
                    print color_option.text
                    break
            if color_verify == '':
                color_options[-1].click()
                print color_options[-1].text
            
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
                browser.find_element_by_id('sh_registe').click()
                register_date_year_options = browser.find_element_by_id('sh_registe_year').find_elements_by_tag_name('option')
                for register_date_year_option in register_date_year_options:
                    if register_date_year in str(register_date_year_option.text):
                        register_date_year_option.click()
                        print register_date_year_option.text
                        break
                    
                register_dates_month_options = browser.find_element_by_id('sh_registe_ul').find_elements_by_tag_name('a')
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
            browser.find_element_by_id('txtRemarkContent').send_keys(detail_info.decode('utf-8'))
             
     
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
                    if check_exists_by_id(browser,'flashObject1'):
                        photo_id = browser.find_element_by_id('flashObject1')
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
                if check_exists_by_id(browser,'flashObject1'):
                    photo_id = browser.find_element_by_id('flashObject1')
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
             
            if len(car_imgs)>15: 
                for i in range(3,15): 
                    print car_imgs[i]
                    third_element_fails = 0
                    while True:
                        if third_element_fails > 5:
                            break
                        if check_exists_by_id(browser,'flashObject1'):
                            photo_id = browser.find_element_by_id('flashObject1')
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
                        if check_exists_by_id(browser,'flashObject1'):
                            photo_id = browser.find_element_by_id('flashObject1')
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
            try:
                #browser.find_element_by_id('AddCar').submit()
            except:
                time.sleep(5)
                #browser.find_element_by_id('AddCar').submit()
                
            #time.sleep(10)
            #browser.quit()
              


if __name__ == "__main__":   
    post_cardata()
