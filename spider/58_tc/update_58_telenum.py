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
from StringIO import StringIO

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup



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
    #img.filter(ImageFilter.SHARPEN)
    vcode = pytesseract.image_to_string(img)
    return vcode


try:
    #conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')   
    #curs = conn.cursor()
    #conn.select_db('spider')
    for i in xrange(1,11041):
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
        curs = conn.cursor()
        conn.select_db('spider')
        curs.execute("select img_src from 58_qiugou_info where id=%s" % i)
        get_img_src = curs.fetchone()
        if not get_img_src:
            pass
        else:
            if len(get_img_src[0])>10:
                tele_num =  get_telephone(get_img_src[0])
                print tele_num,' ',i
                curs.execute("update 58_qiugou_info set telephone_num='%s' where id=%s" % (tele_num,i))

        conn.commit()
        curs.close()
        conn.close()
except MySQLdb.Error,e:
    print "Error %d %s" % (e.args[0],e.args[1])
    sys.exit(1)
