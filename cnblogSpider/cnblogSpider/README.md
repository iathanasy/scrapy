### scrapy-redis分布式

#### 12.2-scrapy-redis基本使用

安装：sudo pip3 install scrapy-redis

下载源代码：git clone http://github.com/rolando/scrapy-redis.git

可以把下载的 scrapy-redis 项目中src下面的 `scrapy_redis` 文件夹拷贝到项目中

scrapy redis 中常用的主键：

```python
# 最重要的主键，在settings.py文件中设置的

#1.必须，使用了scrapy_redis的去重组件，在redis数据库中做去重
DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter"
#2.必须，使用了scrapy_redis的调度器，在redis里分配请求
SCHEDULER="scrapy_redis.scheduler.Scheduler"
#3.可选，在redis中保持scrapy_redis用到的各个队列，从而True允许暂停和暂停后恢复，也就是不清理reidis queues
SCHEDULER_PERSIST = True
#4.必选，通过配置RedisPipeline将item写入key为spider.name:items的redis的list中，供后面的分布式处理item，这个已经由scrapy—redis实现，不需要我们写代码，直接使用即可
ITEM_PIPELINES = {
'scrapy_redis.pipelines.RedisPipeline':100
}
#5.必须，指定redis数据库的连接参数
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379
REDIS_PARAMS ={
    'password': 'redis',  # 服务器的redis对应密码
}
```

##### 第一种方法：

官方案例中的配置：pipelines.py

```python
# 在pipelines.py文件中的设置，官方已经写好的，不用修改
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
```

官方案例中的配置：settings.py

```python
# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'


#  负责执行request去重（必须设置的）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#  对请求进行调度（必须设置的）
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#  默认去掉用过的url(可选)，保存调度器的队列，断电继续
SCHEDULER_PERSIST = True

#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

# （必须设置的）
ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,  # 把数据写入到ridis数据库中，可以自己在pipelines种自己写调取的数据库存储
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

REDIS_HOST = 'localhost'
REDIS_PORT=6379
```

官方案例中的配置：dmoz.py

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy

# class DmozSpider(CrawlSpider):

class DmozSpider(scrapy.Spider):
    """Follow categories and extract links."""
    # 只是说明 redis的持续性
    name = 'dmoz'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com/']  # 用百度测试

    def parse(self, response):

        urls = response.xpath('//a/@href').extract()

        yield{
            'title': response.xpath('//title/text()').extract()[0],
            'url': response.url
        }
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)


# 如果只是用到redis的去重和存储   可以用第一种
# 如果要写分布式的话可以用第二种或第三种
# 第二种和第三种的区别就是spider和crawlspidre的区别
```

设置完成，启动爬虫后，在服务器上进入redis数据库中查看

```python
连接成功
zpl@pyvip:~$ redis-cli  # 进入数据库
127.0.0.1:6379> keys *  # 查看字段
1) "ng-scrapy:requests"
2) "myspider:start_urls"
3) "ng-scrapy:dupefilter"
4) "dmoz:dupefilter"   # 去重的数据
5) "myspider_redis:items"
6) "dmoz:items"     # 数据类型   
7) "dmoz:requests"
127.0.0.1:6379> type dmoz:items   # 查看类型
list
127.0.0.1:6379>LRANGE dmoz:items 0 10   # 在redis中查看list数据
 1) "{\"url\": \"http://www.baidu.com/\", \"spider\": \"dmoz\", \"title\": \"\\u767e\\u5ea6\\u4e00\\u4e0b\\uff0c\\u4f60\\u5c31\\u77e5\\u9053\", \"crawled\": \"2019-10-01 13:29:57\"}"   # 这是一条数据。
