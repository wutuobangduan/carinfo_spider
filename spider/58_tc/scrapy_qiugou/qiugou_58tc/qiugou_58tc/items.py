# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Qiugou58TcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    release_time = scrapy.Field()
    addr = scrapy.Field()
    tag = scrapy.Field()
    price = scrapy.Field()
    displacement = scrapy.Field()
    transmission = scrapy.Field()
    Travel_requirement = scrapy.Field()
    is_seller = scrapy.Field()
    name = scrapy.Field()
    img_src = scrapy.Field()
