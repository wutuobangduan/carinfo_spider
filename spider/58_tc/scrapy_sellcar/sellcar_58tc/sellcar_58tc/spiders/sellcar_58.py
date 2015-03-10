# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib
import re
import simplejson
from scrapy.http import Request
from sellcar_58tc.items import Sellcar58TcItem
from scrapy import Selector
from bs4 import BeautifulSoup
import urllib2




class sellcar58Spider(CrawlSpider):
    name = "sellcar58"
    allow_domains = ["58.com"]
    
    start_urls = []
    #addr_list = ['cz','su','nj','wx','xz','nt','yz','yancheng','ha','lyg','taizhou','suqian','zj','shuyang','dafeng']
    addr_list = ['nj']
    for addr in addr_list:
        for i in range(1,2):
            start_urls += ["http://" + addr + ".58.com/ershouche/1/pn"+str(i)]
    
    def parse(self,response):
        #items = []
        #item = Sellcar58TcItem()
        urls = []
        hxs = Selector(response)
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        heads = {'User-Agent':user_agent}
        req = urllib2.Request(str(response)[5:-1],headers=heads)
        html = ''
        fails = 0
        while True:
            try:
                if fails >= 10: 
                    break
                rs = urllib2.urlopen(req,timeout=30)
                html = rs.read()
            except:
                fails += 1
                print "Handing brand,the network may be not Ok,please wait...",fails
            else:
                break
        if html != '':
            soup = BeautifulSoup(html)
            for div in soup.find_all('div',attrs={'class':'cleft'}):
                for table in div.find_all('table',attrs={'class':'tbimg'}):
                    for td in table.find_all('td',attrs={'class':'t'}):
                        for a in td.find_all('a'):
                            urls.append(a.get('href'))
        
        #raw_urls = hxs.xpath('//a/@href').extract()
        #/table[@class="tbimg"]/td[@class="img"]
        #raw_urls = response.xpath("//a/@href").extract()
        #print "The length .... ", len(raw_urls)
        #urls = []
        #for url in raw_urls:
        #   if '58.com/' in url :
        #       urls.append(url)
        for url in urls:
            yield Request(url,callback=self.parse_page)
        #sel = Selector(response)
        
    def parse_page(self,response):
        item = Sellcar58TcItem()
        hxs = Selector(response)
        item['title'],item['price'],item['name'],item['telephone'],item['release_time'],item['addrs'],item['is_seller'],item['is_seller'] = '','','','','','','',''
        if len(hxs.xpath('//div[@id="content_sumary_right"]/h1[@class="h1"]/text()').extract())>0 and len(hxs.xpath('//div[@id="content_sumary_right"]/p[@class="lineheight_2"]/a/text()').extract())>0 and len(hxs.xpath('//div[@id="content_sumary_right"]/div[@id="content_price"]/div[@class="content_price_left"]/span[@class="font_jiage"]/text()').extract()):
            item['title'] = hxs.xpath('//div[@id="content_sumary_right"]/h1[@class="h1"]/text()').extract()[0]
            item['price'] = hxs.xpath('//div[@id="content_sumary_right"]/div[@id="content_price"]/div[@class="content_price_left"]/span[@class="font_jiage"]/text()').extract()[0]
            item['name'] = hxs.xpath('//div[@id="content_sumary_right"]/p[@class="lineheight_2"]/a/text()').extract()[0]
            item['telephone'] = hxs.xpath('//div[@id="content_sumary_right"]/p[@class="lineheight_2"]/span[@id="t_phone"]/text()').extract()[0]
            item['release_time'] = hxs.xpath('//div[@id="content_sumary_right"]/div[@class="mtit_con c_999 f12 clearfix"]/ul[@class="mtit_con_left fl"]/li/text()').extract()[0]
            item['is_seller'] = u'商家'.encode('utf-8')
            item['owner_readme'] = hxs.xpath('//div[@class="benchepeizhi"]/text()').extract()[0]
            item['url'] = response.url
        if response.url.split('/')[2].split('.')[0] == 'cz':
            item['addrs'] = u'江苏常州'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'su':
            item['addrs'] = u'江苏苏州'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'nj':
            item['addrs'] = u'江苏南京'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'wx':
            item['addrs'] = u'江苏无锡'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'xz':
            item['addrs'] = u'江苏徐州'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'nt':
            item['addrs'] = u'江苏南通'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'yz':
            item['addrs'] = u'江苏扬州'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'yancheng':
            item['addrs'] = u'江苏盐城'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'ha':
            item['addrs'] = u'江苏淮安'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'lyg':
            item['addrs'] = u'江苏连云港'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'taizhou':
            item['addrs'] = u'江苏泰州'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'suqian':
            item['addrs'] = u'江苏宿迁'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'zj':
            item['addrs'] = u'江苏镇江'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'shuyang':
           item['addrs'] = u'江苏沭阳'.encode('utf-8')
        elif response.url.split('/')[2].split('.')[0] == 'dafeng':
            item['addrs'] = u'江苏大丰'.encode('utf-8')
        else:
            item['addrs'] = None
        if item['addrs'] is not None and item['telephone'] != '' and len(item['telephone'])>0:
            for it in item:
                print "yeah ~~~"
                print it
            #yield item
        
