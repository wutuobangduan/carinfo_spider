#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from PIL import Image,ImageFilter,ImageEnhance
import urllib
import urllib2
import re
import MySQLdb
from StringIO import StringIO
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
    print img.format,img.size
    img = img.convert("RGBA")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
	    if pixdata[x, y][1] < 211 or pixdata[x, y][2] < 200:
	        pixdata[x, y] = (0, 0, 0, 255)
            else:
                pixdata[x, y] = (255, 255, 255, 255)
    return img


print binary("http://image.58.com/showphone.aspx?t=v55&v=A78ED7D414575ADDL417AD512A63C55C6")        


def division(img):		#图像的分割，就是验证码按字符分割出来
    #global nume
    nume = 0
    font=[]
    for i in range(11):
        x = 1 + i*8 #这里的数字参数需要自己 
	y = 10 #根据验证码图片的像素进行
	temp = img.crop((x, y, x+6,y+10))
	temp.save("./temp/%d.png" % nume)
	nume=nume+1
	font.append(temp)
    return font

def recognize(img):        #分隔出来的字符与预先定义的字体库中的结果逐个像素进行对比找出差别最小的项
    fontMods = []
    for i in range(10):
        fontMods.append((str(i), Image.open("./fonts/%d.png" % i)))
    result=""
    font=division(img)
    #for i in range(11):
    #    target = Image.open("./temp/%d.png" % i)
     
    for i in font:
        target=i
	points = []
	for mod in fontMods:
	    diffs = 0
	    for yi in range(10):
	        for xi in range(6):     #以下多行为自己修改，参考文章中的值对比存在问题
		    #print "mod[1].getpixel((xi,yi)):"+str(mod[1].getpixel((xi, yi)))
		    #print "target.getpixel((xi,yi)):"+str(target.getpixel((xi, yi)))
		    #if 0 in target.getpixel((xi, yi)):
		    #    compare = 0
		    #else:
		    #    compare = 255
		    #if mod[1].getpixel((xi, yi)) != compare:
		    #    diffs += 1
                    if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                        diffs += 1
            print "diffs：" + str(diffs)
	    points.append((diffs, mod[0]))
        points.sort()
	result += points[0][1]
    return result

#if __name__ == '__main__':
#    for i in xrange(1,1640):
#        try:
#            conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
#            curs = conn.cursor()
#            conn.select_db('spider')
#            curs.execute("select img_src from 51auto_qiugou_info where id=%s" % i)
##            get_img_src = curs.fetchone()
#            if not get_img_src:
#                pass
#            else:
#                if len(get_img_src[0])>10:
#                    img=binary(get_img_src[0])
#                    num = recognize(img)
###                    print num,' ',i
#                    curs.execute("update 51auto_qiugou_info set telephone_num=%s where id=%s" % (num,i))
#            conn.commit()
#            curs.close()
#            conn.close()
#        except MySQLdb.Error,e:
#            print "Error %d %s" % (e.args[0],e.args[1])
#            sys.exit(1)

                       
