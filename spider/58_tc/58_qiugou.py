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
#socket.setdefaulttimeout(60)

def grabHref(url,localfile):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
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
    content = BeautifulSoup(html).find_all('a')
    pat = re.compile(r'http://\w+.58.com/ershoucheqg/\d+x.shtml')
    addr = re.compile(r'/\w*/ershoucheqg/')
#    soup = BeautifulSoup(html)
#    for td in soup.find_all("td",attrs={"class":"t"}):
#        print td.get_text()
    for item in content:
        href = pat.findall(str(item))
        address = addr.findall(str(item))
        if href:
            print href[0]
            get_qiugou_info(href[0])



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


def get_qiugou_info(myUrl):
    proxy = {'http':'http://202.106.16.36:3128'}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(myUrl,headers=heads)
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
    soup = BeautifulSoup(html)
    title = soup.find('h1')

    #print title.next
    Tag = u'标签'.encode('utf-8')
    price = u'价位'.encode('utf-8')
    displacement = u'排量'.encode('utf-8')
    transmission = u'变速器'.encode('utf-8')
    Travel_requirement = u'行程'.encode('utf-8')
    Tags = ''
    prices = ''
    displacements = ''
    transmissions = ''
    Travel_requirements = ''
    is_seller = ''
    name = ''
    release_time = ''
    for ul in soup.find_all("ul",attrs={"class":"info"}):
        for li in ul.find_all("li"): 
            if Tag in li.get_text():
                Tags = str(li.get_text()).split('：')[1]
            if price in li.get_text():
                prices = str(li.get_text()).split('：')[1]
            if displacement in li.get_text():
                displacements = str(li.get_text()).split('：')[1]
            if transmission in li.get_text():
                transmissions = str(li.get_text()).split('：')[1]
            if Travel_requirement in li.get_text():
                Travel_requirements = str(li.get_text()).split('：')[1]
    #print Tags,prices,displacements,transmissions,Travel_requirements
    for ul in BeautifulSoup(html).find_all("div",attrs={"class":"user"}):
        for script in ul.find_all('script'):
            if len(str(script.get_text()).split(','))>3:
                #print str(script.get_text()).split(',') 
                is_seller = str(script.get_text()).split(',')[-3].split(':')[1]
                name = str(script.get_text()).split(',')[-2].split(':')[1]
    #print is_seller,name
    img = soup.findAll('img')
    img_src = ''
    if len(img)>0:
        #print img[0].attrs["src"]
        img_src=img[0].attrs["src"]
    else:
        for ul in soup.find_all('div',attrs={'class':'user'}):
            for img in ul.find_all('script',attrs={'language':'javascript'}):
                img_all = img.get_text()
                
                #print img_all[img_all.find('http'):-6]
                img_src = img_all[img_all.find('http'):-6]
    print img_src
    uni_number = str(myUrl.split('/')[-1]).split('.')[0]
    #if img_src.find('ttp')>0:
    #    urllib.urlretrieve(img_src,'/data/python/spider/58_tc/changzhou/%s.jpg' % uni_number)
  
    for ul in soup.find_all("div",attrs={"class":"other"}):
         release_time = str(ul.contents[0].split('：')[1]).split('\n')[0]
    if myUrl.split('/')[2].split('.')[0] == 'cz':
        addr = u'江苏常州'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'su':
        addr = u'江苏苏州'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'nj':
        addr = u'江苏南京'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'wx':
        addr = u'江苏无锡'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'xz':
        addr = u'江苏徐州'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'nt':
        addr = u'江苏南通'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'yz':
        addr = u'江苏扬州'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'yancheng':
        addr = u'江苏盐城'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'ha':
        addr = u'江苏淮安'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'lyg':
        addr = u'江苏连云港'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'taizhou':
        addr = u'江苏泰州'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'suqian':
        addr = u'江苏宿迁'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'zj':
        addr = u'江苏镇江'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'shuyang':
        addr = u'江苏沭阳'.encode('utf-8')
    elif myUrl.split('/')[2].split('.')[0] == 'dafeng':
        addr = u'江苏大丰'.encode('utf-8')
    else:
        addr = None
    #if img_src.find('ttp')>0:
        #try:
        #    fp = open("/data/python/spider/58_tc/changzhou/%s.jpg" % uni_number)
        #    myImg = fp.read()
        #    fp.close()
        #except IOError,e:
        #    print "Error %d %s" % (e.args[0],e.args[1])
        #    sys.exit(1)
    
        #res = [title.next,Tags,prices,displacements,transmissions,Travel_requirements,is_seller,name,uni_number,img_src,myUrl,release_time,addr]

    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
        curs = conn.cursor()
        conn.select_db('spider')
        if img_src != '' and addr is not None and release_time != '':
            curs.execute("select id from qiu_gou_info where url='%s'" % myUrl)
            getrows=curs.fetchall()
            if not getrows:
                requirements = Tags + " | " + displacements + " | " + transmissions + " | " + Travel_requirements 
                info_src = "58"
                res = [title.next,name,release_time,addr,prices,requirements,img_src,info_src,myUrl]
                curs.execute("insert into qiu_gou_info(title,name,release_time,addrs,prices,other_requirements,img_src,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
            else:
                print 'The data is already in the database...'
        conn.commit()
        curs.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)


#get_qiugou_info('http://cz.58.com/ershoucheqg/18576667119879x.shtml')


#print "==========================="

#get_qiugou_info('http://nj.58.com/ershoucheqg/20618520091265x.shtml')

#print "==========================="

#get_qiugou_info('http://nj.58.com/ershoucheqg/20618376714376x.shtml')

#print "==========================="

#get_qiugou_info('http://nj.58.com/ershoucheqg/13455984775049x.shtml')

def main():
    #addr_list = ['nj']
    addr_list = ['cz','su','nj','wx','xz','nt','yz','yancheng','ha','lyg','taizhou','suqian','zj','shuyang','dafeng']
    for i in range(len(addr_list)):
        url="http://"+addr_list[i]+".58.com/ershoucheqg/pn"
        localfile="Href.txt"
        for j in range(1,2):
            myUrl = url + str(j)
            grabHref(myUrl,localfile)

if __name__=="__main__":
    main()
