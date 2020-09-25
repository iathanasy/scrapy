# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    # 文件
    file_urls = scrapy.Field()
    files = scrapy.Field()

    # 图片
    cimage_urls = scrapy.Field()
    cimages = scrapy.Field()

