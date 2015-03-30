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
        conn = MySQLdb.connect(host='218.244.135.238',user='spider',passwd='spider_tc5u',charset='utf8')
        curs = conn.cursor()
        conn.select_db('tc5u')
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
    #print file1
    img = Image.open(file1)
    #print img.info,img.size,img.format
    img = img.convert("RGBA")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
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
        x = 3 + i*21
        y = 4 
        temp = img.crop((x, y, x+8,y+10))
        temp.save("C:\Python27\Bulk_Posting\iautos_temp\%d.png" % nume)
        nume=nume+1
        font.append(temp)
    return font


def recognize(img):
    fontMods = []
    image_num = ['2','22','222','3','33','333','3333','4','44','444','4444','5','55','555','6','66','666','7','77','8','88','888','9','99','999','A','AA','AAA','AAAA','AAAAA','B','BB','BBB','C','CC','D','DD','DDD','DDDD','E','EE','EEE','EEEE','F','FF','FFF','G','GG','GGG','GGGG','H','HH','HHH','I','II','III','J','JJ','JJJ','JJJJ','K','KK','KKK','KKKK','M','MM','MMM','MMMM','N','NN','NNN','NNNN','P','PP','PPP','PPPP','Q','QQ','QQQ','QQQQ','QQQQQ','R','RR','S','SS','SSS','SSSS','T','TT','TTT','TTTT','TTTTT','U','UU','UUU','V','VV','VVV','W','WW','WWW','WWWW','X','XX','XXX','Y','YY','YYY','Z','ZZ','ZZZ','ZZZZ','ZZZZZ']
    for i in image_num:
        fontMods.append((str(i), Image.open("C:\Python27\Bulk_Posting\iautos_fonts\%s.png" % i)))
    result=""
    font=division(img)
    for i in font:
        target=i
        points = []
        for mod in fontMods:
            diffs = 0
            for yi in range(10):
                for xi in range(8):     
                    if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                        diffs += 1
            print diffs
            points.append((diffs, mod[0]))
        points.sort()
        if "A" in points[0][1]:
            result += "A"
        elif "B" in points[0][1]:
            result += "B"
        elif "C" in points[0][1]:
            result += "C"
        elif "D" in points[0][1]:
            result += "D"
        elif "E" in points[0][1]:
            result += "E"        
        elif "F" in points[0][1]:
            result += "F"
        elif "G" in points[0][1]:
            result += "G"
        elif "H" in points[0][1]:
            result += "H"
        elif "I" in points[0][1]:
            result += "I" 
        elif "J" in points[0][1]:
            result += "J"
        elif "K" in points[0][1]:
            result += "K"
        elif "M" in points[0][1]:
            result += "M"
        elif "N" in points[0][1]:
            result += "N"        
        elif "P" in points[0][1]:
            result += "P"
        elif "Q" in points[0][1]:
            result += "Q"
        elif "R" in points[0][1]:
            result += "R"
        elif "S" in points[0][1]:
            result += "S"
        elif "T" in points[0][1]:
            result += "T"
        elif "U" in points[0][1]:
            result += "U"
        elif "V" in points[0][1]:
            result += "V"
        elif "W" in points[0][1]:
            result += "W"        
        elif "X" in points[0][1]:
            result += "X"
        elif "Y" in points[0][1]:
            result += "Y"
        elif "Z" in points[0][1]:
            result += "Z"
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
        chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        browser = webdriver.Chrome(chromedriver)
        #browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        #browser = webdriver.Firefox()
        browser.implicitly_wait(5)
        browser.set_page_load_timeout(30)
    except WebDriverException,e:
        print e
    if browser is not None:
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://www.iautos.cn/user/login/#")
                browser.implicitly_wait(5)              
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        time.sleep(1)
        browser.find_element_by_id('username').send_keys(options.username.decode('gb2312'))
        browser.find_element_by_id('password').send_keys(options.password)
        validate_code_img = browser.find_element_by_id('captcha')
        ActionChains(browser).context_click(validate_code_img).perform()
        time.sleep(1)
