# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 手机名称
    name = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 评论数
    comment_num = scrapy.Field()
    # 店铺名称
    shop_name = scrapy.Field()
    # 店铺链接
    shop_link = scrapy.Field()
