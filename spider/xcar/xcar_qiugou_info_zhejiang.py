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

import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO


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
    #print img.info,img.size,img.format
    img = img.convert("RGBA")  
    pixdata = img.load()
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            #print pixdata[x, y]
            if pixdata[x, y][3] >50:
                pixdata[x, y] = (0, 0, 0,255)
            else:
                pixdata[x, y] = (255, 255, 255,255)
    return img



def division(img):              #图像的分割，就是验证码按字符分割出来
    #global nume
    nume=0
    font=[]
    for i in range(11):
        
        #x = 9 + i*7 #这里的数字参数需要自己 
        y = 15 #根据验证码图片的像素进行
        if i==0:
            x = 1
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13)) 
                a1 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a1 = 9

        elif i == 1:
            x += a1 
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a2 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a2 = 9
        elif i == 2:
            x += a2
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a3 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a3 = 9
        elif i == 3:
            x += a3
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a4 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a4 = 9
        elif i == 4:
            x += a4
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a5 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a5 = 9
        elif i == 5:
            x += a5
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a6 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a6 = 9
        elif i == 6:
            x += a6
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a7 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a7 = 9
        elif i == 7:
            x += a7
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a8 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a8 = 9
        elif i == 8:
            x += a8 
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a9 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a9 = 9
        elif i == 9:
            x += a9
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
                a10 = 10
            else:
                temp = img.crop((x,y,x+9,y+13))
                a10 = 9
        elif i == 10:
            x += a10
            temp1 = img.crop((x,y,x+9,y+13))
            pixdata = temp1.load()
            if pixdata[7,9][2]==0:
                temp = img.crop((x,y,x+10,y+13))
            else:
                temp = img.crop((x,y,x+9,y+13))
        temp.save("/data/python/spider/xcar/temp/%d.png" % nume)
        nume=nume+1
        font.append(temp)
    return font

def recognize(img):        #分隔出来的字符与预先定义的字体库中的结果逐个像素进行对比找出差别最小的项
    fontMods = []
    for i in range(10):
        fontMods.append((str(i), Image.open("/data/python/spider/xcar/fonts/%d.png" % i)))
    result=""
    font=division(img)
     
    for i in font:
        target=i
        points = []
        for mod in fontMods:
            diffs = 0
            for yi in range(13):
                for xi in range(9):     #以下多行为自己修改，参考文章中的值对比存在问题
                    #print "mod[1].getpixel((xi,yi)):"+str(mod[1].getpixel((xi, yi)))
                    #print "target.getpixel((xi,yi)):"+str(target.getpixel((xi, yi)))
                    if mod[1].getpixel((xi, yi)) != target.getpixel((xi, yi)):
                        diffs += 1
            #print "diffs：" + str(diffs)
            points.append((diffs, mod[0]))
        points.sort()
        result += points[0][1]
    return result


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
    pat = re.compile(r'/qiugou/\d+.htm')
    for item in content:
        href = pat.findall(str(item))
        if href:
            #print href[0]
            ans = 'http://used.xcar.com.cn' + href[0]
            print ans
            get_qiugou_info(ans)



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
    title = soup.find('h3')
    print title.next
    vehicle_series = ''
    prices = ''
    vehicle_class = ''
    vehicle_age = ''
    vehicle_color = ''
    addr = ''
    name = ''
    release_time = ''
    img_src = ''
    other_requirements = ''
    contact = u'姓　名'.encode('utf-8')
    i=1
    for div in soup.find_all("div",attrs={'class':'buy_conte'}):
        for td in div.find_all("td"):
            #print str(td.get_text()).split('：')[0]
            if i == 2:
                vehicle_series = str(td.get_text()).split('：')[0]
            elif i == 4:
                prices = str(td.get_text()).split('：')[0]
            elif i == 6:
                vehicle_age = str(td.get_text()).split('：')[0]
            elif i == 8:
                addr = str(td.get_text()).split('：')[0]
            elif i == 12:
                vehicle_class = str(td.get_text()).split('：')[0]
            elif i == 10:
                release_time = str(td.get_text()).split('：')[0]
            elif i == 14:
                vehicle_color = str(td.get_text()).split('：')[0]
            elif i == 16:
                other_requirements = str(td.get_text()).split('：')[0]
            i += 1
    #print vehicle_series,prices,vehicle_age,addr,release_time,vehicle_class,vehicle_color,other_requirements

    for div in soup.find_all("div",attrs={'class':'buy_conte'}):
        for p in div.find_all("p"):
            if contact in p.get_text():
                name = str(p.get_text()).split('：')[1]
    for span in soup.find_all("span",attrs={'class':'c_f76'}):
        for img in span.find_all("img"):
            img_src = 'http://used.xcar.com.cn' + img.get('src')
    print vehicle_series,prices,vehicle_age,addr,release_time,vehicle_class,vehicle_color,other_requirements,name,img_src,myUrl


    uni_number = str(myUrl.split('/')[-1]).split('.')[0]
    telephone_num = ''
    if img_src.find('ttp')>0:
        img=binary(img_src)
        telephone_num = recognize(img)
        print telephone_num
        #urllib.urlretrieve(img_src,'/data/python/spider/xcar/telephone_img/%s.jpg' % uni_number)
    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
        curs = conn.cursor()
        conn.select_db('spider')
        if img_src != '':
            curs.execute("select id from qiu_gou_info where url='%s'" % myUrl)
            getrows=curs.fetchall()
            if not getrows:
                requirements = str(vehicle_series + " | " + vehicle_age + " | " + vehicle_class + " | " + vehicle_color  + " | " + other_requirements).encode('utf-8')
                info_src = 'xcar'
                res = [title.next,name,telephone_num,release_time,addr,prices,requirements,img_src,info_src,myUrl]
                curs.execute("insert into qiu_gou_info(title,name,telephone,release_time,addrs,prices,other_requirements,img_src,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
            else:
                print 'The data is already in the database...'
        conn.commit()
        curs.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)

#get_qiugou_info('http://used.xcar.com.cn/qiugou/881.htm')

#print "====================================="
#get_qiugou_info('http://used.xcar.com.cn/qiugou/808.htm')


def main():
    url = "http://used.xcar.com.cn/qiugou/26-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0?RequestBuy_page="
    localfile="Href.txt"
    for i in range(1,2):
        myUrl = url + str(i)
        grabHref(myUrl,localfile)

if __name__=="__main__":
    main()