#         # ----------- firefox -------------------
#         for x in range(10):
#             win32api.keybd_event(40,0,0,0)
#             time.sleep(0.1)
#         win32api.keybd_event(13,0,0,0)
#         time.sleep(1)
#         #ActionChains(browser).move_by_offset(0,100).perform()
#         #ActionChains(browser).click().perform()
#         win32api.keybd_event(40,0,win32con.KEYEVENTF_KEYUP,0)
#         win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
#         autoit = win32com.client.Dispatch("AutoItX3.Control")
#         #ControlFocus("title","text",controlID) Edit1=Edit instance 1
#         autoit.ControlFocus(u"保存图像", "","Edit1")
#         #Wait 10 seconds for the Upload window to appear
#         autoit.WinWait("[CLASS:#32770]","",5)
#         # Set the File name text on the Edit field
#         autoit.ControlSetText(u"保存图像", "", "Edit1", "C:\Python27\Bulk_Posting\iautos_validate_code\index.php.png")
#         time.sleep(1)
#         #Click on the Open button
#         autoit.ControlClick(u"保存图像", "","Button1")
#         time.sleep(1)
#         try:
#             autoit.ControlClick(u"确认另存为","","Button1")
#             time.sleep(1)
#         except:
#             print "The image is not exists..."
        # ----------------chrome -------------------
        for x in range(6):
            win32api.keybd_event(40,0,0,0)
            time.sleep(0.1)
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
        autoit.ControlSetText(u"另存为", "", "Edit1", "C:\Python27\Bulk_Posting\iautos_validate_code\index.php.png")
        time.sleep(1)
        #Click on the Open button
        autoit.ControlClick(u"另存为", "","Button1")
        time.sleep(1)
        try:
            autoit.ControlClick(u"确认另存为","","Button1")
            time.sleep(1)
        except:
            print "The image is not exists..."
        img_src = "C:\Python27\Bulk_Posting\iautos_validate_code\index.php.png" 
        #urllib.urlretrieve(validate_code_url, "captcha.png")
        #browser.save_screenshot("screenshot.png")
        
        images = binary(img_src)
        num = recognize(images)
        print num
#         numbers = raw_input("please input the validate code: ")
        browser.find_element_by_id('validatecode').send_keys(num)
        browser.find_element_by_id('remember').click()
        browser.find_element_by_id('btnSubmit').click()
        time.sleep(5)
        print 'test...'
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
                    browser.get("http://www.iautos.cn/shopadmin/usedcar/addusedcar/")
                    browser.implicitly_wait(5)
                    wait = ui.WebDriverWait(browser,30)
                except:
                    get_publish_page_fails += 1
                    print "get page info failed ... ",get_publish_page_fails
                else:
                    break
             
            
            # ----------------- 所在地 -------------------------
            wait.until(EC.element_to_be_clickable((By.ID,"selected_proper")))
            browser.find_element_by_id('selected_proper').click()
            addrs_detail = u'新区'
            addrs_options = browser.find_element_by_id('proper').find_elements_by_tag_name('a')
            for addrs_option in addrs_options:
                if addrs_detail in str(addrs_option.text):
                    addrs_option.click()
                    break
            
            # ------------------ brands ---------------------
            printDelimiter()
            print u"品牌首字母:",brand_initial
            print u"品牌:",brand.decode('utf-8')
            print u"车系:",vehicle_series.decode('utf-8')
            print u"车型:",vehicle_model.decode('utf-8')
             
            wait.until(EC.element_to_be_clickable((By.ID,"car_brand")))
            browser.find_element_by_id('car_brand').click()
            time.sleep(1)
            brand_lists = browser.find_element_by_id('pp_s2').find_elements_by_tag_name('li')
            verify_brand = 0
            for brand_list in brand_lists:
                if str(brand_list.find_element_by_tag_name('span').text) != brand_initial:
                    continue
                else:
                    brand_options = brand_list.find_elements_by_tag_name('a')
                    first_brand = 0
                    second_brand = 0
                    for brand_option in brand_options:
                        if str(brand_option.text).lower() == brand.lower():
                            print brand_option.text
                            brand_option.click()
                            first_brand = 1
                            verify_brand = 1
                            break
                    if first_brand == 0:
                        for brand_option in brand_options:
                            if str(brand_option.text).lower() in brand.lower():
                                print brand_option.text
                                brand_option.click()
                                second_brand = 1
                                verify_brand = 1
                                break
                    if first_brand == 0 and second_brand == 0:
                        for brand_option in brand_options:
                            if brand.lower() in str(brand_option.text).lower():
                                print brand_option.text
                                brand_option.click()
                                verify_brand = 1
                                break
            time.sleep(2)
            if verify_brand == 0:
                continue
            
            # ------------------- vehicle_series -------------------------
