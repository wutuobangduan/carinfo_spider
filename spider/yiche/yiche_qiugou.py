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
    content = BeautifulSoup(html).find_all(['a','span'])
    #myfile = open(localfile,'w')
    pat = re.compile(r'/qiugou/\d+.html')
    invalid = u'失效'.encode('utf-8')
    #print invalid
    for item in content:
        #print item
        if invalid in item:
            print item
            break
        href = pat.findall(str(item))
        if not href:
            continue
        #is_valid=
        ans = "http://www.taoche.com" + href[0]
        get_qiugou_info(ans)
        #myfile.write(ans)
        #myfile.write('\r\n')
        print ans
    #myfile.close()


def get_qiugou_info(myUrl):
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
    title = soup.find('h4')
    addr = soup.find('a',href=re.compile(r'http://www.taoche.com/qiugou/\w+/'))
    telephone = soup.find_all('em')
    vehicle_body_level = soup.find_all('a',href=re.compile(r'http://www.taoche.com/qiugou/\w+/'))
    trip_distance = soup.find_all('strong')
    for ul in soup.find_all('ul',attrs={'class':'cyxx_new'}):
        for li in ul.find_all('li'):
            if '20' in li.get_text():
                release_time = str(li.get_text()).split('：')[1]
    #is_valid=soup.find_all('span')
    #print is_valid
    #res = [title.next,addr.next,telephone[1].next,vehicle_body_level[1].next,trip_distance[4].next,myUrl,release_time]
    print title.next,addr.next,telephone[1].next,vehicle_body_level[1].next,trip_distance[4].next,release_time
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
    curs = conn.cursor()
    conn.select_db('spider')
    curs.execute("select id from qiu_gou_info where url='%s'" % myUrl)
    getrows=curs.fetchall()
    if not getrows:
        requirements = str(vehicle_body_level[1].next + " | " + trip_distance[4].next).encode('utf-8')
        info_src = "yiche"
        res = [title.next,telephone[1].next,release_time,addr.next,requirements,info_src,myUrl]
        curs.execute("insert into qiu_gou_info(title,telephone,release_time,addrs,other_requirements,info_src,url) values(%s,%s,%s,%s,%s,%s,%s)",res)
    else:
        print 'The data is already in the database...'
    conn.commit()
    curs.close()
    conn.close()

    #strs=str(List[4])
    #print type(strs)
    #print strs
    #li_soup = BeautifulSoup(strs)
    #info = li_soup.find_all('li')
    #print str(info[0]).encode('utf-8')
   # res += [title.next]
   # info = soup.find('a')
   # print info.next


def main():
    url="http://www.taoche.com/qiugou/bspluxt15f/?page="
    localfile="Href.txt"
    for i in range(1,2):
        myUrl = url + str(i)
        grabHref(myUrl,localfile)

if __name__=="__main__":
    main()  
#get_qiugou_info("http://www.taoche.com/qiugou/653581.html")
