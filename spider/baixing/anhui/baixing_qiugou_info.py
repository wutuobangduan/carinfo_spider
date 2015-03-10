# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import socket 
#socket.setdefaulttimeout(60) 
from bs4 import BeautifulSoup

def grabHref(url,localfile):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    html = ''
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
    if html != '':
        for div in BeautifulSoup(html).find_all('div',attrs={'class':'section'}):
            for div2 in div.find_all('div',attrs={'id':'all-list'}):
                content = div2.find_all('a')
        pat = re.compile(r'http://\w+.baixing.com/ershouqiche/a\d+.html')
        dictionary = {}
        for item in content:
            href = pat.findall(str(item))
            if href:
                #if href[0] not in dictionary:
                    print href[0]
                    #dictionary[href[0]] = ''
                    get_qiugou_info(href[0])



def get_qiugou_info(myUrl):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(myUrl,headers=heads)
    html = ''
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
    if html!='':
        soup = BeautifulSoup(html)

        title = soup.find('h2')
        if title is not None:
            print title.next
        vehicle_series = ''
        prices = ''
        brands = ''
        vehicle_colors = ''
        addrs = u'安徽'.encode('utf-8')
        name = ''
        release_time = ''
        img_src = ''
        other_requirements = ''
        vehicle_models = ''
        registration_dates = ''
        trip_distances = ''
        displacements = ''
        transmissions = ''
        major_accidents = ''
        model_levels = ''
        telephone = ''
        detail_informations = ''
        Price = u'价格'.encode('utf-8')
        Brand = u'品牌'.encode('utf-8')
        Vehicle_serie = u'车系列'.encode('utf-8')
        Vehicle_model = u'车型'.encode('utf-8')
        Registration_date = u'上牌'.encode('utf-8')
        Trip_distance = u'行驶里程'.encode('utf-8')
        Addr = u'地区'.encode('utf-8')
        Displacement = u'排量'.encode('utf-8')
        Vehicle_color = u'车辆颜色'.encode('utf-8')
        Transmission = u'变速箱'.encode('utf-8')
        Major_accident = u'重大事故'.encode('utf-8')
        Model_level = u'车型级别'.encode('utf-8')
        click = u'点击查看'.encode('utf-8')
        for div in soup.find_all("div",attrs={'class':'media-body'}):
            for span in div.find_all("span",attrs={'class':'pull-left'}):
                telephone = str(span.get_text())
            if 'data-contact' in  str(div.find_all("a")[0]):
                telephone = telephone[:-4] + str(div.find_all("a")[0].get('data-contact'))

        #print telephone

        if len(soup.find_all("span",attrs={'data-toggle':'tooltip'}))>0:
            release_time = str(soup.find_all("span",attrs={'data-toggle':'tooltip'})[0].get('title')).split('：')[1]
        for div in soup.find_all("div",attrs={'class':'typo-p textwrap','id':'metadata'}):
            for span in div.find_all('span',attrs={'class':'normal'}):
                if Price in str(span.get_text()).split('：')[0]:
                    prices =  str(span.get_text()).split('：')[1]
                elif Brand in str(span.get_text()).split('：')[0]:
                    brands = str(span.get_text()).split('：')[1]
                elif Vehicle_serie in str(span.get_text()).split('：')[0]:
                    vehicle_series = str(span.get_text()).split('：')[1]
                elif Vehicle_model in str(span.get_text()).split('：')[0] and Model_level not in str(span.get_text()).split('：')[0]:
                    vehicle_models = str(span.get_text()).split('：')[1]
                elif Registration_date in str(span.get_text()).split('：')[0]:
                    registration_dates = str(span.get_text()).split('：')[1]
                elif Trip_distance in str(span.get_text()).split('：')[0]:
                    trip_distances = str(span.get_text()).split('：')[1]
                elif Displacement in str(span.get_text()).split('：')[0]:
                    displacements = str(span.get_text()).split('：')[1]
                elif Vehicle_color in str(span.get_text()).split('：')[0]:
                    vehicle_colors = str(span.get_text()).split('：')[1]
                elif Transmission in str(span.get_text()).split('：')[0]:
                    transmissions = str(span.get_text()).split('：')[1]
                elif Major_accident in str(span.get_text()).split('：')[0]:
                    major_accidents = str(span.get_text()).split('：')[1]
                elif Model_level in str(span.get_text()).split('：')[0]:
                    model_levels = str(span.get_text()).split('：')[1]
            for span in div.find_all('span',attrs={'class':'long'}):
                if u'安徽'.encode('utf-8') in str(span.get_text()):
                    addrs = str(span.get_text()).split('：')[1]
                else:
                    addrs += str(span.get_text()).split('：')[1]
        if len(soup.find_all("div",attrs={'class':'typo-p textwrap'}))>0:
            for div in soup.find_all("div",attrs={'class':'typo-p textwrap'})[-1]:
                detail_informations += str(div)
        
        detail_informations = detail_informations.replace('<br/>','')
        for address in soup.find_all("small",attrs={"class":"viewad-mobilearea"}):
            addrs = str(address.get_text())[1:-1] + addrs
        if title is not None:
            print title.next,prices,release_time,telephone,brands,vehicle_series,vehicle_models,registration_dates,trip_distances,addrs,displacements,vehicle_colors,transmissions,major_accidents,model_levels,detail_informations,myUrl
            #print detail_informations,myUrl
            #res= [title.next,telephone,prices,release_time,brands,vehicle_series,vehicle_models,registration_dates,trip_distances,addrs,displacements,vehicle_colors,transmissions,major_accidents,model_levels,detail_informations,myUrl]
        if telephone != '':
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    curs.execute("select id from sell_car_info where telephone_num='%s'" % telephone)
                    get_telephones = curs.fetchall()
                    if not get_telephones:
                        is_seller = u'个人'.encode('utf-8')
                    else:
                        is_seller = u'商家'.encode('utf-8')
                    if telephone.startswith('400'):
                        is_seller = u'商家'.encode('utf-8')
                    car_config = ''
                    if registration_dates != '':
                        car_config += registration_dates + " | "
                    elif trip_distances != '':
                        car_config += trip_distances + " | "
                    elif displacements != '':
                        car_config += displacements + " | "
                    elif transmissions != '':
                        car_config += transmissions + " | "
                    elif vehicle_colors != '':
                        car_config += vehicle_colors
                    info_src = "baixing"
                    res = [title.next,car_config,telephone,addrs,release_time,prices,is_seller,detail_informations,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,telephone_num,addrs,release_time,prices,is_seller,owner_readme,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)


#print "=================================================================================="
#get_qiugou_info('http://yangzhou.baixing.com/ershouqiche/a570379616.html')
#
#print "=================================================================================="



#print "=================================================================================="

#get_qiugou_info('http://zhenjiang.baixing.com/ershouqiche/a587446764.html')

#print "=================================================================================="

#get_qiugou_info('http://xuzhou.baixing.com/ershouqiche/a587757074.html')

def main():
    url="http://anhui.baixing.com/ershouqiche/?page="
    localfile="Href.txt"
    for i in range(1,5):
        myUrl = url + str(i)
        grabHref(myUrl,localfile)

if __name__=="__main__":
    main()