#             wait.until(EC.element_to_be_clickable((By.ID,"series_name")))
#             browser.find_element_by_id('series_name').click()
#             time.sleep(1)
            browser.execute_script("document.getElementById('cx_s2').setAttribute('style','display: block;')")
            vehicle_series_options = browser.find_element_by_id('cx_s2').find_elements_by_tag_name('a')
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
            if first_vehicle_series ==0 and second_vehicle_series == 0:
                for vehicle_series_option in vehicle_series_options:
                    if vehicle_series.lower() in str(vehicle_series_option.text).lower():
                        print vehicle_series_option.text
                        vehicle_series_option.click()
                        verify_vehicle_series = 1
                        break
            time.sleep(1)
            if verify_vehicle_series == 0:
                continue
            
            
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
            
            
            # ------------------ 购买年份 ----------------------
#             wait.until(EC.element_to_be_clickable((By.ID,"car_year")))
#             browser.find_element_by_id('car_year').click()
#             time.sleep(1)
            browser.execute_script("document.getElementById('nf_s2').setAttribute('style','display: block;')")
            buy_year_options = browser.find_element_by_id('nf_s2').find_elements_by_tag_name('a')
            for buy_year_option in buy_year_options:
                if str(buy_year_option.text) == register_date_year:
                    buy_year_option.click()
                    break
            
            # ------------------ vehicle models ------------------------
