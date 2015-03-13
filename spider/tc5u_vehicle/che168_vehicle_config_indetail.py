# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import chardet
import re
#import ast
import MySQLdb
#import socket 
#socket.setdefaulttimeout(120) 
import threading
#from pyvirtualdisplay import Display
#from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException,WebDriverException,TimeoutException

from urllib2 import Request,urlopen,URLError,HTTPError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import simplejson as json

        
def get_config_indetail(url):
    proxy = {'http':'http://202.106.16.36:3128'}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    html = ''
    fails = 0
    while True:
        try:
            if fails>=18:
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing stopsale,the network may be not Ok,please wait...",fails
        else:
            break
    if html != '':
        j = 1
        config_in_details = ['' for j in range(3)]
        if chardet.detect(html)['encoding'] == 'GB2312':
            soup = BeautifulSoup(html.decode('gbk').encode('utf-8'))
        else:
            get_config_indetail(url)
        config_in_details[0] = get_config(html)
        config_in_details[1] = get_option(html)
        config_in_details[2] = get_color(html)
        if config_in_details[0] == '' or config_in_details[1] == '':
            print "There is no config information..."
            return '[]'
        config = config_in_details[0].decode('gbk').encode('utf-8').rstrip(';')
        option = config_in_details[1].decode('gbk').encode('utf-8').rstrip(';')
        color = config_in_details[2].decode('gbk').encode('utf-8').rstrip(';')
        #print chardet.detect(config)
        #print config
        #config_dict = ast.parse(config,mode="eval")
        #print config_dict.body
        #config_dict = ast.literal_eval(config)
        #print config_str
        #print type(config_str)
        
        config_json = json.loads(config)
        option_json = json.loads(option)
        color_json = json.loads(color)
        #print config_json
        #print type(config_json),type(option_json),type(color_json)
        config_result = {}
        attr_value = []
        attr_value_dict ={}
        for i in range(len(config_json['result']['paramtypeitems'])):
            for m in range(len(config_json['result']['paramtypeitems'][i]['paramitems'])):
                attr_value_dict["name"] = config_json['result']['paramtypeitems'][i]['paramitems'][m]['name']
                attr_value_dict["vid"] = 0
                attr_value_dict["vname"] = config_json['result']['paramtypeitems'][i]['paramitems'][m]['valueitems'][0]['value']
                
                #print json.dumps(attr_value_dict,encoding="UTF-8", ensure_ascii=False)
                #attr_value_dict_sort = sort_dispaly_dict(json.dumps(attr_value_dict,encoding="UTF-8", ensure_ascii=False))
                #print json.dumps(attr_value_dict_sort,encoding="UTF-8", ensure_ascii=False)
                #print attr_value_dict_sort
                #print config_json['result']['paramtypeitems'][i]['paramitems'][m]['name'],config_json['result']['paramtypeitems'][i]['paramitems'][m]['valueitems'][0]['value']
                
                #attr_value.append(json.dumps(attr_value_dict, encoding="UTF-8", ensure_ascii=False))
                attr_value.append(attr_value_dict)
                attr_value_dict ={}
                #print zhprint(attr_value)
                #print json.dumps(attr_value, encoding="UTF-8", ensure_ascii=False)
        #print zhprint(attr_value)
        for i in range(len(option_json['result']['configtypeitems'])):
            for m in range(len(option_json['result']['configtypeitems'][i]['configitems'])):
                attr_value_dict["name"] = option_json['result']['configtypeitems'][i]['configitems'][m]['name']
                attr_value_dict["vid"] = 0
                attr_value_dict["vname"] = option_json['result']['configtypeitems'][i]['configitems'][m]['valueitems'][0]['value']
                #attr_value_dict_sort = sort_dispaly_dict(attr_value_dict)

                #print option_json['result']['configtypeitems'][i]['configitems'][m]['name'],option_json['result']['configtypeitems'][i]['configitems'][m]['valueitems'][0]['value']
                #attr_value.append(json.dumps(attr_value_dict, encoding="UTF-8", ensure_ascii=False))
                
                attr_value.append(attr_value_dict)
                #print zhprint(attr_value)
                attr_value_dict ={}
        #print attr_value
        #print zhprint(attr_value).replace(" u'","  '")
         
        #config_result["attr"] = json.dumps(attr_value,encoding="UTF-8", ensure_ascii=False)
      
        config_result["attr"] = zhprint(attr_value).replace(" u'"," '")
        #print zhprint(config_result).replace('"','').replace('u[','[')
        color_result = []
        if len(color_json['result']['specitems'])>0:
            for m in range(len(color_json['result']['specitems'][0]['coloritems'])):
                #print type(color_json['result']['specitems'][0]['coloritems'])
                #color_result.append(json.dumps(color_json['result']['specitems'][0]['coloritems'][m],encoding="UTF-8", ensure_ascii=False))
                color_result.append(color_json['result']['specitems'][0]['coloritems'][m])
        #config_result["color"] = json.dumps(color_result,encoding="UTF-8", ensure_ascii=False)
        config_result["color"] = zhprint(color_result).replace(" u'"," '")
        #print zhprint(config_result).replace('"','').replace('u[','[')
        config_detail = [zhprint(config_result).replace('"','').replace('u[','[')]
        #print json.dumps(config_detail,encoding="UTF-8", ensure_ascii=False).replace('\\','')
        #return json.dumps(config_detail,encoding="UTF-8", ensure_ascii=False).replace('\\','')
        #print zhprint(config_detail).replace('u"','').replace('"','')
        return zhprint(config_detail).replace('u"','').replace('"','').replace("'",'"')


