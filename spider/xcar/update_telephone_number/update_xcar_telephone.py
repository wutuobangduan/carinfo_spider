#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO
import urllib
import urllib2
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import socket

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



def division(img):		#图像的分割，就是验证码按字符分割出来
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

if __name__ == '__main__':
    for i in xrange(30480,40000):
        try:
            conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
            curs = conn.cursor()
            conn.select_db('spider')
            curs.execute("select img_src from xcar_sell_car_info where id=%s" % i)
            get_img_src = curs.fetchone()
            if not get_img_src:
                pass
            else:
                if len(get_img_src[0])>10:
                    img=binary(get_img_src[0])
                    num = recognize(img)
                    print num,' ',i
                    curs.execute("update xcar_sell_car_info set telephone_num=%s where id=%s" % (num,i))
            conn.commit()
            curs.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Error %d %s" % (e.args[0],e.args[1])
            sys.exit(1)

