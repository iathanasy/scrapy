# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from scrapy.exceptions import DropItem

class CnblogspiderPipeline:
    def __init__(self):
        writepath = 'data/papers.json'
        self.file = open(writepath, 'w', encoding="utf-8")
    def process_item(self, item, spider):
        if item['title']:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            print(line)
            self.file.write(line)
            return item
        else:
            raise DropItem("Missing title in %s" % item)




class CnblogspiderMongoPipeline:

    collection_name = 'scrapy_items'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item