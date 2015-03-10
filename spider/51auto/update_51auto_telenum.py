# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib
import urllib2
import re
import MySQLdb

import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from StringIO import StringIO

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup



def numpoint(im):
    w,h = im.size
    data = list( im.getdata() )
    mumpoint=0
    for x in range(w):
        for y in range(h):
            if data[ y*w + x ] !=255:
                mumpoint+=1
    return mumpoint
                
def pointmidu(im):
    w,h = im.size
    p=[]
    for y in range(0,h,5):
        for x in range(0,w,5):
            box = (x,y, x+5,y+5)
            im1=im.crop(box)
            a=numpoint(im1)
            if a<11:
                for i in range(x,x+5):
                    for j in range(y,y+5):
                        im.putpixel((i,j), 255)
    im.save(r'img.jpg')
        
def ocrend(img_src):
    #image_name = "img.jpg"
    #im = Image.open(image_name)
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
    im = Image.open(file1)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    #im.save("1.tif")
    print pytesseract.image_to_string(im)    
ocrend("http://www.51auto.com/PhoneCode?s=0&info=018270cb74e1c5fa2d494397b23116da")
    
#if __name__=='__main__':
#    image_name = "1.png"
#    im = Image.open(image_name)
#    im = im.filter(ImageFilter.DETAIL)
#    im = im.filter(ImageFilter.MedianFilter())
#    
#    enhancer = ImageEnhance.Contrast(im)
##    im = enhancer.enhance(2)
#    im = im.convert('1')
#    ##a=remove_point(im)
#    pointmidu(im)
#    ocrend()


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
    img.filter(ImageFilter.SHARPEN)
    vcode = pytesseract.image_to_string(img)
    return vcode


#try:
    #conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')   
    #curs = conn.cursor()
    #conn.select_db('spider')
#    for i in xrange(1,1630):
#        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
#        curs = conn.cursor()
#        conn.select_db('spider')
#        curs.execute("select img_src from 51auto_qiugou_info where id=%s" % i)
#        get_img_src = curs.fetchone()
#        if not get_img_src:
#            pass
#        else:
##            if len(get_img_src[0])>10:
#                tele_num =  get_telephone(get_img_src[0])
#                print tele_num,' ',i
#                curs.execute("update 51auto_qiugou_info set telephone_num='%s' where id=%s" % (tele_num,i))
#
#        conn.commit()
#        curs.close()
#        conn.close()
#except MySQLdb.Error,e:
#    print "Error %d %s" % (e.args[0],e.args[1])
#    sys.exit(1)