127.0.0.1:6379> del ng-scrapy:requests   # 删除队列
(integer) 1
127.0.0.1:6379> del myspider:start_urls  # 删除队列
(integer) 1
127.0.0.1:6379> del ng-scrapy:dupefilter  # 删除队列
(integer) 1
127.0.0.1:6379> type dmoz:requests
zset
127.0.0.1:6379> ZRANGE dmoz:requests 0 10  # 查看zset型的数据
1)"\x80\x04\x95\x02\x01\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04body\x94C\x00\x94\x8c\x04meta\x94}\x94\x8c\x05depth\x94K\x03s\x8c\x06method\x94\x8c\x03GET\x94\x8c\aerrback\x94N\x8c\bpriority\x94K\x00\x8c\x05flags\x94]\x94\x8c\bcallback\x94\x8c\x05parse\x94\x8c\x0bdont_filter\x94\x89\x8c\x03url\x94\x8c/http://v.baidu.com/show/list/order-pubtime+pn-1\x94\x8c\t_encoding\x94\x8c\x05utf-8\x94\x8c\acookies\x94}\x94\x8c\aheaders\x94}\x94C\aReferer\x94]\x94C\x17http://v.baidu.com/show\x94asu."
```

scrapy_redis框架：

官方文档中有三种方法：

第一种方法dmoz.py文件中，说明redis持续性。也就是第一次运行爬虫关掉后会有记录，再次开启会接着爬。

运行爬虫后，在服务器中查看：

redis-cli

输入：keys  *

第一种形式继承scrapy.Spider（或CrawlSpider）类

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy

# class DmozSpider(CrawlSpider): # 官方文档中的第一种方法CrawlSpider
class DmozSpider(scrapy.Spider):
    """Follow categories and extract links."""
    # 只是说明 redis的持续性
    name = 'dmoz'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):

        urls = response.xpath('//a/@href').extract()

        yield{
            'title': response.xpath('//title/text()').extract()[0],
            'url': response.url
        }
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

```

```python
zpl@pyvip:~/aliyun/爬虫高级/scrapy-redis/example-project$ redis-cli
127.0.0.1:6379> keys *
1) "dmoz:items"
127.0.0.1:6379> type dmoz:items   # 查看数据类型
list
127.0.0.1:6379> LRANGE dmoz:items 0 10  #在redis数据空中怎么查看数据类型
1) "{\"url\": \"http://www.baidu.com/\", \"spider\": \"dmoz\", \"title\": \"\\u767e\\u5ea6\\u4e00\\u4e0b\\uff0c\\u4f60\\u5c31\\u77e5\\u9053\", \"crawled\": \"2019-10-01 13:29:57\"}"
127.0.0.1:6379> keys *
1) "dmoz:dupefilter"   # 去重了
2) "dmoz:items"
127.0.0.1:6379> del name   # 在redis数据库中删除name
127.0.0.1:6379> keys *
1) "dmoz:dupefilter" # 去重了
2) "dmoz:requests"  # 请求队列
3) "dmoz:items"
127.0.0.1:6379> type dmoz:requests
zset
127.0.0.1:6379> ZRANGE dmoz:requests 0 10  # 查看zset类型的数据内容
        
127.0.0.1:6379> LRANGE dmoz:items 0 10  # 查看list类型数据
127.0.0.1:6379> SMEMBERS dmoz:dupefilter  # 查看set类型数据
```

##### 第二种方法：

官方案例中的配置：myspider_redis.py

继承RedisSpider类，需要动态的设置url，默认是没有start_urls方法的。

启动爬虫后需要给他一个起点，也就是入口url

```python
from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'  # 比第一种多了 redis_key,少了 start_urls
    # start_urls

# 这种需要动态的设置url
    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
```

```python
# 启动爬虫后在redis段设置url

# 动态设置url方法：

127.0.0.1:6379> lpush myspider:start_urls https://www.baidu.com  # 设置url后爬虫就会向下运行
(integer) 1   
127.0.0.1:6379> lpush myspider:start_urls https://www.jd.com   # 设置url后爬虫就会向下运行
(integer) 1   
```



第二种方法的变种：

也可以自己写，去掉redis_key = 'myspider:start_urls'

