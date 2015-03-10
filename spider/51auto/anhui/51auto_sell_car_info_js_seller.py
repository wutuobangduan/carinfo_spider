# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import socket 
socket.setdefaulttimeout(30) 
import threading
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException

from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO
import pytesseract

def grabHref(url,localfile):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
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
    content = BeautifulSoup(html).find_all('a')
    pat = re.compile(r'http://www.51auto.com/buycar/\d+.html')
    dictionary = {}
    for item in content:
        href = pat.findall(str(item))
        if href:
            #if href[0] not in dictionary:
                #dictionary[href[0]] = ''
                print href[0]
                th = threading.Thread(get_qiugou_info(href[0]))
                th.start()

def get_telephone(img_src):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(img_src,headers=heads)
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
    file1 = StringIO(html)
    img = Image.open(file1)
    vcode = pytesseract.image_to_string(img)
    return vcode


def get_qiugou_info(myUrl):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
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
        soup = BeautifulSoup(html)
        title = ''
        for h in soup.find_all('h1'):
            for b in h.find_all('b'):
                title = str(b.get_text())
        prices = ''
        vehicle_colors = ''
        addrs = u'安徽'.encode('utf-8')
        name = ''
        img_src = ''
        release_time = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        licenses = ''
        effluent_standard = ''
        owner_readme = ''
        contact = u'人'.encode('utf-8')
        addr = u'看车地点'.encode('utf-8')
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = None
        #try:
        #    browser = webdriver.PhantomJS(executable_path='/data/python/phantomjs-1.9.8-linux-x86_64/bin/phantomjs') 
        #except WebDriverException,e:
        #    print e
        #if browser is not None:
        #    browser.get(myUrl)
        #    release_content = None
        #    try:
        #        release_content = browser.find_element_by_id('car_publish_time')
        #    except NoSuchElementException,e:
        #        print e
        #    if release_content is not None:
        #        if len(str(release_content.text).split('：'))>1:
        #            RG = re.compile(r'\d+-\d+-\d+')
        #            if len(RG.findall(str(release_content.text).split('：')[1]))>0:
        #                release_time = RG.findall(str(release_content.text).split('：')[1])[0]
        


        req = Request(myUrl)
        response = urlopen(req)
        if response.info().getheader("ETag") is not None:
            id = response.info().getheader("ETag").split('/')[1][1:-1]
            number = myUrl.split('/')[-1].split('.')[0]
            test_data = {'callCount':1,'c0-scriptName':'CarViewAJAX','c0-methodName':'getCarInfoNew','xml':'true'}

            test_data['c0-id']=str(id)
            test_data['c0-param0']='number:' + str(number)

            test_data_urlencode = urllib.urlencode(test_data)
            requrl = "http://www.51auto.com/dwr/exec/CarViewAJAX.getCarInfoNew"

            req = urllib2.Request(url = requrl,data =test_data_urlencode)

            res_data = urllib2.urlopen(req)
            res = res_data.read()
            Regex = re.compile(r'\d+-\d+-\d+')
            if len(Regex.findall(res))>0:
                release_time = Regex.findall(res)[0]
        
        i = 1
        for dl in soup.find_all("dl",attrs={'class':'or_dl'}):
            for dt in dl.find_all("dt"):
                if len(str(dt.get_text()).split('：'))>=2:
                    prices = str(dt.get_text()).split('：')[1].split('\n')[0]
            for dd in dl.find_all("dd"):
                for p in dd.find_all("p"):
                    if len(str(p.get_text()).split('：'))>1:
                        if i == 1:
                            licenses = str(p.get_text()).split('：')[1]
                        elif i == 2:
                            trip_distances = str(p.get_text()).split('：')[1]
                        elif i == 3:
                            displacements = str(p.get_text()).split('：')[1]
                        elif i == 4:
                            transmissions = str(p.get_text()).split('：')[1]
                        elif i == 5:
                            vehicle_colors = str(p.get_text()).split('：')[1]
                        elif i == 6:
                            effluent_standard = str(p.get_text()).split('：')[1]
                    i += 1
        for div in soup.find_all("div",attrs={'class':'ophone_height'}):
            for img in div.find_all('img'):
                img_src = img.get('src')
        for p in soup.find_all("p",attrs={'class':'lookcar'}):
            for i in p.find_all('i'):
                for span in p.find_all('span'):
                    if contact in str(span.get_text()):
                        name = str(i.get_text())           
                
                    if addr in str(span.get_text()):
                        if u'安徽'.encode('utf-8') in str(i.get_text()):
                            addrs = str(i.get_text())
                        else:
                            addrs += str(i.get_text())
        for dl in soup.find_all("dl",attrs={'class':'sm_dl'}):
            for dt in dl.find_all("dt"):
                for a in dt.find_all("a"):
                    name = str(a.get_text())
            for dd in dl.find_all("dd"):
                if contact in str(dd.get_text()):
                    if len(str(dd.get_text()).split('：'))>1:
                        name += ': '+str(dd.get_text()).split('：')[1]  
        for p in soup.find_all("p",attrs={'class':'o_pmain'}):
            owner_readme = str(p.get_text())
        #print title,name,addrs,release_time,prices,licenses,trip_distances,displacements,transmissions,vehicle_colors,effluent_standard,img_src,owner_readme
        telephone_num = ''
        if img_src != '':
            telephone_num = get_telephone(img_src)
            print title,name,addrs,release_time,prices,licenses,trip_distances,displacements,transmissions,vehicle_colors,effluent_standard,img_src,owner_readme,myUrl
            is_seller = u'商家'.encode('utf-8')
            #res = [title,name,addrs,release_time,prices,licenses,trip_distances,displacements,transmissions,vehicle_colors,effluent_standard,img_src,owner_readme,myUrl]
            uni_number = str(myUrl.split('/')[-1]).split('.')[0]
            #urllib.urlretrieve(img_src,'/data/python/spider/51auto/telephone_img_sell_car/%s.jpg' % uni_number)
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    car_config = trip_distances + " | " + licenses + " | " + displacements + " | " + transmissions + " | " + vehicle_colors + " | " + effluent_standard
                    info_src = "51auto"
                    res = [title,car_config,img_src,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,img_src,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database,begin to update the data...'
                    curs.execute("update sell_car_info set release_time='%s',name='%s' where url='%s'" % (release_time,name,myUrl))
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)


#print "=================================================================================="
#get_qiugou_info('http://www.51auto.com/buycar/2489927.html')

#print "=================================================================================="



#print "=================================================================================="

#get_qiugou_info('http://www.51auto.com/buycar/2488833.html')

#print "=================================================================================="

#get_qiugou_info('http://www.51auto.com/buycar/2479037.html')


def main():
    url="http://www.51auto.com/anhui/pabmdcig3f/?page="
    localfile="Href.txt"
    for i in range(1,8):
        print "current page is %d" % i
        myUrl = url + str(i)
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d" % i

if __name__=="__main__":
    main()
