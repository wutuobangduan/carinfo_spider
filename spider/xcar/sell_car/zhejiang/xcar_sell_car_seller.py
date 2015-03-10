# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import threading
import time
import socket
#socket.setdefaulttimeout(30)
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO

def binary(img_src):
    print img_src
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
    #print img.info,img.size,img.format
    img = img.convert("RGBA")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            #print pixdata[x, y]
            if pixdata[x, y][3] >50:
                pixdata[x, y] = (0, 0, 0,255)
            else:
                pixdata[x, y] = (255, 255, 255,255)
    return img



def division(img):              #图像的分割，就是验证码按字符分割出来
    #global nume
    nume=0
    font=[]
    for i in range(11):
        
        #x = 9 + i*7 #这里的数字参数需要自己 
        y = 15 #根据验证码图片的像素进行
        if i==0:
            x = 1
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13)) 
                a1 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a1 = 9

        elif i == 1:
            x += a1 
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a2 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a2 = 9
        elif i == 2:
            x += a2
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a3 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a3 = 9
        elif i == 3:
            x += a3
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a4 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a4 = 9
        elif i == 4:
            x += a4
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a5 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a5 = 9
        elif i == 5:
            x += a5
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a6 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a6 = 9
        elif i == 6:
            x += a6
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a7 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a7 = 9
        elif i == 7:
            x += a7
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a8 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a8 = 9
        elif i == 8:
            x += a8 
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a9 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a9 = 9
        elif i == 9:
            x += a9
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a10 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a10 = 9
        elif i == 10:
            x += a10
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
            else:
                temp = img.crop((x,y,x+9,y+13))
        temp.save("/data/python/spider/xcar/update_telephone_number/temp/%d.png" % nume)
        nume=nume+1
        font.append(temp)
    return font

def recognize(img):        #分隔出来的字符与预先定义的字体库中的结果逐个像素进行对比找出差别最小的项
    fontMods = []
    for i in range(10):
        fontMods.append((str(i), Image.open("/data/python/spider/xcar/update_telephone_number/fonts/%d.png" % i)))
    result=""
    font=division(img)
     
    for i in font:
        target=i
        points = []
        for mod in fontMods:
            diffs = 0
            for yi in range(13):
                for xi in range(9):     #以下多行为自己修改，参考文章中的值对比存在问题
                    #print "mod[1].getpixel((xi,yi)):"+str(mod[1].getpixel((xi, yi)))
                    #print "target.getpixel((xi,yi)):"+str(target.getpixel((xi, yi)))
                    if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                        diffs += 1
            #print "diffs：" + str(diffs)
            points.append((diffs, mod[0]))
        points.sort()
        result += points[0][1]
    return result



def grabHref(url,localfile):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    html = None
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
    if html is not None:
        #dictionary = {}
        href = None
        for div in  BeautifulSoup(html).find_all('div',attrs={'class':'f_l list_02'}):
            for h2 in div.find_all('h2',attrs={'style':'white-space:nowrap'}):
                for a in h2.find_all('a'):
                    href = a.get('href')
                    if href: 
                        #and href not in dictionary:
                        #dictionary[href] = ''
                        ans = 'http://used.xcar.com.cn' + href
                         
                        print "====================================================================================================================================="
                        print ans
                        get_qiugou_info(ans)
                        print "====================================================================================================================================="

