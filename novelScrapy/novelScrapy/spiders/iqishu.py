# -*- coding: utf-8 -*-
import scrapy


class IqishuSpider(scrapy.Spider):
    name = 'iqishu'
    allowed_domains = ['www.iqishu.la']
    start_urls = ['http://www.iqishu.la/']

    def parse(self, response):
        pass
