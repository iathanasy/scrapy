# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector

from ..items import CnblogspiderItem
from scrapy_redis.spiders import RedisSpider


class CnblogSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['https://www.cnblogs.com/iathanasy/default.html?page=1']

    def parse(self, response):
        # 里面实现网页的而解析
        # 里面实现网页的而解析
        # 首先抽取所有的文章
        papers = response.xpath(".//*[@class='day']")
        # 从每篇文章中抽取数据
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/span/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item  # 将item暂存
            yield request

        next_page = response.xpath("//div[@id='nav_next_page']/a/@href").extract()
        if not next_page:
            next_page = Selector(response).re(r'<a href="(\S*)">下一页</a>')
        print(next_page)
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['cimage_urls'] = body.xpath('.//img//@src').extract()  # 提取图片链接
        yield item



'''
class CnblogsSpider(CrawlSpider):
    name = 'cnblogs'
    allowed_domains = ["cnblogs.com"]#允许的域名
    start_urls = [
    "https://www.cnblogs.com/iathanasy/default.html?page=1"
    ]
    rules = (
            Rule(LinkExtractor(allow=("/iathanasy/default.html\?page=\d{1,}",)),
                      follow=True,
                      callback='parse_item'
    ),
                 )
    def parse_item(self,response):
        papers = response.xpath(".//*[@class='day']")
        #从每篇文章中抽取数据
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/span/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url,callback=self.parse_body)
            request.meta['item'] = item
        yield request

    def parse_body(self,response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['cimage_urls'] = body.xpath('.//img//@src').extract()#提取图片链接
        yield item
'''

'''
class CnblogSpider(RedisSpider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['https://www.cnblogs.com/iathanasy/default.html?page=1']
    redis_key = 'cnblogs:start_urls'

    def parse(self, response):
        # 里面实现网页的而解析
        # 里面实现网页的而解析
        # 首先抽取所有的文章
        papers = response.xpath(".//*[@class='day']")
        # 从每篇文章中抽取数据
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/span/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item  # 将item暂存
            yield request

        next_page = response.xpath("//div[@id='nav_next_page']/a/@href").extract()
        if not next_page:
            next_page = Selector(response).re(r'<a href="(\S*)">下一页</a>')
        print(next_page)
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['cimage_urls'] = body.xpath('.//img//@src').extract()  # 提取图片链接
        yield item
'''


'''
class CnblogSpider(CrawlSpider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['https://www.cnblogs.com/iathanasy/default.html?page=1']

    def parse(self, response):
        # 里面实现网页的而解析
        # 里面实现网页的而解析
        # 首先抽取所有的文章
        papers = response.xpath(".//*[@class='day']")
        # 从每篇文章中抽取数据
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/span/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item  # 将item暂存
            yield request

        next_page = response.xpath("//div[@id='nav_next_page']/a/@href").extract()
        if not next_page:
            next_page = Selector(response).re(r'<a href="(\S*)">下一页</a>')
        print(next_page)
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['cimage_urls'] = body.xpath('.//img//@src').extract()  # 提取图片链接
        yield item
'''