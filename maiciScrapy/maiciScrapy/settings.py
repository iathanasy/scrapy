# -*- coding: utf-8 -*-


BOT_NAME = 'maiciScrapy'

SPIDER_MODULES = ['maiciScrapy.spiders']
NEWSPIDER_MODULE = 'maiciScrapy.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
  'Host': 'www.ailinglei.com',
}

ITEM_PIPELINES = {
   'maiciScrapy.pipelines.MaiciscrapyPipeline': 300
}


""" mongo配置 """
MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DATABASE='maici_scrapy'
REPLICASET = ''

""" scrapy-redis配置 """
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 配置调度器是否要持久化, 也就是当爬虫结束了, 要不要清空Redis中请求队列和去重指纹的set。如果是True, 就表示要持久化存储, 就不清空数据, 否则清空数据
SCHEDULER_PERSIST = True

# 指定redis数据库的连接参数
REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_PARAMS ={
    'password': 'redis',  # 服务器的redis对应密码
}