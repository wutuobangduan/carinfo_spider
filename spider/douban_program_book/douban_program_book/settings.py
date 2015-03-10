# -*- coding: utf-8 -*-

# Scrapy settings for douban_program_book project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import sys
import os
from os.path import dirname
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)

BOT_NAME = 'douban_program_book'

SPIDER_MODULES = ['douban_program_book.spiders']
NEWSPIDER_MODULE = 'douban_program_book.spiders'

ITEM_PIPELINES = {'douban_program_book.pipelines.DoubanProgramBookPipeline':300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban_program_book (+http://www.yourdomain.com)'

LOG_LEVEL = 'INFO'