def zhprint(obj):
    return re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())




def update_vehicle_model():
    try:
        #conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
        #curs = conn.cursor()
        #conn.select_db('tc_platform')
        for i in xrange(6055,14003):
            conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
            curs = conn.cursor()
            conn.select_db('tc_platform')
            curs.execute("select che168_model_id from tc_vehicle_model_tmp where vehicle_model_id=%s" % i)
            get_che168_model_id = curs.fetchone()
            if not get_che168_model_id:
                pass
            else:
                url = "http://car.autohome.com.cn/config/spec/" + str(get_che168_model_id[0]) + ".html"
            print url
            config_detail = get_config_indetail(url)
            print config_detail
            #print config_detail_json
            curs.execute("update tc_vehicle_model_tmp set spec_value = %s where vehicle_model_id=%s",(config_detail.encode('utf-8'),i))
            conn.commit()
            curs.close()
            conn.close()
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)



def sort_dispaly_dict(dictionary):
    return "{" + ", ".join("%r: %r" % (key, dictionary[key]) for key in sorted(dictionary)) + "}"


def get_config(html):
    req=r'var config = ({.*};)'
    trs = re.compile(req)
    trslist = re.findall(trs,html)
    if len(trslist)==0:
        return ''
    else:
        Str=str(trslist[0])
        return Str


def get_option(html):
    req=r'var option = ({.*};)'
    trs = re.compile(req)
    trslist = re.findall(trs,html)
    if len(trslist)==0:
        return ''
    else:
        Str=str(trslist[0])                
        return Str


def get_color(html):
    req=r'var color = ({.*};)'
    trs = re.compile(req)           
    trslist = re.findall(trs,html)
    if len(trslist)==0:
        return ''
    else:
        Str=str(trslist[0])                                           
        return Str





#print "=================================================================================="


#get_config_indetail("http://car.autohome.com.cn/config/spec/19485.html#pvareaid=102170")
#get_config_indetail("http://car.autohome.com.cn/config/spec/1379.html")


#handle_vehicle_config('http://car.autohome.com.cn/config/series/2745.html')

#print "=================================================================================="
#handle_vehicle_config('http://car.autohome.com.cn/config/series/923.html')


#get_qiugou_info('http://www.autohome.com.cn/car/')




if __name__=="__main__":
    update_vehicle_model()