def get_qiugou_info(myUrl):
    #proxy = {'http':'http://202.106.16.36:3128'}
    #proxy_support = urllib2.ProxyHandler(proxy)
    #opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    #urllib2.install_opener(opener)  
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
        soup = BeautifulSoup(html)
        title = ''
        prices = ''
        new_car_prices = ''
        addrs = ''
        name = ''
        vehicle_info = ''
        release_time = ''
        telephone = ''
        trip_distance = ''
        licenses = ''
        is_seller = ''
        owner_readme = ''
        displacement = ''
        transmissions = ''
        vehicle_color = ''
        img_src = ''
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        j = 1
        for div in soup.find_all('div',attrs={'class':'specifics_l f_l'}):
            for div2 in div.find_all('div',attrs={'class':'specifics_title'}):
                for h1 in div2.find_all('h1'):
                    title = str(h1.get_text())
                for span in div2.find_all('span',attrs={'class':'time'}):
                    if len(str(span.get_text()).split('：'))>1:
                        release_time = str(span.get_text()).split('：')[1]
            for div3 in div.find_all('div',attrs={'class':'info_right f_r'}):
                for div4 in div3.find_all('div',attrs={'class':'info_cost'}):
                    #print str(div4.get_text()).split('：')
                    if len(str(div4.get_text()).split('：'))>1 and len(str(div4.get_text()).split('：')[1].split('\n'))>0:
                        prices = str(div4.get_text()).split('：')[1].split('\n')[0]
                        new_car_prices = str(div4.get_text()).split('：')[-1]
                for ul in div3.find_all('ul',attrs={'class':'datum_ul'}):
                    for li in ul.find_all('li'):
                        if j == 1:
                            if len(str(li.get_text()).split('：'))>1:
                                licenses = str(li.get_text()).split('：')[1]   
                        elif j == 2:
                            if len(str(li.get_text()).split('：'))>1:
                                displacement = str(li.get_text()).split('：')[1] 
                        elif j == 3:
                            if len(str(li.get_text()).split('：'))>1:
                                trip_distance = str(li.get_text()).split('：')[1]
                        elif j == 4:
                            if len(str(li.get_text()).split('：'))>1:
                                transmissions = str(li.get_text()).split('：')[1]
                        elif j == 5:
                            if len(str(li.get_text()).split('：'))>1:
                                vehicle_color = str(li.get_text()).split('：')[1]
                        elif j == 6:
                            if len(str(li.get_text()).split('：'))>1:
                                environmental_protection_standard = str(li.get_text()).split('：')[1]     
                        j += 1
                for div5 in div3.find_all('div',attrs={'class':'details_one'}):
                    for img in div5.find_all('img'):    
                        img_src = 'http://used.xcar.com.cn' + img.get('src')
                    for span in div5.find_all('span',attrs={'class':'name'}):
                        name = str(span.get_text())
        k = 1
        for div in soup.find_all('div',attrs={'class':'details_list clearfix mt12'}):
            for td in div.find_all('td',attrs={'class':'td_128'}):
                if k == 1:
                    addrs = str(td.get_text())
                k += 1
        s = 1
        for div in soup.find_all('div',attrs={'class':'details_list2 clearfix mt12'}):
            if s == 1:
                for p in div.find_all('p'):
                    owner_readme = str(p.get_text())
            s += 1
        #print title,release_time,prices,new_car_prices
        #print licenses,displacement,trip_distance,transmissions,vehicle_color,environmental_protection_standard
        print img_src,name,addrs,owner_readme
        telephone_num = ''
        if img_src != '':
            img=binary(img_src)
            telephone_num = recognize(img)
            print telephone_num
        if img_src != '':
            print title,name,addrs,release_time,prices,new_car_prices,licenses,displacement,trip_distance,transmissions,vehicle_color,environmental_protection_standard,img_src,owner_readme,myUrl
            is_seller = u'商家'.encode('utf-8')
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    car_config = trip_distance + " | " + licenses + " | " + displacement + " | " + transmissions + " | " + vehicle_color + " | " + environmental_protection_standard
                    info_src = "xcar"
                    res = [title,car_config,img_src,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,img_src,name,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/personal/1743881.htm')

#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/personal/1760248.htm')

#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/shop/1464939.htm')


#print "=================================================================================="

#get_qiugou_info('http://used.xcar.com.cn/shop/1650309.htm')



def main():
    url = "http://used.xcar.com.cn/search/26-0-0-0-0-0-0-0-0-0-0-0-0-0-0-2-0?page="
    localfile="Href.txt"
    for i in xrange(1,5):
    #for i in range(1,5):
        myUrl = url + str(i)
        print "current page is %d " % i
        t = threading.Thread(target=grabHref(myUrl,localfile))
        t.start()
        print "current page is %d " % i

if __name__=="__main__":
    main()
