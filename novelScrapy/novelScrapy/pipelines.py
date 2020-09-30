# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from .items import NovelscrapyItem


class NovelscrapyPipeline:

    def __init__(self, mongo_uri, mongo_db,replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'novel_scrapy'),
            replicaset = crawler.settings.get('REPLICASET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        if isinstance(item,NovelscrapyItem):
            self._process_novel_item(item)
        else:
            self._process_novel_chapter_item(item)
        return item



    def _process_novel_item(self,item):
        '''
        处理小说信息
        :param item:
        :return:
        '''
        self.db.novel.insert(dict(item))





    def _process_novel_chapter_item(self,item):
        '''
        处理小说详情
        :param item:
        :return:
        '''
        self.db.novel_chapter.insert(dict(item))
