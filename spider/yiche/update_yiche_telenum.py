# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib
import urllib2
import re
import MySQLdb
import pytesseract
from PIL import Image
from cStringIO import StringIO
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup



def get_telephone(img_src):
    file1 = StringIO(urllib2.urlopen(img_src).read())
    img = Image.open(file1)
    vcode = pytesseract.image_to_string(img)
    return vcode


try:
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')   
    curs = conn.cursor()
    conn.select_db('spider')
    for i in xrange(20030,20105):
        curs.execute("select img_src from yiche_sell_car_info where id=%s" % i)
        get_img_src = curs.fetchone()
        if not get_img_src:
            pass
        else:
            if len(get_img_src[0])>10:
                tele_num =  get_telephone(get_img_src[0])
                print tele_num,' ',i
                curs.execute("update yiche_sell_car_info set telephone_num='%s' where id=%s" % (tele_num,i))

    conn.commit()
    curs.close()
    conn.close()
except MySQLdb.Error,e:
    print "Error %d %s" % (e.args[0],e.args[1])
    sys.exit(1)
