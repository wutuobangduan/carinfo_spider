# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from douban_program_book.items import DoubanProgramBookItem

class doubanbookSpider(scrapy.Spider):
    name = "book"
    allow_domains = ["http://www.che168.com/jiangsu/BuyList------p.html"]
    start_urls = ["http://www.che168.com/jiangsu/BuyList------p.html"]
    def parse(self,response):
        items = []
        item = DoubanProgramBookItem()
        for sel in response.xpath('//td[@class="font12NoLine left"]'):
            item = DoubanProgramBookItem()
            item['title'] = sel.xpath("a/@title").extract()
            item['link'] = sel.xpath("a/@href").extract()
            items.append(item)
        return items
