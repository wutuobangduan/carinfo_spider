#!/usr/bin/python
import urllib
import urllib2
import MySQLdb
import re
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def getHtml(myUrl):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads={'User-Agent':user_agent}
    req=urllib2.Request(myUrl,headers=heads)
    myResponse=urllib2.urlopen(req)
    myPage=myResponse.read()


    soup = BeautifulSoup(myPage)

    #Str=''
    #Str+=(soup.table).encode('utf-8')
    #soup=BeautifulSoup(Str)
   

    table = soup.find("ul", attrs={"id":"logwtqiugou"})
    

    names=[td.get_text() for td in soup.find_all("div",attrs={"class":"box-1"})]

    print names
    #for row in table.find_all("tr")[1:]:
#	for td in row.find_all("td"):
#	    if i%2!=0:
#	        a=i>>1
#		if a<270:
#		    datasets[a]=td.get_text().encode('utf-8')
#	    i+=1
	    #td.get_text().encode('utf-8')
	    
    #for row in table.find_all("tr")[1:]:
    #    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    #	datasets.append(dataset)

#    result=zip(names,datasets)
#    return result
    #for i in range(len(result)):
    #    print result[i][0].encode('utf-8')+":"+result[i][1].encode('utf-8')
    #print result
    #for name in names:
    #    print name.encode('utf--8')
    #for data in datasets:
    #   print data.encode('utf-8')
    #print datasets

    

#    trslist = re.findall('<tr>([\s\S])</tr>',myPage,re.S)
    

def getConf(html):
    reg=r'<tr>[\s\S]*<\/tr>'
    trs = re.compile(reg)
    trslist = re.findall('<tr>([\s\S]*)</tr>',html)

    items=[]
    for item in trslist:
        items.append(item.replace("\n",""))
    return items

#def name_to_conf(name,ans,result):
#    return {
#        '':ans[0]= 
#        }

print getHtml("http://www.taoche.com/qiugou/bspluxt15f/?page=1")
#for i in range(22000,22001):
#   url="http://www.che168.com/cardetail/carconfig_"+str(i)+".html"
#   result=getHtml(url)
#   conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
#   curs = conn.cursor()
#   conn.select_db('spider')
#   ans=['' for m in range(270)]
#   for j in range(len(result)):
#       ans[j]=result[j][1]
#   ans=[i]+[i]+ans
#   curs.execute("insert into vehicle_model_conf values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",ans)
#   conn.commit()
#   curs.close()
#   conn.close()
