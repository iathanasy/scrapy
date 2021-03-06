# -*- coding: utf-8 -*-
import scrapy

from ..items import JdItem


class DjSpider(scrapy.Spider):
    name = 'dj'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=手机']
    page = 2

    def parse(self, response):
        # 获取节点
        node_list = response.xpath('//div[@class="gl-i-wrap"]')
        # 打印个数
        print(len(node_list))
        # 拿出节点每个信息
        for node in node_list:
            item = JdItem()
            # 我们try一下，有些缺失的抛错，我们阻止异常，返回None
            try:
                item["name"] = node.xpath('./div[4]/a/em/text()').extract_first().strip()
            except:
                item["name"] = None
            try:
                item["link"] = response.urljoin(node.xpath('./div[4]/a/@href').extract_first())
            except:
                item["link"] = None

            try:
                item["price"] = node.xpath('./div[3]/strong/i/text()').extract_first() + '元'
            except:
                item["price"] = None

            try:
                item["comment_num"] = node.xpath('./div[5]/strong/a/text()').extract_first()
            except:
                item["comment_num"] = None

            try:
                item["shop_name"] = node.xpath('./div[7]/span/a/text()').extract_first().strip()
            except:
                item["shop_name"] = None

            try:
                item["shop_link"] = "https:" + node.xpath('./div[7]/span/a/@href').extract_first()
            except:
                item["shop_link"] = None
            print(item)
            # 返回item，交给pipline
            yield item
        # 采用拼接的方式获取下一页
        if self.page < 74:
            next_url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&page={}'.format(self.page)
            self.page += 1
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
