# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
from StringIO import StringIO
import gzip
import cookielib
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import tempfile
import chardet
import MySQLdb

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException

from urllib2 import Request,urlopen,URLError,HTTPError

import time

import optparse

#登录地址
tbLoginUrl = "http://www.baixing.com/oz/login"
checkCodeUrl = ''
#post请求头部
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'www.baixing.com',
    'Origin':'http://www.baixing.com',
    'Referer':'http://www.baixing.com/oz/login',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'cookie':'__t=ut54b0e767662705.22113420; __u=130826894; __c=3bdc50072103a38bb65a1e0810d531ce956e1e4a;__n=%E7%99%BE%E5%A7%93_662967420354635;_auth_redirect=deleted; path=/; domain=baixing.com;httponly',
}




#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;



def get_car_info():
    try:
        conn = MySQLdb.connect(host='115.29.242.204',user='spider',passwd='spider')
        curs = conn.cursor()
        conn.select_db('tc5u')
        curs.execute("select (select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address),vmc.vehicle_model_conf53 as environmental_standards,vmc.vehicle_model_conf48 as fuel_form,vmc.vehicle_model_conf5 as car_level  from vehicle_info vi,vehicle_model vm,vehicle_model_conf vmc where vi.vehicle_number='32061101000014000000202764' and vm.id=vi.model_id and vmc.id=vi.model_id")
        getrows=curs.fetchall()
        if not getrows:
             pass
        else:
             return getrows
        conn.commit()
        curs.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)
    



def post_cardata():

    print "Usage: post_baixing.py -u yourbxUsername -p yourbxPassword"
    printDelimiter()

    parser = optparse.OptionParser()
    parser.add_option("-u","--username",action="store",type="string",default='',dest="username",help="Your baixing Username")
    parser.add_option("-p","--password",action="store",type="string",default='',dest="password",help="Your baixing password")
    (options, args) = parser.parse_args()
    
    ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address,environmental_standards,fuel_form,car_level),)=get_car_info()
    get_page_fails = 0
    try:
        browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8-linux-x86_64/bin/phantomjs',) 
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(60)
    except WebDriverException,e:
        print e
     
    if browser is not None:
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://nantong.baixing.com/oz/login")
                browser.implicitly_wait(10)
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        browser.find_element_by_id('id_identity').find_element_by_name('identity').send_keys(options.username)
        browser.find_element_by_id('id_password').find_element_by_name('password').send_keys(options.password)
        time.sleep(10)
        browser.find_element_by_id('id_submit').submit()
        print browser.find_element_by_id('welcome-info').find_element_by_class_name('dropdown-topbar').text
        while True:
            try:
                if get_page_fails > 10:
                    break
                browser.get("http://nantong.baixing.com/fabu/ershouqiche/?")
                browser.implicitly_wait(10)
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
            if str(brand_option.text) == brand:     
                print brand_option.text
                brand_option.click()
                time.sleep(5)
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
                time.sleep(5)
        
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
                time.sleep(5)
     
        if color_verify == '':
            color_options[-1].click()   
            time.sleep(5)

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
                time.sleep(5)

        if car_level_verify == '':
            car_level_options[-1].click()
            time.sleep(5)
   
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
                    time.sleep(5)
            register_dates_month = get_register_dates.find_element_by_name('年份[1]')
            register_dates_month_options = register_dates_month.find_elements_by_tag_name('option')
            for register_dates_month_option in register_dates_month_options:
                register_dates_month_str = re.findall('\d+',str(register_dates_month_option.text))
                if len(register_dates_month_str)>0:
                    if register_date_month[0] == '0':
                        if register_date_month[1] == register_dates_month_str[0]:
                            print "首次上牌月份：",register_dates_month_option.text
                            register_dates_month_option.click()
                            time.sleep(5)
                    else:
                        if register_date_month == register_dates_month_str[0]:
                            print "首次上牌月份：",register_dates_month_option.text
                            register_dates_month_option.click()
                            time.sleep(5)
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
                    time.sleep(5)
            inspection_dates_month = get_inspection_dates.find_element_by_name('年检[1]')
            inspection_dates_month_options = inspection_dates_month.find_elements_by_tag_name('option')
            for inspection_dates_month_option in inspection_dates_month_options:
                inspection_dates_month_str = re.findall('\d+',str(inspection_dates_month_option.text))
                if len(inspection_dates_month_str)>0:
                    if inspection_date_month[0] == '0':
                        if inspection_date_month[1] == inspection_dates_month_str[0]:
                            print "年检到期月份：",inspection_dates_month_option.text
                            inspection_dates_month_option.click()
                            time.sleep(5)
                    else:
                        if inspection_date_month == inspection_dates_month_str[0]:
                            print "年检到期月份：",inspection_dates_month_option.text
                            inspection_dates_month_option.click()
                            time.sleep(5)
        
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
                    time.sleep(5)
            force_insurance_dates_month = get_force_insurance_dates.find_element_by_name('交强险[1]')
            force_insurance_dates_month_options = force_insurance_dates_month.find_elements_by_tag_name('option')
            for force_insurance_dates_month_option in force_insurance_dates_month_options:
                force_insurance_dates_month_str = re.findall('\d+',str(force_insurance_dates_month_option.text))
                if len(force_insurance_dates_month_str)>0:
                    if force_insurance_date_month[0] == '0':
                        if force_insurance_date_month[1] == force_insurance_dates_month_str[0]:
                            print "交强险到期月份：",force_insurance_dates_month_option.text
                            force_insurance_dates_month_option.click()
                            time.sleep(5)
                    else:
                        if force_insurance_date_month == force_insurance_dates_month_str[0]:
                            print "交强险到期月份：",force_insurance_dates_month_option.text
                            force_insurance_dates_month_option.click()
                            time.sleep(5)

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
                    time.sleep(5)
            insurance_dates_month = get_insurance_dates.find_element_by_name('商业险[1]')
            insurance_dates_month_options = insurance_dates_month.find_elements_by_tag_name('option')
            for insurance_dates_month_option in insurance_dates_month_options:
                insurance_dates_month_str = re.findall('\d+',str(insurance_dates_month_option.text))
                if len(insurance_dates_month_str)>0:
                    if insurance_date_month[0] == '0':
                        if insurance_date_month[1] == insurance_dates_month_str[0]:
                            print "商业险到期月份：",insurance_dates_month_option.text
                            insurance_dates_month_option.click()
                            time.sleep(5)
                    else:
                        if insurance_date_month == insurance_dates_month_str[0]:
                            print "商业险到期月份：",insurance_dates_month_option.text
                            insurance_dates_month_option.click()
                            time.sleep(5)
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


        #return True
        time.sleep(10)
        browser.find_element_by_id('fabu-form-submit').submit()
        time.sleep(10)
        #browser.quit()



if __name__ == "__main__":   
    #loginTobaixing()
    post_cardata()
