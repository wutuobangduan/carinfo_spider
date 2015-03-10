#!/usr/bin/env python
# -*- coding: utf_8 -*-
import pytesseract
from PIL import Image,ImageEnhance
from cStringIO import StringIO
import urllib2

image1 = Image.open('/data/python/spider/Identifying_code/PhoneCode1.png')
#enhancer1 = ImageEnhance.Contrast(image1)
#image_enhancer1 = enhancer1.enhance(4)
vcode1 = pytesseract.image_to_string(image1)
#print image_enhancer1.format,image_enhancer1.mode,image_enhancer1.size
print "PhoneCode1 : ",vcode1


image10 = Image.open('/data/python/spider/Identifying_code/PhoneCode2.png')
#enhancer1 = ImageEnhance.Contrast(image1)
#image_enhancer1 = enhancer1.enhance(4)
vcode10 = pytesseract.image_to_string(image10)
print "PhoneCode2 : ",vcode10

image11 = Image.open('/data/python/spider/Identifying_code/PhoneCode3.png')
#enhancer1 = ImageEnhance.Contrast(image1)
#image_enhancer1 = enhancer1.enhance(4)
vcode11 = pytesseract.image_to_string(image11)
print "PhoneCode3 : ",vcode11


image2 = Image.open('/data/python/spider/Identifying_code/showphone1.gif')
vcode2 = pytesseract.image_to_string(image2)
print "showphone1 : ",vcode2


image4 = Image.open('/data/python/spider/Identifying_code/showphone2.gif')
vcode4 = pytesseract.image_to_string(image4)
print "showphone2 : ",vcode4


image5 = Image.open('/data/python/spider/Identifying_code/showphone3.gif')
vcode5 = pytesseract.image_to_string(image5)
print "showphone3 : ",vcode5

image6 = Image.open('/data/python/spider/Identifying_code/showphone4.gif')
vcode6 = pytesseract.image_to_string(image6)
print "showphone4 : ",vcode6


image7 = Image.open('/data/python/spider/Identifying_code/RequestBuyObj.974.PhoneImg.png')
vcode7 = pytesseract.image_to_string(image7)
print "showphone4 : ",vcode7

