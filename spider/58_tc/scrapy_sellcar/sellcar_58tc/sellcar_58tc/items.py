# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Sellcar58TcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
    telephone = scrapy.Field()
    release_time = scrapy.Field()
    addrs = scrapy.Field()
    is_seller = scrapy.Field()
    owner_readme = scrapy.Field()
    url = scrapy.Field()
