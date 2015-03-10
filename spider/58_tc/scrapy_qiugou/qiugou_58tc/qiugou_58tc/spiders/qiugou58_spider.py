# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib
import re
import simplejson
from scrapy.http import Request
from qiugou_58tc.items import Qiugou58TcItem
from scrapy import Selector
#class qiugou58Spider(scrapy.Spider):
#    name = "qiugou58"
#    allow_domains = ["58.com"]
#    start_urls = ["http://nj.58.com/ershoucheqg/"]
#    def parse(self,response):
#        items = []
#        for sel in response.xpath('//div[@id="infolist"]/table[@class="tblist"]/td[@class="t"]'):
#            item = Qiugou58TcItem()
#            item['title'] = sel.xpath("a[1]/text()").extract()
#            item['link'] = sel.xpath("a[1]/@href").extract()
#            items.append(item)
#        for item in items:
#            yield Request(item['link'],meta={'item':item},callback=self.parse2)      
#    def parse2(self,response):
#        items = []
#        item = Qiugou58TcItem()
#        item['tag'] = ''
#        item['price'] = ''
#        item['displacement'] = ''
#        item['transmission'] = ''
#        item['Travel_requirement'] = ''
#        item['addr'] = ''
#        item['is_seller'] = ''
#        item['name'] = ''
#        item['img_src'] = ''
#        item['release_time'] = ''
#        item['link'] = ''
#        item['title'] = ''
        
#        item['tag'] = response.xpath('//div[@class="w"]/ul[@class="info"]/li[1]/a/text()').extract()
#        item['price'] = response.xpath('//div[@class="w"]/ul[@class="info"]/li[2]/text()').extract()
#        item['displacement'] = response.xpath('//div[@class="w"]/ul[@class="info"]/li[3]/text()').extract()
#        item['transmission'] = response.xpath('//div[@class="w"]/ul[@class="info"]/li[4]/text()').extract()
#        item['Travel_requirement'] = response.xpath('//div[@class="w"]/ul[@class="info"]/li[5]/text()').extract()
#        item['addr'] = u'南京'.encode('utf-8')
#        item['is_seller'] = response.xpath('//div[@class="w"]/div[@class="user"]/ul[@class="userinfo"]/li[1]/em/text()').extract()
#        item['name'] = response.xpath('//div[@class="w"]/div[@class="user"]/ul[@class="userinfo"]/li[1]/a/@title').extract()
#        item['img_src'] = response.xpath('//div[@class="w"]/div[@class="user"]/ul[@class="vuser nomargin"]/li[1]/img/@src').extract()
#        item['release_time'] = response.xpath('//div[@class="w headline"]/div[@class="other"]/text()').extract()
#        item['link'] = response.item['link']
#        item['title'] = response.xpath('//div[@class="w headline"]/h1/text()').extract()
#        items.append(item)
#        return items


class qiugou58Spider(scrapy.Spider):
    name = "qiugou58"
    allow_domains = ["58.com"]
    start_urls = []
    for i in range(1,13):
        start_urls += ["http://nj.58.com/ershoucheqg/pn"+str(i)]
    def parse(self,response):
        items = []
        item = Qiugou58TcItem()
        raw_urls = response.xpath("//a/@href").extract()
        urls = []
        for url in raw_urls:
           if 'nj.58.com/ershoucheqg/' in url :
               urls.append(url)
        for url in urls:
            yield Request(url)
        sel = Selector(response)

        item['tag'] = []
        item['price'] = []
        item['displacement'] = []
        item['transmission'] = []
        item['Travel_requirement'] = []
        item['addr'] = []
        item['is_seller'] = []
        item['name'] = []
        item['img_src'] = []
        item['release_time'] = []
        item['title'] = []
        item['link'] = response.url.encode('utf-8')
        item['tag'] = sel.xpath('//div[@class="w"]/ul[@class="info"]/li[1]/a/text()').extract()
        item['price'] = sel.xpath('//div[@class="w"]/ul[@class="info"]/li[2]/text()').extract()
        item['displacement'] = sel.xpath('//div[@class="w"]/ul[@class="info"]/li[3]/text()').extract()
        item['transmission'] = sel.xpath('//div[@class="w"]/ul[@class="info"]/li[4]/text()').extract()
        item['Travel_requirement'] = sel.xpath('//div[@class="w"]/ul[@class="info"]/li[5]/text()').extract()
        item['addr'] = [u'南京'.encode('utf-8')]
        item['is_seller'] = sel.xpath('//div[@class="w"]/div[@class="user"]/div[@id="newuser"]/ul[@class="userinfo"]/li[1]/em[@class="medium"]/text()').extract()
        item['name'] = sel.xpath('//div[@class="w"]/div[@class="user"]/div[@id="newuser"]/ul[@class="userinfo"]/li[1]/a[@class="tx"]/@title').extract()
        item['img_src'] = sel.xpath('//div[@class="w"]/div[@class="user"]/ul[@class="vuser nomargin"]/li[1]/span[@class="phone"]/img/@src').extract()
        item['release_time'] = response.xpath('//div[@class="w headline"]/div[@class="other"]/text()').extract()
        pat = re.compile(r'\d+-\d+-\d+')
        item['release_time'] = pat.findall(item['release_time'][0])
        item['title'] = response.xpath('//div[@class="w headline"]/h1/text()').extract()
        yield item
