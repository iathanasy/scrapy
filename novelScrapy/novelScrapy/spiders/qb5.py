# -*- coding: utf-8 -*-
import scrapy


class Qb5Spider(scrapy.Spider):
    name = 'qb5'
    allowed_domains = ['www.qb5.tw']
    start_urls = ['http://www.qb5.tw/']

    def parse(self, response):
        pass
