# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import socket


from PIL import Image


img = Image.open('showphone4.gif') # 读入图片
img = img.convert("RGBA")
pixdata = img.load()
print type(pixdata)
#二值化
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][0] < 90:
            pixdata[x,y] = (0, 0, 0, 255)
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][1] < 136:
            pixdata[x, y] = (0, 0, 0, 255)
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][2] > 0:
            pixdata[x, y] = (255, 255, 255, 255)
img.save("input-black.gif", "GIF")
#放大图像 方便识别
im_orig = Image.open('input-black.gif')
big = im_orig.resize((1000, 500), Image.NEAREST)
