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



#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;



def get_car_info(vehicle_nums):
    imgurls = []
    try:
        conn = MySQLdb.connect(host='',user='spider',passwd='s',charset='utf8')
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
        browser = webdriver.Firefox()
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
        browser.find_element_by_id('id_identity').find_element_by_name('identity').send_keys(options.username)
        browser.find_element_by_id('id_password').find_element_by_name('password').send_keys(options.password)
        time.sleep(5)
        browser.find_element_by_id('id_submit').submit()
        print browser.find_element_by_id('welcome-info').find_element_by_class_name('dropdown-topbar').text
     
        vehicle_nums = ['32010401000003900000204335','32010402000002950000204333','32010401000002920000204320','32010402000002720000204323','32010401000003590000204324','32010401000012150000204330','32010401000011450000204327','32010401000008520000204328','32010401000004250000204317','32010401000008490000204315']
        for vehicle_num in vehicle_nums:
            if len(get_car_info(vehicle_num)) > 1:
                ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info(vehicle_num)[0]
            else:
                return False
            
            while True:
                try:
                    if get_page_fails > 10:
                        break
                    browser.get("http://nanjing.baixing.com/fabu/ershouqiche/?")
                    browser.implicitly_wait(10)
                    time.sleep(3)
                except:
                    get_page_fails += 1
                    print "get page info failed ... ",get_page_fails
                else:
                    break
            #print chardet.detect(vehicle_model.decode('utf-8'))
            print type(vehicle_model.decode('utf-8'))
            #print chardet.detect(volume.decode('ascii'))
            #print type(volume.decode('ascii'))
            #print volume[:3]
            
            #print len(volume)
            #print type(shown_miles)
            #print type(owner_price)
    
            
            # ------------------ brands ---------------------
            printDelimiter()
            print "品牌:",brand
            div = browser.find_element_by_id('id_车品牌')
            get_brands = div.find_element_by_tag_name('select')
            brand_options = get_brands.find_elements_by_tag_name('option')
            for brand_option in brand_options:
                #print option.text,type(option.text),chardet.detect(str(option.text))
                if str(brand_option.text).lower() == brand.lower():     
                    print brand_option.text
                    brand_option.click()
                    time.sleep(3)
                    break
                elif str(brand_option.text).lower() in brand.lower():
                    print brand_option.text
                    brand_option.click()
                    time.sleep(3)
                    break
                elif brand.lower() in str(brand_option.text).lower():
                    print brand_option.text
                    brand_option.click()
                    time.sleep(3)
                    break
            moreinfo = browser.find_element_by_id('moreinfo')
            span = moreinfo.find_element_by_class_name('button-show')
            span.click()
            #print browser.find_element_by_id('id_燃油类型').text
            
            # --------------------------------------------
            printDelimiter()
            print "title、行驶里程、价格、排量、燃油类型、排放标准"
            browser.find_element_by_id('id_title').find_element_by_tag_name('input').send_keys(vehicle_model.decode('utf-8'))
            browser.find_element_by_id('id_行驶里程').find_element_by_tag_name('input').send_keys(shown_miles.decode('utf-8'))
            browser.find_element_by_id('id_价格').find_element_by_tag_name('input').send_keys(str(owner_price))
            browser.find_element_by_id('id_排量').find_element_by_tag_name('input').send_keys(str(volume[:3]))
            browser.find_element_by_id('id_燃油类型').find_element_by_tag_name('input').send_keys(fuel_form.decode('utf-8'))        
            browser.find_element_by_id('id_排放标准').find_element_by_tag_name('input').send_keys(environmental_standards.decode('utf-8'))  
            detail_info = """
            淘车乐承诺：重大事故车、泡水车，包退款。
            淘车乐覆盖：大众 本田 丰田 日产 奥迪 奔驰 别克 马自达 现代 雪铁龙 标致 江淮 三菱 铃木 只要你想要 统统都有。南京最全车辆信息，我们没有，南京都没有。
            淘车乐贷款：赚普桑级别的工资 开宝马级别的豪车 你要你想要 我就给你买 买！买！买！买！买！
            淘车乐地址 ：南京市江宁区秦淮路63号南京淘车乐认证二手车卖场（江宁区车管局斜对面） （交通：地铁1号线河定桥站乘坐802、866、867路至通淮街站下。河定桥欧尚超市向西1公里，新奇特汽车超市旁）
            
            淘车乐微信：搜索订阅号“南京淘车乐”或“tcl282”
            
            淘车乐，帮您实现有车生活
            """
            browser.find_element_by_id('id_content').find_element_by_tag_name('textarea').send_keys(detail_info.decode('utf-8'))
    		
            # ----------- transmissions -------------------
            printDelimiter()
            print "变速箱:",transmission
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
            print "车身颜色:",color
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
            print "车身级别:",car_level
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
            print "首次上牌:",register_date
            if register_date is not None:
                get_register_dates = browser.find_element_by_id('id_年份')
                register_dates_year = get_register_dates.find_element_by_name('年份[0]')
                register_dates_year_options = register_dates_year.find_elements_by_tag_name('option')
                for register_dates_year_option in register_dates_year_options:
                    if register_date_year in str(register_dates_year_option.text):
                        print "首次上牌年份：",register_dates_year_option.text
                        register_dates_year_option.click()
                        time.sleep(3)
                register_dates_month = get_register_dates.find_element_by_name('年份[1]')
                register_dates_month_options = register_dates_month.find_elements_by_tag_name('option')
                for register_dates_month_option in register_dates_month_options:
                    register_dates_month_str = re.findall('\d+',str(register_dates_month_option.text))
                    if len(register_dates_month_str)>0:
                        if register_date_month[0] == '0':
                            if register_date_month[1] == register_dates_month_str[0]:
                                print "首次上牌月份：",register_dates_month_option.text
                                register_dates_month_option.click()
                                time.sleep(3)
                        else:
                            if register_date_month == register_dates_month_str[0]:
                                print "首次上牌月份：",register_dates_month_option.text
                                register_dates_month_option.click()
                                time.sleep(3)
            # ------------- 年检到期 ---------------------
            printDelimiter()
            print "年检到期:",inspection_date
            if inspection_date is not None:
                get_inspection_dates = browser.find_element_by_id('id_年检')
                inspection_dates_year = get_inspection_dates.find_element_by_name('年检[0]')
                inspection_dates_year_options = inspection_dates_year.find_elements_by_tag_name('option')
                for inspection_dates_year_option in inspection_dates_year_options:
                    if inspection_date_year in str(inspection_dates_year_option.text):
                        inspection_dates_year_option.click()
                        time.sleep(3)
                inspection_dates_month = get_inspection_dates.find_element_by_name('年检[1]')
                inspection_dates_month_options = inspection_dates_month.find_elements_by_tag_name('option')
                for inspection_dates_month_option in inspection_dates_month_options:
                    inspection_dates_month_str = re.findall('\d+',str(inspection_dates_month_option.text))
                    if len(inspection_dates_month_str)>0:
                        if inspection_date_month[0] == '0':
                            if inspection_date_month[1] == inspection_dates_month_str[0]:
                                print "年检到期月份：",inspection_dates_month_option.text
                                inspection_dates_month_option.click()
                                time.sleep(3)
                        else:
                            if inspection_date_month == inspection_dates_month_str[0]:
                                print "年检到期月份：",inspection_dates_month_option.text
                                inspection_dates_month_option.click()
                                time.sleep(3)
            
            # ------------- 交强险到期 ---------------------
            printDelimiter()
            print "交强险到期:",force_insurance_date
            if force_insurance_date is not None:
                get_force_insurance_dates = browser.find_element_by_id('id_交强险')
                force_insurance_dates_year = get_force_insurance_dates.find_element_by_name('交强险[0]')
                force_insurance_dates_year_options = force_insurance_dates_year.find_elements_by_tag_name('option')
                for force_insurance_dates_year_option in force_insurance_dates_year_options:
                    if force_insurance_date_year in str(force_insurance_dates_year_option.text):
                        force_insurance_dates_year_option.click()
                        time.sleep(3)
                force_insurance_dates_month = get_force_insurance_dates.find_element_by_name('交强险[1]')
                force_insurance_dates_month_options = force_insurance_dates_month.find_elements_by_tag_name('option')
                for force_insurance_dates_month_option in force_insurance_dates_month_options:
                    force_insurance_dates_month_str = re.findall('\d+',str(force_insurance_dates_month_option.text))
                    if len(force_insurance_dates_month_str)>0:
                        if force_insurance_date_month[0] == '0':
                            if force_insurance_date_month[1] == force_insurance_dates_month_str[0]:
                                print "交强险到期月份：",force_insurance_dates_month_option.text
                                force_insurance_dates_month_option.click()
                                time.sleep(3)
                        else:
                            if force_insurance_date_month == force_insurance_dates_month_str[0]:
                                print "交强险到期月份：",force_insurance_dates_month_option.text
                                force_insurance_dates_month_option.click()
                                time.sleep(3)
    
            # ------------- 商业险到期 ---------------------
            printDelimiter()
            print "商业险到期:",insurance_date
            if insurance_date is not None:
                get_insurance_dates = browser.find_element_by_id('id_商业险')
                insurance_dates_year = get_insurance_dates.find_element_by_name('商业险[0]')
                insurance_dates_year_options = insurance_dates_year.find_elements_by_tag_name('option')
                for insurance_dates_year_option in insurance_dates_year_options:
                    if insurance_date_year in str(insurance_dates_year_option.text):
                        insurance_dates_year_option.click()
                        time.sleep(3)
                insurance_dates_month = get_insurance_dates.find_element_by_name('商业险[1]')
                insurance_dates_month_options = insurance_dates_month.find_elements_by_tag_name('option')
                for insurance_dates_month_option in insurance_dates_month_options:
                    insurance_dates_month_str = re.findall('\d+',str(insurance_dates_month_option.text))
                    if len(insurance_dates_month_str)>0:
                        if insurance_date_month[0] == '0':
                            if insurance_date_month[1] == insurance_dates_month_str[0]:
                                print "商业险到期月份：",insurance_dates_month_option.text
                                insurance_dates_month_option.click()
                                time.sleep(3)
                        else:
                            if insurance_date_month == insurance_dates_month_str[0]:
                                print "商业险到期月份：",insurance_dates_month_option.text
                                insurance_dates_month_option.click()
                                time.sleep(3)
            # ------------- 承担过户费 ---------------------
            printDelimiter()
            print "承担过户费"
            browser.find_element_by_id('id_承担过户费').find_element_by_tag_name('input').click()
    
            # ------------- 行驶证 ---------------------
            printDelimiter()
            print "行驶证"
            browser.find_element_by_id('id_行驶证').find_element_by_tag_name('input').click()
                 
            # ------------- 登记证 ---------------------
            printDelimiter()
            print "登记证"
            browser.find_element_by_id('id_登记证').find_element_by_tag_name('input').click()
    
            # ------------- 购车发票 ---------------------
            printDelimiter()
            print "购车发票"
            browser.find_element_by_id('id_购车发票').find_element_by_tag_name('input').click()
    
            # ------------- 维修记录 ---------------------
            printDelimiter()
            print "维修记录"
            browser.find_element_by_id('id_维修记录').find_element_by_tag_name('input').click()
    
            # ------------- 购置税 ---------------------
            printDelimiter()
            print "购置税"
            browser.find_element_by_id('id_购置税').find_element_by_tag_name('input').click()
    
            # ------------- 重大事故 ---------------------
            printDelimiter()
            print "重大事故"
            accident = browser.find_element_by_id('id_重大事故')
            accident_res = accident.find_elements_by_tag_name('input')
            accident_res[1].click()
    
            # ------------- 能否过户 ---------------------
            printDelimiter()
            print "能否过户"
            browser.find_element_by_id('id_能否过户').find_element_by_tag_name('input').click()
            
            # ------------- 能否按揭 ---------------------
            printDelimiter()
            print "能否按揭"
            browser.find_element_by_id('id_能否按揭').find_element_by_tag_name('input').click()
            
            # ------------- 上传车辆图片 ------------------
            autoit = win32com.client.Dispatch("AutoItX3.Control")
    		# ------------- 1.车辆封面照 ------------------
            car_imgs = get_car_info(vehicle_num)[1]
            print "cover image..."
            browser.find_element_by_id('SWFUpload_0').click()
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",10)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[0])
            time.sleep(5)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(10)
            
            print "two-dimensional bar code"
            browser.find_element_by_id('SWFUpload_0').click()
            #ControlFocus("title","text",controlID) Edit1=Edit instance 1
            autoit.ControlFocus(u"打开", "","Edit1")
            #Wait 10 seconds for the Upload window to appear
            autoit.WinWait("[CLASS:#32770]","",10)
            # Set the File name text on the Edit field
            autoit.ControlSetText(u"打开", "", "Edit1", "C:\\Users\\Administrator\\Desktop\\image\\nanjing\\nanjing.jpg")
            time.sleep(5)
            #Click on the Open button
            autoit.ControlClick(u"打开", "","Button1")
            time.sleep(10)
    		
            print "upload two-dimensional bar code finished ..."
            for i in range(1,len(car_imgs)):
                print car_imgs[i]
                browser.find_element_by_id('SWFUpload_0').click()
                
                #ControlFocus("title","text",controlID) Edit1=Edit instance 1
                autoit.ControlFocus(u"打开", "","Edit1")
                #Wait 10 seconds for the Upload window to appear
                autoit.WinWait("[CLASS:#32770]","",10)
                # Set the File name text on the Edit field
                autoit.ControlSetText(u"打开", "", "Edit1", car_imgs[i])
                time.sleep(5)
                #Click on the Open button
                autoit.ControlClick(u"打开", "","Button1")
                time.sleep(10)
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
            time.sleep(5)
            browser.find_element_by_id('fabu-form-submit').submit()
            #time.sleep(10)
            #browser.quit()



if __name__ == "__main__":   
    #loginTobaixing()
    post_cardata()
