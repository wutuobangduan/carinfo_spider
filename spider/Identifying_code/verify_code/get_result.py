#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from PIL import Image,ImageFilter,ImageEnhance
import urllib
import urllib2
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import socket

def binary(f):
    print f
    img = Image.open(f)
    #x_end=img.size[0]
    #temp = img.crop((2,15,x_end-13,28))
    #print temp.size,temp.format
    print img.info,img.size,img.format
    img = img.convert("RGBA")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            #print pixdata[x, y]
	    if pixdata[x, y][1] < 220:
	        pixdata[x, y] = (0, 0, 0,255)
            else:
                pixdata[x, y] = (255, 255, 255,255)
    #for y in xrange(img.size[1]):
    #    for x in xrange(img.size[0]):
    #	    if pixdata[x, y][2] < 200:
    #            pixdata[x, y] = (0, 0, 0,255)
    #	        pixdata[x, y] = (255, 255, 255, 255)
    return img


nume=0

def division(img):		#图像的分割，就是验证码按字符分割出来
    global nume
    #nume=0
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
            #for j in range(8,24):
            #    if 
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
	temp.save("/data/python/spider/Identifying_code/verify_code/temp/%d.png" % nume)
	nume=nume+1
	font.append(temp)
    return font

def recognize(img):        #分隔出来的字符与预先定义的字体库中的结果逐个像素进行对比找出差别最小的项
    fontMods = []
    for i in range(10):
        fontMods.append((str(i), Image.open("/data/python/spider/Identifying_code/verify_code/fonts/%d.png" % i)))
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
        #if "0" in points[0][1]:
        #    result += "0"
        #elif "1" in points[0][1]:
        #    result += "1"
        #elif "2" in points[0][1]:
        #    result += "2"
        ##elif "3" in points[0][1]:
        #    result += "3"
        #elif "4" in points[0][1]:
        #    result += "4"
        #elif "5" in points[0][1]:
        #    result += "5"
        #elif "6" in points[0][1]:
        #    result += "6"
        #elif "7" in points[0][1]:
        #    result += "7"
        #elif "8" in points[0][1]:
        ##    result += "8"
        #elif "9" in points[0][1]:
        #    result += "9"
	result += points[0][1]
    return result

if __name__ == '__main__':
    codedir="/data/python/spider/Identifying_code/verify_code/pic/"
    num = 0
    for imgfile in os.listdir(codedir):
        if imgfile.endswith(".gif"):
	    dir="/data/python/spider/Identifying_code/verify_code/result/"
	    img=binary(codedir+imgfile)
	    #num=recognize(img)
            #print num
	    dir += (str(num)+".png")
	    print "save to", dir
	    img.save(dir)
            num += 1

