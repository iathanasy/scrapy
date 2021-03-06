# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from pymongo import MongoClient

class SavePipeline(object):
    def open_spider(self, spider):
        self.file = open("JD.csv", 'a', newline="", encoding="gb18030")
        self.csv_writer = csv.writer(self.file)
        self.csv_writer.writerow(["标题", "链接", '价格', "评论数", "店铺", "店铺链接"
                                  ])

    def process_item(self, item, spider):
        self.csv_writer.writerow(
            [item["name"], item["link"], item["price"],
             item["comment_num"], item["shop_name"], item["shop_link"]]
        )
        return item

    def close_spider(self, spider):
        self.file.close()


class MongoPipline(object):
    def open_spider(self, spider):
        self.client = MongoClient('127.0.0.1',27017)
        self.db = self.client['JD']
        self.col = self.db['Phone']

    def process_item(self, item, spider):
        data = dict(item)
        self.col.insert(data)
        return item

    def close_spider(self, spider):
        self.client.close()