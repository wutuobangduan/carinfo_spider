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

#用户名，密码
password = "654321"
#请求数据包

tokenVal = ''

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
     def http_error_301(self, req, fp, code, msg, httpmsg):
         print httpmsg.headers
         return urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, httpmsg)

     def http_error_302(self, req, fp, code, msg, httpmsg):
         print httpmsg.headers
         return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, httpmsg)




def get_args(myUrl):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(myUrl,headers=heads)
    fails = 0
    html = None
    global tokenVal
    while True:
        try:
            if fails >= 10:
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    if html is not None:
        soup = BeautifulSoup(html)
        for token in soup.find_all('input',attrs={'name':'token','type':'hidden'}):
            tokenVal = token.get('value')
        print "token value is : ",tokenVal
   

#get_args('http://passport.58.com/login')


def checkAllCookiesExist(cookieNameList, cookieJar) :
    cookiesDict = {};
    for eachCookieName in cookieNameList :
        cookiesDict[eachCookieName] = False;
    
    allCookieFound = True;
    for cookie in cookieJar :
        if(cookie.name in cookiesDict) :
            cookiesDict[cookie.name] = True;
    
    for eachCookie in cookiesDict.keys() :
        if(not cookiesDict[eachCookie]) :
            allCookieFound = False;
            break;

    return allCookieFound;

#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;

def loginTobaixing():
    #cookie 自动处理器
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
   
    printDelimiter()
    print "[step1] to get cookie"
    
    request = urllib2.Request(tbLoginUrl)
    for index, cookie in enumerate(cj):
        print '[',index, ']',cookie
    
    response = opener.open(request)
    cookie = response.info().getheader('Set-Cookie')
    #headers['cookie'] = cookie
    #print response.info(),response.getcode()
    printDelimiter();
    print "[step2] to get token value";
    get_args(tbLoginUrl)
    printDelimiter();
    print "[step3] emulate login" 
    
    postData = {
        'identity':identity,
        'password':password,
        'token':tokenVal,
    }
    #print headers
    sendPostData(tbLoginUrl, postData, headers)

    cookiesToCheck = ['__trackId','__uuid','__uuid']
    loginbaixingOK = checkAllCookiesExist(cookiesToCheck, cj)
    print loginbaixingOK
    login_baixing('http://nantong.baixing.com/fabu/ershouqiche/?')
    post_cardata('http://nantong.baixing.com/fabu/ershouqiche/?')   
    #headers2 = {
    #    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #    'Accept-Encoding':'gzip,deflate',
    #    'Accept-Language':'zh-CN,zh;q=0.8',
    #    'Cache-Control':'max-age=0',
    #    'Connection':'keep-alive',
    #    'Content-Type':'application/x-www-form-urlencoded',
    #    'Host':'nantong.baixing.com',
    #    'Referer':'http://nantong.baixing.com/fabu/cheliang',
    #    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    #    'cookie':'__t=ut54b0e767662705.22113420; __u=130826894; __c=3bdc50072103a38bb65a1e0810d531ce956e1e4a;__n=%E7%99%BE%E5%A7%93_662967420354635;_auth_redirect=http%3A%2F%2Fnantong.baixing.com%2F; path=/; domain=baixing.com;httponly',
    #}
    #sendPostData('http://nantong.baixing.com/fabu/ershouqiche/?',carData,headers2)
    #((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address),)=get_car_info()
    #cookiesToCheck = ['__trackId','__uuid','__uuid']
    #loginbaixingOK = checkAllCookiesExist(cookiesToCheck, cj)
    #print loginbaixingOK   
    #print brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address
     


def get_car_info():
    try:
        conn = MySQLdb.connect(host='115.29.242.204',user='spider',passwd='spider')
        curs = conn.cursor()
        conn.select_db('tc5u')
        curs.execute("select (select dd.field_value from data_dictionary dd where dd.id=vm.brand),(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_series),(select dd.field_value from data_dictionary dd where dd.id=vm.volume),vm.vehicle_model,(select dd.field_value from data_dictionary dd where dd.id=vm.vehicle_style),(select dd.field_value from data_dictionary dd where dd.id=vm.transmission),register_date,shown_miles,(select field_value from data_dictionary dd where dd.id=vi.vehicle_color),inspection_date,force_insurance_date,insurance_date,owner_price,(select field_value from data_dictionary dd where dd.id=vi.address) from vehicle_info vi,vehicle_model vm where vi.vehicle_number='32061101000014000000202764' and vm.id=vi.model_id")
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
    

#get_car_info()


