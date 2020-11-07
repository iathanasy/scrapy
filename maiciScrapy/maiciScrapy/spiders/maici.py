# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import MaiciscrapyItem

# # 单机
# class MaiciSpider(scrapy.Spider):
#     name = 'maici'
#     allowed_domains = ['www.ailinglei.com']
#     start_urls = ['https://www.ailinglei.com/news/list-id-7-1.html/']
#
#     def parse(self, response):
#         papers = response.xpath(".//*[@class='list']/li")
#         # 列表中抽取
#         for paper in papers:
#             url = paper.xpath(".//a/@href").extract()[0]
#
#             title = paper.xpath(".//a/font/text()").extract()[0]
#             time = paper.xpath(".//a/span/text()").extract()[0]
#
#             item = MaiciscrapyItem(title=title, time=time)
#             newUrl = 'https:' + url;
#             request = scrapy.Request(url=newUrl, callback=self.parse_body)
#             request.meta['item'] = item  # 将item暂存
#             yield request
#
#
#
#     def parse_body(self, response):
#         item = response.meta['item']
#         body = response.xpath(".//*[@class='content t20']").extract()[0]
#
#         re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
#         re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
#         re_div = re.compile('<div class="boTex"[^>]*?>[\s\S]*?<\/div>', re.I)
#
#         body = re.sub(re_script, '', body)
#         body = re.sub(re_style, '', body)
#         body = re.sub(re_div, '', body)
#         body = body.replace('<span><var id="wp_playTime">00:00</var><label> | </label><var id="wp_totalTime">00:00</var></span>', '')
#         print(body)
#         # txt = ''
#         # for i in range(len(body)):
#         #     txt = txt + body[i] + '<br>'  # strip()去掉首位空格字符，‘\n’换行
#         #     # txt = txt.replace('全本小说网 www.qb5.tw，最快更新', '')  # replace()可以替换不需要的字符串
#         #     # txt = txt.replace('最新章节！', '')  # replace()可以替换不需要的字符串
#         #
#         item['content'] = body
#         yield item

# 分布式
class MaiciSpider(CrawlSpider):
    name = 'maici'
    allowed_domains = ['www.ailinglei.com']
    start_urls = ['https://www.ailinglei.com/news/list-id-7-1.html/']
    rules = (
        Rule(LinkExtractor(allow=("/news/list-id-7-\d{1,}.html",)),
             follow=True,
             callback='parse_item'
             ),
    )

    def parse_item(self, response):
        papers = response.xpath(".//*[@class='list']/li")
        # 列表中抽取
        for paper in papers:
            url = paper.xpath(".//a/@href").extract()[0]

            title = paper.xpath(".//a/font/text()").extract()[0]
            time = paper.xpath(".//a/span/text()").extract()[0]

            item = MaiciscrapyItem(title=title, time=time)
            newUrl = 'https:' + url;
            request = scrapy.Request(url=newUrl, callback=self.parse_body)
            request.meta['item'] = item  # 将item暂存
            yield request


    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='content t20']").extract()[0]

        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
        re_div = re.compile('<div class="boTex"[^>]*?>[\s\S]*?<\/div>', re.I)

        body = re.sub(re_script, '', body)
        body = re.sub(re_style, '', body)
        body = re.sub(re_div, '', body)
        body = body.replace('<span><var id="wp_playTime">00:00</var><label> | </label><var id="wp_totalTime">00:00</var></span>', '')
        # txt = ''
        # for i in range(len(body)):
        #     txt = txt + body[i] + '<br>'  # strip()去掉首位空格字符，‘\n’换行
        #     # txt = txt.replace('全本小说网 www.qb5.tw，最快更新', '')  # replace()可以替换不需要的字符串
        #     # txt = txt.replace('最新章节！', '')  # replace()可以替换不需要的字符串
        #
        item['content'] = body
        yield item