# -*- coding: utf-8 -*-
import time
from dateutil import parser

import scrapy


# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider

from ..items import NovelscrapyItem, NovelscrapyDetailItem
from ..utlis.extract import extract_pre_next_chapter, extract_chapters


class Qb5Spider(scrapy.Spider):
    name = 'qb5'
    allowed_domains = ['www.qb5.tw']
    start_urls = ['http://www.qb5.tw/']

    '''
    '1', '玄幻奇幻'
    '2', '武侠仙侠'
    '3', '都市言情'
    '4', '历史军事'
    '5', '侦探推理'
    '6', '网游竞技'
    '7', '科幻灵异'
    '8', '恐怖灵异'
    '9', '其他类型'
    '''

    # 一级解析：获取主题
    def parse(self, response):
        # topic_list = response.xpath('//div[@class="nav_cont"]/ul/li[position()>1 and position()<9]')
        # for i in topic_list:
        #     novel_topic = i.xpath('./a/@title').get()
        #     link = i.xpath('./a/@href').get()
        #
        #     m = re.match(".*/fenlei/(\d+)_(\d+)/", link)
        #     novel_topic_id = m.group(1)
        #     yield scrapy.Request(
        #         url=link,
        #         meta={'novel_topic': novel_topic, 'novel_topic_id': novel_topic_id},
        #         callback=self.parse_page
        #     )


        # 仙侠修真
        novel_topic = "仙侠修真"
        # link = "https://www.qb5.tw/fenlei/2_3/" 待爬
        # link = "https://www.qb5.tw/fenlei/2_11/"
        link = "https://www.qb5.tw/fenlei/2_14/" # 14-89
        novel_topic_id = 2

        # 玄幻奇幻
        # novel_topic = "玄幻奇幻"
        # # link = "https://www.qb5.tw/fenlei/1_10/" # 11-369
        # link = "https://www.qb5.tw/fenlei/1_370/"
        # novel_topic_id = 1

        # 都市言情
        # novel_topic = "都市言情"
        # # link = "https://www.qb5.tw/fenlei/3_10/" # 11-1299
        # link = "https://www.qb5.tw/fenlei/3_1300/"
        # novel_topic_id = 3

        # 历史军事
        # novel_topic = "历史军事"
        # # link = "https://www.qb5.tw/fenlei/4_10/" # 11-209
        # link = "https://www.qb5.tw/fenlei/4_210/"
        # novel_topic_id = 4

        # 网游竞技
        # novel_topic = "网游竞技"
        # # link = "https://www.qb5.tw/fenlei/5_10/" # 11-89
        # link = "https://www.qb5.tw/fenlei/5_90/"
        # novel_topic_id = 6

        # 科幻灵异
        # novel_topic = "科幻灵异"
        # # link = "https://www.qb5.tw/fenlei/6_10/" # 11-199
        # link = "https://www.qb5.tw/fenlei/6_200/"
        # novel_topic_id = 7

        # 恐怖灵异
        # novel_topic = "恐怖灵异"
        # # link = "https://www.qb5.tw/fenlei/7_10/" # 11-40
        # link = "https://www.qb5.tw/fenlei/7_40/"
        # novel_topic_id = 8

        # 其他类型
        # novel_topic = "其他类型"
        # # link = "https://www.qb5.tw/fenlei/8_10/" # 11
        # link = "https://www.qb5.tw/fenlei/8_540/"
        # novel_topic_id = 9

        yield scrapy.Request(
            url=link,
            meta={'novel_topic': novel_topic, 'novel_topic_id': novel_topic_id},
            callback=self.parse_two
        )

    # 二级解析：遍历页码数
    def parse_page(self, response):
        novel_topic = response.meta['novel_topic']
        novel_topic_id = response.meta['novel_topic_id']
        # <a href="https://www.qb5.tw/fenlei/1_375/" class="last">375</a>
        page_count = response.xpath('//div[@class="pagelink"]/a[@class="last"]/text()').get()
        url = response.url
        for i in range(0, int(page_count)):
            link = url[:-3] + "_" + str((i + 1)) + "/"
            yield scrapy.Request(
                url=link,
                meta={'novel_topic': novel_topic, 'novel_topic_id': novel_topic_id},
                callback=self.parse_two
            )

    # 二级解析：获取主题下小说
    def parse_two(self, response):
        novel_topic = response.meta['novel_topic']
        novel_topic_id = response.meta['novel_topic_id']
        novle_lists = response.xpath('//div[@id="tlist"]/ul[@class="titlelist"]/li')
        for i in novle_lists:
            novel_name = i.xpath('./div[@class="zp"]/a/@title').get()
            link = i.xpath('./div[@class="zp"]/a/@href').get()

            m = re.match(".*/book_(\d+)", link)
            novel_id = m.group(1)
            # print(novel_topic, novel_name, link)
            yield scrapy.Request(
                url=link,
                meta={'novel_topic': novel_topic, 'novel_topic_id': novel_topic_id, 'novel_name': novel_name, 'novel_id': novel_id},
                callback=self.parse_three
            )


    # 三级解析：获取小说章节
    def parse_three(self, response):
        novel_topic = response.meta['novel_topic']
        novel_topic_id = response.meta['novel_topic_id']
        novel_name = response.meta['novel_name']
        novel_id = response.meta['novel_id']

        # 获取章节第一章
        # book_url = response.url
        # chapter_01 = response.xpath("//dt[@class='ttname']/following-sibling::dd[1]")[0]
        # novel_chapter = chapter_01.xpath('./a/text()').get()
        # # 不同网站的章节处理方式不一样，有些是绝对路径，有些是相对路径
        # # 如果是相对路径就需要拼接
        # link = response.url + chapter_01.xpath('./a/@href').get()
        # # print(novel_name, novel_chapter, link)
        #
        # yield scrapy.Request(
        #     url=link,
        #     meta={'novel_topic': novel_topic, 'novel_name': novel_name, 'novel_chapter': novel_chapter, 'book_url': book_url},
        #     callback=self.parse_fuor
        # )

        desc = response.xpath('//*[@id="intro"]/text()').extract()
        cover = response.xpath('//*[@id="picbox"]/div/img/@src').extract_first()
        author = response.xpath('//*[@id="info"]/h1/small/a/text()').extract_first()
        chapterUpdatedAt = response.xpath('//*[@id="info"]/div[1]/text()[2]').extract_first()
        chapterId = response.xpath('//*[@id="info"]/div[1]/a/@href').extract_first()
        chapterTitle = response.xpath('//*[@id="info"]/div[1]/a/text()').extract_first()
        novStatus = response.xpath('//*[@id="info"]/p/span[2]/text()').extract_first()

        chapterId = chapterId.strip(".html")
        #（2020-09-30 14:31）
        a = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
        chapterUpdatedAt = a.findall(chapterUpdatedAt)[0]

        nimage_urls = response.xpath('//*[@id="picbox"]/div/img/@src').extract()
        cdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        txt = ''
        for i in range(len(desc)):
            txt = txt + desc[i] + '<br>'  # strip()去掉首位空格字符，‘\n’换行

        novel = NovelscrapyItem(novId=str(novel_id),
                                name=novel_name,
                                desc=txt,
                                cover=cover,
                                cateId=novel_topic_id,
                                cateName=novel_topic,
                                author=author,
                                views=1024,
                                textNum=0,
                                chapterUpdatedAt=parser.parse(chapterUpdatedAt),
                                chapterId=str(chapterId),
                                chapterTitle=chapterTitle,
                                novStatus=novStatus,
                                status=0,
                                nimage_urls=nimage_urls,
                                createdAt=parser.parse(cdate),
                                updatedAt=parser.parse(cdate))
        yield novel

        # 章节排序
        chapter_list = response.xpath('//dd').extract()
        chapters = extract_chapters(response.url, chapter_list)
        # print(novel_name, chapters)
        book_url = response.url

        for ch in chapters:
            novel_chapter = ch.get("chapter_name")
            # 不同网站的章节处理方式不一样，有些是绝对路径，有些是相对路径
            # 如果是相对路径就需要拼接
            link = ch.get("chapter_url")
            index = ch.get("index")
            yield scrapy.Request(
                url=link,
                meta={'novel_topic': novel_topic, 'novel_name': novel_name, 'novel_id': novel_id, 'novel_chapter': novel_chapter, 'book_url': book_url, 'index': index},
                callback=self.parse_fuor
            )

        # 列表
        # chapter_list = response.xpath('//dd')
        # for i in chapter_list:
        #     novel_chapter = i.xpath('./a/text()').get()
        #     # 不同网站的章节处理方式不一样，有些是绝对路径，有些是相对路径
        #     # 如果是相对路径就需要拼接
        #     link = response.url + i.xpath('./a/@href').get()
        #     yield scrapy.Request(
        #         url=link,
        #         meta={'novel_topic': novel_topic, 'novel_name': novel_name, 'novel_chapter': novel_chapter},
        #         callback=self.parse_fuor
        #     )
    #
    # 四级解析：获取小说内容
    def parse_fuor(self, response):
        novel_topic = response.meta['novel_topic']
        novel_name = response.meta['novel_name']
        novel_id = response.meta['novel_id']
        novel_chapter = response.meta['novel_chapter']
        book_url = response.meta['book_url']
        index = response.meta['index']

        # 章节排序 列表
        novel_chapter = response.xpath('//div[@id="main"]/h1/text()').extract_first()
        html = response.xpath('//div[@id="readbox"]').extract_first()
        content = response.xpath('//div[@id="content"]/text()').extract()
        txt = ''
        for i in range(len(content)):
            # txt = txt + content[i].strip() + '\n'  # strip()去掉首位空格字符，‘\n’换行
            txt = txt + content[i] + '<br>'  # strip()去掉首位空格字符，‘\n’换行
            txt = txt.replace('全本小说网 www.qb5.tw，最快更新', '')  # replace()可以替换不需要的字符串
            txt = txt.replace('最新章节！', '')  # replace()可以替换不需要的字符串

        textNum = len(txt)
        cdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        novelChapter = NovelscrapyDetailItem(chapterId=str(index),
                                             novId=str(novel_id),
                                             chapterNo=int(index),
                                             title=novel_chapter,
                                             desc=txt,
                                             link=response.url,
                                             textNum=textNum,
                                             status=0,
                                             tryViews=0,
                                             createdAt=parser.parse(cdate),
                                             updatedAt=parser.parse(cdate))
        yield novelChapter


        # 获取章节第一章
        # next_chapter = extract_pre_next_chapter(book_url, html)
        # # 获取下一章
        # next_url = next_chapter.get('下一章')
        #
        # yield scrapy.Request(
        #     url=next_url,
        #     meta={'novel_topic': novel_topic, 'novel_name': novel_name, 'novel_chapter': novel_chapter, 'book_url': book_url},
        #     callback=self.parse_fuor)


    def parse_err(self,response):
        self.logger.error('crawl %s fail'%response.url)