def login_baixing(myUrl):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(myUrl,headers=heads)
    html = ''
    fails = 0
    while True:
        try:
            if fails >= 10: 
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    if html != '':
        #print response.info()
        soup = BeautifulSoup(html)
        token_val = ''
        var1_val = ''
        var2_val = ''
        var3_val = ''
        var4_name = ''
        var4_value = ''
        for div in soup.find_all('div',attrs={'class':'topbar-right'}):
            for span in div.find_all('span',attrs={'id':'welcome-info'}):
                for a in span.find_all('a',attrs={'class':'username'}):
                    print "username is : ",a.get_text()
        for div in soup.find_all('div',attrs={'class':'wrapper'}):
            for div2 in div.find_all('div',attrs={'class':'publish-detail'}):
                for div3 in div2.find_all('div',attrs={'class':'p-line','id':'id_contact'}):
                    for tele in div3.find_all('input',attrs={'name':'contact','class':'input input-5'}):
                        print "telephone number is : ",tele.get('value')                
        for div in soup.find_all('div',attrs={'id':'id_地区'}):
            for div2 in div.find_all('div',attrs={'class':'publish-detail-item '}):
                for input in div2.find_all('input'):
                    print "address is : ", input.get('value')
        ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address),)=get_car_info()
       
        for div in soup.find_all('div',attrs={'class':'publish-detail-item '}):
            for option in div.find_all('option'):
                if brand in str(option.get_text()):
                    brand_code = option.get('value')   
        for token in soup.find_all('input',attrs={'name':'token','class':'input','title':'[token]'}):
            token_val = token.get('value')
        for var1 in soup.find_all('input',attrs={'name':'7720e540a73e80522c4c1c54fa2b1dbf','type':'hidden'}):
            var1_val = var1.get('value')
        #for div in soup.find_all('div',attrs={'id':'d988531cc13d548e14c7021d122b4913e'}):
        #    print div
        for var2 in soup.find_all('input',attrs={'name':'577fdfff3de2d95a350f71d26e3c68d6'}):
            var2_val = var2.get('value')
        for var3 in soup.find_all('input',attrs={'name':'988531cc13d548e14c7021d122b4913e'}):
            var3_val = var3.get('value')
        y = 1

        var4_name = token_val[5:13]
        var4_value = token_val[7:15]


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
        print vehicle_model,brand_code,register_date_year,register_date_month,identity,token_val,volume,transmission,color,inspection_date_year,inspection_date_month,force_insurance_date_year,force_insurance_date_month,insurance_date_year,insurance_date_month,var1_val,var3_val,var4_name,var4_value
        car_infodata = {
            'pay':'',
            'wanted':0,
            'title':vehicle_model,
            '车品牌':brand_code,
            '车系列':'',
            '车型':'',
            '年份[0]':register_date_year,
            '年份[1]':register_date_month,
            '行驶里程':shown_miles,
            '价格':owner_price,
            'content':'',
            '地区[]':'m6010',
            '具体地点':u'南通市港闸区兴泰路3号(南通淘车无忧认证二手车精品展厅-交警三大队旁)'.encode('utf-8'),
            'QQ号':'',
            'contact':identity,
            'token':token_val,
            '排量':volume,
            '变速箱':transmission,
            '燃油类型':u'汽油'.encode('utf-8'),
            '排放标准':u'国四'.encode('utf-8'),
            '车辆颜色':color,
            '类型':'',
            '车辆用途':'',
            '年检[0]':inspection_date_year,
            '年检[1]':inspection_date_month,
            '交强险[0]':force_insurance_date_year,
            '交强险[1]':force_insurance_date_month,
            '商业险[0]':insurance_date_year,
            '商业险[1]':insurance_date_month,
            '承担过户费':'',
            '行驶证':'',
            '登记证':'',
            '购车发票':'',
            '维修记录':'',
            '购置税':'',
            '重大事故':'',
            '能否过户':'',
            '能否按揭':'',
            'video':'',
            '7720e540a73e80522c4c1c54fa2b1dbf':var1_val,
            '577fdfff3de2d95a350f71d26e3c68d6':'696f73d604f2919c1f78e0b7e6395049',
            '988531cc13d548e14c7021d122b4913e':var3_val,
            var4_name:var4_value,
        }
        return car_infodata
        


def post_cardata(url):
    ((brand,vehicle_series,volume,vehicle_model,vehicle_style,transmission,register_date,shown_miles,color,inspection_date,force_insurance_date,insurance_date,owner_price,address),)=get_car_info()
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
                browser.get(url)
            except:
                get_page_fails += 1
                print "get page info failed ... ",get_page_fails
            else:
                break
        browser.find_element_by_id('id_title').find_element_by_tag_name('input').send_keys('1')
        browser.find_element_by_id('id_行驶里程').find_element_by_tag_name('input').send_keys('2')
        browser.find_element_by_id('id_价格').find_element_by_tag_name('input').send_keys('3')
        #browser.find_elements_by_tag_name('input').find_element_by_name('价格').send_keys(owner_price)
        time.sleep(10)
        browser.find_element_by_id('fabu-form-submit').submit()
        time.sleep(10)
        print browser.find_element_by_tag_name('div').text
        #browser.quit()


def sendPostData(url, data, header):
    print "+"*20+"sendPostData"+"+"*20
    data = urllib.urlencode(data)      
    #print url
    print data
    #print header
    #cj = cookielib.CookieJar()
    #request = urllib2.Request(url,data,header)
	#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url,data,header)

    response = urllib2.urlopen(req)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        text = f.read()
    else:
        text = response.read()
    info = response.info()
    status = response.getcode()
    response.close()
    print "code = ",response.code
    print "status = ",status
    print "info ",info
    print response.geturl()
    soup = BeautifulSoup(text)

if __name__ == "__main__":   
    loginTobaixing()