```python
from scrapy_redis.spiders import RedisSpider
import scrapy


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    #redis_key = 'myspider:start_urls'

    def start_requests(self):    # 用这个方法添加url
        urls = ['https://www.baidu.com']
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)
           
    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
```

##### 第三种方法：

官方案例中的配置：myspider_redis.py

```python
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'mycrawler_redis'
    redis_key = 'mycrawler:start_urls'

    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MyCrawler, self).__init__(*args, **kwargs)

    def parse_page(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }

```

如果只是用到redis的去重和存储   可以用第一种

如果要写分布式的话可以用第二种或第三种

第二种和第三种的区别就是spider和crawlspidre的区别

scrapy-redis源码介绍

1.scrapy-redis/src/connection.py     负责跟进seetings的配置  进行实例化redis链接

2.scrapy-redis/src/defaults.py   #  显示的名字    重点理解

3.scrapy-redis/src/dupefilter.py  # 复制去重的

4.scrapy-redis/src/picklecompat.py  # 序列化的   

5.scrapy-redis/src/pipelines.py  # redispipeline类，方法

6.scrapy-redis/src/queue.py  #队列   pop方法，push方法   重点理解

```python
class LifoQueue(Base):
    """Per-spider LIFO queue."""

    def __len__(self):
        """Return the length of the stack"""
        return self.server.llen(self.key)

    def push(self, request):   # 存入一个url
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self, timeout=0):   # 在队列里取一个url
        """Pop a request"""
        if timeout > 0:   # 判断url是否是一个字典
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)

        if data:
            return self._decode_request(data)
```

7.scrapy-redis/src/scheduler.py  #负责调度的

8.scrapy-redis/src/spiders.py  #

9.scrapy-redis/src/utils.py  #



scrapy-redis 中redis键名介绍

1. “项目名：items”

   list类型，保存爬虫获取到的数据item，内容是json字符串

2. “项目名：dupefilter”

   set类型，用于爬虫访问的url去重，内容是40个字符串的url的hash字符串

3. “项目名：start_urls”

   list类型，用于获取spider启动时爬取的第一个url

4. “项目名：requests”

   zset类型，用于scheduler调度处理requests，内容是request对象的序列化字符串

#### 12.3-scrapy-redis案例

解析网页的方法：  xpath  ， bs4   ，re

xpath： 用来解析结构化页面

re ： 用来解析非结构化页面

创建爬虫后需要用redis去重的话，需要修改的地方：

1.settings.py文件中：

```python
# 添加内容
# 1.指定scrapy-redis的scheduler
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# 2.在redis中保持scrapy-redis用到的队列
SCHEDULER_PERSIST = True

# 3.去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 4.redis 链接信息
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
```

2.在qiancheng.py文件中：

```python
# 导入redis
from scrapy_redis.spiders import RedisSpider

# calss QianchengSpider(spider.Spider)
class QianchengSpider(RedisSpider):
    name = 'qiancheng'
    allowed_domains = ['51job.com']
	redis_key = 'qiancheng:start_urls'
	# 把start_urls换成  redis_key
	# start_urls = ['https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,1.html']

```

3.在redis中输入url，后再启动爬虫

```python
127.0.0.1:6379> lpush qiancheng:start_urls https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,1.html
(integer) 1
127.0.0.1:6379> LRANGE qiancheng:start_urls 0 10   # 查看数据 是空的
(empty list or set)

```

mongo  使用方法：

```python
zpl@pyvip:~$ mongo    # 查看mongo是否安装
MongoDB shell version: 2.6.10
connecting to: test
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
        http://docs.mongodb.org/
Questions? Try the support group
        http://groups.google.com/group/mongodb-user
        
> show databases
admin  (empty)
local  0.078GB

> use nong
switched to db nong
> db.items.findOne()  # 查看数据
null
> db.items.count() # 查看数据条数
0
> 

```

```python
# 在文件pipelines中重写这个函数，调用Mongo的方法
class MongospiderPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['nong']
        self.connection = self.db['items']

    def process_item(self, item, spider):
        data = dict(item)
        self.connection.insert(data)
        return item
```