#             wait.until(EC.element_to_be_clickable((By.ID,"car_modleName")))
#             browser.find_element_by_id('car_modleName').click()
#             time.sleep(1)
            browser.execute_script("document.getElementById('car_modleName').setAttribute('style','display: block;')")
            printDelimiter()
            print u"排量：",volume.decode('utf-8')
            volume_options = browser.find_element_by_id('pl').find_elements_by_tag_name('span')
            for volume_option in volume_options:
                if volume[:-1] in str(volume_option.text):
                    volume_option.click()
                    break
            printDelimiter()
            print u"变速箱：",transmission.decode('utf-8')
            transmission_options = browser.find_element_by_id('bsfs').find_elements_by_tag_name('span')
            for transmission_option in transmission_options:
                if transmission in str(transmission_option.text):
                    transmission_option.click()
                    break
            is_exist = 0
            print u"年款：",vehicle_style.decode('utf-8')
            print u"环保标准：",environmental_standards.decode('utf-8')
            vehicle_models_uls = browser.find_element_by_id('car_model').find_elements_by_tag_name('ul')
            for vehicle_models_ul in vehicle_models_uls:
                if str(vehicle_models_ul.get_attribute('yid')) in vehicle_style:
                    vehicle_models_options = vehicle_models_ul.find_elements_by_tag_name('a')
                    for vehicle_models_option in vehicle_models_options:
                        # 环保标准可能为 国IV+OBD
                        if u'国IV' in environmental_standards:
                            if u'国Ⅳ' in str(vehicle_models_option.text):
                                vehicle_models_option.click()
                                is_exist = 1
                                break
                        elif u'国II' in environmental_standards:
                            if u'国Ⅱ' in str(vehicle_models_option.text):
                                vehicle_models_option.click()
                                is_exist = 1
                                break
                        elif u'国III' in environmental_standards:
                            if u'国Ⅲ' in str(vehicle_models_option.text):
                                vehicle_models_option.click()
                                is_exist = 1
                                break
                        elif u'国V' in environmental_standards:
                            if u'国Ⅴ' in str(vehicle_models_option.text):
                                vehicle_models_option.click()
                                is_exist = 1
                                break
                
                    if is_exist == 0:
                        vehicle_models_options[0].click()
                        break
                 
            
            
            
            # -------------- 首次上牌 ---------------------------
            printDelimiter()
            print u'首次上牌：',register_date
            if register_date is not None:
                wait.until(EC.element_to_be_clickable((By.ID,"regdate_year")))
                browser.find_element_by_id('regdate_year').click()
                register_date_year_options = browser.find_element_by_id('scspsjnf_s2').find_elements_by_tag_name('a')
                for register_date_year_option in register_date_year_options:
                    if register_date_year in str(register_date_year_option.text):
                        register_date_year_option.click()
                        print register_date_year_option.text
                        break
                
                wait.until(EC.element_to_be_clickable((By.ID,"regdate_month")))
                browser.find_element_by_id('regdate_month').click()
                register_dates_month_options = browser.find_element_by_id('scspsjyf_s2').find_elements_by_tag_name('a')
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
                browser.find_element_by_id('is_regdate').click()  
                
            # -------------- 交强险到期 ---------------------------
            printDelimiter()
            print u'交强险到期：',force_insurance_date
            if force_insurance_date is not None:
                wait.until(EC.element_to_be_clickable((By.ID,"roadMaintance_fee_year")))
                browser.find_element_by_id('roadMaintance_fee_year').click()
                force_insurance_date_year_options = browser.find_element_by_id('jqxnf_s2').find_elements_by_tag_name('a')
                for force_insurance_date_year_option in force_insurance_date_year_options:
                    if force_insurance_date_year in str(force_insurance_date_year_option.text):
                        force_insurance_date_year_option.click()
                        print force_insurance_date_year_option.text
                        break
                
                wait.until(EC.element_to_be_clickable((By.ID,"roadMaintance_fee_month")))
                browser.find_element_by_id('roadMaintance_fee_month').click()
                force_insurance_dates_month_options = browser.find_element_by_id('jqxyf_s2').find_elements_by_tag_name('a')
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
            else:
                wait.until(EC.element_to_be_clickable((By.ID,"roadMaintance_fee_year")))
                browser.find_element_by_id('roadMaintance_fee_year').click()
                browser.find_element_by_id('jqxnf_s2').find_elements_by_tag_name('a')[0].click() 
            
            # -------------- 商业险到期 ---------------------------
            printDelimiter()
            print u'商业险到期：',insurance_date
            if insurance_date is not None:
                wait.until(EC.element_to_be_clickable((By.ID,"insurance_year")))
                browser.find_element_by_id('insurance_year').click()
                insurance_date_year_options = browser.find_element_by_id('syxnf_s2').find_elements_by_tag_name('a')
                for insurance_date_year_option in insurance_date_year_options:
                    if insurance_date_year in str(insurance_date_year_option.text):
                        insurance_date_year_option.click()
                        print insurance_date_year_option.text
                        break
                
                wait.until(EC.element_to_be_clickable((By.ID,"insurance_month")))
                browser.find_element_by_id('insurance_month').click()
                insurance_dates_month_options = browser.find_element_by_id('syxyf_s2').find_elements_by_tag_name('a')
                for insurance_dates_month_option in insurance_dates_month_options:
                    if insurance_date_month[0] == '0':
                        if insurance_date_month[1] in str(insurance_dates_month_option.text):
                            insurance_dates_month_option.click()
                            time.sleep(1)
                            print insurance_date_month
                            break
                    else:
                        if insurance_date_month in str(insurance_dates_month_option.text):
                            insurance_dates_month_option.click()
                            time.sleep(1)
                            print insurance_date_month
                            break
            else:
                wait.until(EC.element_to_be_clickable((By.ID,"insurance_year")))
                browser.find_element_by_id('insurance_year').click()
                browser.find_element_by_id('syxnf_s2').find_elements_by_tag_name('a')[0].click()           
             
            # ----------------  里程、售价 ------------------------
            printDelimiter()
            print u'里程：',shown_miles
            browser.find_element_by_id('km').send_keys(shown_miles.decode('utf-8'))
            print u'售价：',owner_price
            browser.find_element_by_id('price').send_keys(str(owner_price))
            print u'原车用途：非运营'
            browser.find_element_by_id('ycyt').find_element_by_tag_name('span').click()
            print u'内饰颜色：深内饰'
            browser.find_element_by_id('nsys').find_element_by_tag_name('span').click()
            print u'保养记录：齐全'
            browser.find_element_by_id('byjl').find_element_by_tag_name('span').click()
            print u'是否一手车：是'
            browser.find_element_by_id('ghcs').find_element_by_tag_name('span').click()
             
            # ---------------- 车身颜色 ----------------------------
            printDelimiter()
            print u'车身颜色：',color.decode('utf-8')
            color_verify = 0
            color_options = browser.find_element_by_id('csys').find_elements_by_tag_name('span')
            for color_option in color_options:
                if color in str(color_option.text):
                    color_option.click()
                    color_verify = 1
                    print color_option.text
                    break
            if color_verify == 0:
                color_options[-1].click()
                print color_options[-1].text
             


               
            # ------------- 补充说明 -------------------------
            printDelimiter()
            print u"补充说明"
            detail_info = u"""  淘车乐微信：“南通淘车乐二手车”（微信号：nt930801） ，海量车源在线看。
  淘车乐服务 ：二手车寄售、二手车购买、二手车零首付贷款、二手车评估认证。
  淘车乐地址：南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)
  公交路线 ：可乘坐3路、10路、600路、602路到果园站下车。沿城港路走30米左转进入兴泰路走200米。
  淘车乐，帮您实现有车生活。"""
            browser.find_element_by_id('subtitle').send_keys(u'淘车乐认证首付30%')
            browser.find_element_by_id('liuyanArea').send_keys(detail_info.decode('utf-8'))
            
            # -----------行驶证、登记证、购车发票 -----------------------
            printDelimiter()
            print u"行驶证、登记证、购车发票"
            browser.find_element_by_id('xsz').find_element_by_tag_name('span').click()
            browser.find_element_by_id('djz').find_element_by_tag_name('span').click()
            browser.find_element_by_id('gcfp').find_element_by_tag_name('span').click()
      
            # ------------- 上传车辆图片 ------------------
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            car_imgs = get_car_info(vehicle_num)[1]
     		# ------------- 1.车辆封面照 ------------------           
            for i in range(3):
                print car_imgs[i]
                wait.until(EC.element_to_be_clickable((By.ID,"iautosFlash1")))
                browser.find_element_by_id('iautosFlash1').click()
                #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
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
                
            # ------------- 2.卖场二维码 ------------------
            print "two-dimensional bar code"
            print car_imgs[i]
            wait.until(EC.element_to_be_clickable((By.ID,"iautosFlash1")))
            browser.find_element_by_id('iautosFlash1').click()
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
              
            # -------------- 3.其他车辆图片 -------------------
            for i in range(3,len(car_imgs)): 
                print car_imgs[i]
                wait.until(EC.element_to_be_clickable((By.ID,"iautosFlash1")))
                browser.find_element_by_id('iautosFlash1').click()
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
#                 #browser.find_element_by_id('AddCar').submit()
#             except:
#                 #time.sleep(5)
#                 #browser.find_element_by_id('AddCar').submit()
#                 
#             #time.sleep(10)
#             #browser.quit()
              


if __name__ == "__main__":   
    post_cardata()
