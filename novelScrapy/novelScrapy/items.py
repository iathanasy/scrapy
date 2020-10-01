# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #
    novId = scrapy.Field()
    # 小说名称
    name = scrapy.Field()
    # 小说描述
    desc = scrapy.Field()
    # 小说封面
    cover = scrapy.Field()
    # 小说分类
    cateId = scrapy.Field()
    # 分类名称
    cateName = scrapy.Field()
    # 小说作者
    author = scrapy.Field()
    # 浏览次数
    views = scrapy.Field()
    # 小说字数
    textNum = scrapy.Field()
    # 小说章节数
    chapterNum = scrapy.Field()
    # 最新章节时间
    chapterUpdatedAt = scrapy.Field()
    # 最新章节id
    chapterId = scrapy.Field()
    # 最新章节标题
    chapterTitle = scrapy.Field()
    #
    collectNum = scrapy.Field()
    #
    recNum = scrapy.Field()
    #
    createdAt = scrapy.Field()
    #
    updatedAt = scrapy.Field()

    # 图片
    nimage_urls = scrapy.Field()
    nimages = scrapy.Field()

class NovelscrapyDetailItem(scrapy.Item):
    #
    chapterId = scrapy.Field()
    # 小说ID
    novId = scrapy.Field()
    # 章节编号
    chapterNo = scrapy.Field()
    # 章节标题
    title = scrapy.Field()
    # 章节内容
    desc = scrapy.Field()
    # 章节采集链接
    link = scrapy.Field()
    # 章节采集站点源
    source = scrapy.Field()
    # 浏览次数
    views = scrapy.Field()
    # 章节字数
    textNum = scrapy.Field()
    # 章节采集状态0正常，1失败
    status = scrapy.Field()
    # 采集重试次数
    tryViews = scrapy.Field()
    #
    createdAt = scrapy.Field()
    #
    updatedAt = scrapy.Field()