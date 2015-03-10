# -*- coding: utf-8 -*-
#!/usr/bin/env python
import simplejson as json
import os
import urllib
import urllib2
import chardet
import re
import MySQLdb
from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

json_data = u'{"returncode":0,"message":null,"result":{"seriesid":2730,"paramtypeitems":[{"name":"基本参数","paramitems":[{"name":"车型名称","valueitems":[{"specid":15427,"value":"奥迪S3 2015款 S3 2.0T Limousine"}]},{"name":"厂商指导价(元)","valueitems":[{"specid":15427,"value":"39.98万"}]},{"name":"厂商","valueitems":[{"specid":15427,"value":"奥迪(进口)"}]},{"name":"级别","valueitems":[{"specid":15427,"value":"紧凑型车"}]},{"name":"发动机","valueitems":[{"specid":15427,"value":"2.0T 286马力 L4"}]},{"name":"变速箱","valueitems":[{"specid":15427,"value":"6挡双离合"}]},{"name":"长*宽*高(mm)","valueitems":[{"specid":15427,"value":"4472*1796*1392"}]},{"name":"车身结构","valueitems":[{"specid":15427,"value":"4门5座三厢车"}]},{"name":"最高车速(km/h)","valueitems":[{"specid":15427,"value":"250"}]},{"name":"官方0-100km/h加速(s)","valueitems":[{"specid":15427,"value":"4.9"}]},{"name":"实测0-100km/h加速(s)","valueitems":[{"specid":15427,"value":"4.87"}]},{"name":"实测100-0km/h制动(m)","valueitems":[{"specid":15427,"value":"38.08"}]},{"name":"实测油耗(L/100km)","valueitems":[{"specid":15427,"value":"9.3"}]},{"name":"工信部综合油耗(L/100km)","valueitems":[{"specid":15427,"value":"-"}]},{"name":"实测离地间隙(mm)","valueitems":[{"specid":15427,"value":"-"}]},{"name":"整车质保","valueitems":[{"specid":15427,"value":"三年或10万公里"}]}]},{"name":"车身","paramitems":[{"name":"长度(mm)","valueitems":[{"specid":15427,"value":"4472"}]},{"name":"宽度(mm)","valueitems":[{"specid":15427,"value":"1796"}]},{"name":"高度(mm)","valueitems":[{"specid":15427,"value":"1392"}]},{"name":"轴距(mm)","valueitems":[{"specid":15427,"value":"2628"}]},{"name":"前轮距(mm)","valueitems":[{"specid":15427,"value":"1551"}]},{"name":"后轮距(mm)","valueitems":[{"specid":15427,"value":"1526"}]},{"name":"最小离地间隙(mm)","valueitems":[{"specid":15427,"value":"-"}]},{"name":"整备质量(kg)","valueitems":[{"specid":15427,"value":"1505"}]},{"name":"车身结构","valueitems":[{"specid":15427,"value":"三厢车"}]},{"name":"车门数(个)","valueitems":[{"specid":15427,"value":"4"}]},{"name":"座位数(个)","valueitems":[{"specid":15427,"value":"5"}]},{"name":"油箱容积(L)","valueitems":[{"specid":15427,"value":"55"}]},{"name":"行李厢容积(L)","valueitems":[{"specid":15427,"value":"390"}]}]},{"name":"发动机","paramitems":[{"name":"发动机型号","valueitems":[{"specid":15427,"value":"EA888"}]},{"name":"排量(mL)","valueitems":[{"specid":15427,"value":"1984"}]},{"name":"排量(L)","valueitems":[{"specid":15427,"value":"2.0"}]},{"name":"进气形式","valueitems":[{"specid":15427,"value":"涡轮增压"}]},{"name":"气缸排列形式","valueitems":[{"specid":15427,"value":"L"}]},{"name":"气缸数(个)","valueitems":[{"specid":15427,"value":"4"}]},{"name":"每缸气门数(个)","valueitems":[{"specid":15427,"value":"4"}]},{"name":"压缩比","valueitems":[{"specid":15427,"value":"-"}]},{"name":"配气机构","valueitems":[{"specid":15427,"value":"DOHC"}]},{"name":"缸径(mm)","valueitems":[{"specid":15427,"value":"-"}]},{"name":"行程(mm)","valueitems":[{"specid":15427,"value":"-"}]},{"name":"最大马力(Ps)","valueitems":[{"specid":15427,"value":"286"}]},{"name":"最大功率(kW)","valueitems":[{"specid":15427,"value":"210"}]},{"name":"最大功率转速(rpm)","valueitems":[{"specid":15427,"value":"5100-6500"}]},{"name":"最大扭矩(N·m)","valueitems":[{"specid":15427,"value":"380"}]},{"name":"最大扭矩转速(rpm)","valueitems":[{"specid":15427,"value":"1800-5100"}]},{"name":"发动机特有技术","valueitems":[{"specid":15427,"value":"-"}]},{"name":"燃料形式","valueitems":[{"specid":15427,"value":"汽油"}]},{"name":"燃油标号","valueitems":[{"specid":15427,"value":"97号(京95号)"}]},{"name":"供油方式","valueitems":[{"specid":15427,"value":"直喷"}]},{"name":"缸盖材料","valueitems":[{"specid":15427,"value":"铝"}]},{"name":"缸体材料","valueitems":[{"specid":15427,"value":"铝"}]},{"name":"环保标准","valueitems":[{"specid":15427,"value":"欧V"}]}]},{"name":"变速箱","paramitems":[{"name":"简称","valueitems":[{"specid":15427,"value":"6挡双离合"}]},{"name":"挡位个数","valueitems":[{"specid":15427,"value":"6"}]},{"name":"变速箱类型","valueitems":[{"specid":15427,"value":"双离合变速箱(DCT)"}]}]},{"name":"底盘转向","paramitems":[{"name":"驱动方式","valueitems":[{"specid":15427,"value":"前置四驱"}]},{"name":"四驱形式","valueitems":[{"specid":15427,"value":"全时四驱"}]},{"name":"中央差速器结构","valueitems":[{"specid":15427,"value":"多片离合器"}]},{"name":"前悬架类型","valueitems":[{"specid":15427,"value":"麦弗逊式独立悬架"}]},{"name":"后悬架类型","valueitems":[{"specid":15427,"value":"多连杆独立悬架"}]},{"name":"助力类型","valueitems":[{"specid":15427,"value":"电动助力"}]},{"name":"车体结构","valueitems":[{"specid":15427,"value":"承载式"}]}]},{"name":"车轮制动","paramitems":[{"name":"前制动器类型","valueitems":[{"specid":15427,"value":"通风盘式"}]},{"name":"后制动器类型","valueitems":[{"specid":15427,"value":"通风盘式"}]},{"name":"驻车制动类型","valueitems":[{"specid":15427,"value":"电子驻车"}]},{"name":"前轮胎规格","valueitems":[{"specid":15427,"value":"225/40 R18"}]},{"name":"后轮胎规格","valueitems":[{"specid":15427,"value":"225/40 R18"}]},{"name":"备胎规格","valueitems":[{"specid":15427,"value":"非全尺寸"}]}]}]}}'.encode('utf-8')

print type(json_data)
json_object = json.loads(json_data)
print json_object
print type(json_object)


python_object = json.dumps(json_data)
print python_object
print type(python_object)




