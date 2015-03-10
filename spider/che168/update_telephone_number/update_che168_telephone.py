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
    img = img.convert("RGB")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
	    if pixdata[x, y][1] < 200:
	        pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)
    #for y in xrange(img.size[1]):
    #    for x in xrange(img.size[0]):
    #	    if pixdata[x, y][2] < 200:
    #            pixdata[x, y] = (0, 0, 0,255)
    #	        pixdata[x, y] = (255, 255, 255, 255)
    return img


#nume=0

def division(img):		#图像的分割，就是验证码按字符分割出来
    #global nume
    nume=0
    font=[]
    for i in range(11):
        
        #x = 9 + i*7 #这里的数字参数需要自己 
	y = 7 #根据验证码图片的像素进行
        if i==0:
            x = 7
            temp = img.crop((x,y,x+7,y+9))
        elif i == 1:
            x = 14
            temp = img.crop((x,y,x+8,y+9))
        elif i == 2:
            x = 22
            temp = img.crop((x,y,x+8,y+9))
        elif i == 3:
            x = 30
            temp = img.crop((x,y,x+8,y+9))
        elif i == 4:
            x = 38
            temp = img.crop((x,y,x+8,y+9))
        elif i == 5:
            x = 46
            temp = img.crop((x,y,x+8,y+9))
        elif i == 6:
            x = 54
            temp = img.crop((x,y,x+7,y+9))
        elif i == 7:
            x = 61
            temp = img.crop((x,y,x+7,y+9))
        elif i == 8:
            x = 68 
            temp = img.crop((x,y,x+7,y+9))
        elif i == 9:
            x = 75
            temp = img.crop((x,y,x+7,y+9))
        elif i == 10:
            x = 82
            temp = img.crop((x,y,x+7,y+9))
	#temp = img.crop((x, y, x+6,y+9))
	temp.save("/data/python/spider/che168/update_telephone_number/temp/%d.bmp" % nume)
	nume=nume+1
	font.append(temp)
    return font

def recognize(img):        #分隔出来的字符与预先定义的字体库中的结果逐个像素进行对比找出差别最小的项
    fontMods = []
    image_num = ['0','00','000','1','11','111','1111','2','22','222','3','33','333','3333','4','44','444','4444','5','55','555','6','66','666','7','77','777','8','88','888','8888','9','99','999','9999']
    for i in image_num:
        fontMods.append((str(i), Image.open("/data/python/spider/che168/update_telephone_number/fonts/%s.bmp" % i)))
    result=""
    font=division(img)
     
    for i in font:
        target=i
	points = []
	for mod in fontMods:
	    diffs = 0
	    for yi in range(9):
	        for xi in range(6):     #以下多行为自己修改，参考文章中的值对比存在问题
		    #print "mod[1].getpixel((xi,yi)):"+str(mod[1].getpixel((xi, yi)))
		    #print "target.getpixel((xi,yi)):"+str(target.getpixel((xi, yi)))
                    if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                        diffs += 1
            #print "diffs：" + str(diffs)
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
	#result += points[0][1]
    return result

if __name__ == '__main__':
    for i in xrange(1,1143):
        try:
            conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
            curs = conn.cursor()
            conn.select_db('spider')
            curs.execute("select img_src from che168_qiugou_info where id=%s" % i)
            get_img_src = curs.fetchone()
            if not get_img_src:
                pass
            else:
                if len(get_img_src[0])>10:
                    img=binary(get_img_src[0])
                    num = recognize(img)
                    print num,' ',i
                    curs.execute("update che168_qiugou_info set telephone_num=%s where id=%s" % (num,i))
            conn.commit()
            curs.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Error %d %s" % (e.args[0],e.args[1])
            sys.exit(1)


#if __name__ == '__main__':
#    codedir="/data/python/spider/che168/update_telephone_number/"
#    for imgfile in os.listdir(codedir):
#        if imgfile.endswith(".bmp"):
#	    dir="/data/python/spider/che168/update_telephone_number/"
#	    img=binary(codedir+imgfile)
#            #img = Image.open(codedir+imgfile)
#	    num=recognize(img)
#            print num
#	    #dir += (num+".bmp")
#	    #print "save to", dir
#	    #img.save(dir)

