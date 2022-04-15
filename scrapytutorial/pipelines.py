# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):
    """
    处理 Item 数据
    """
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0, self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoDBPipeline(object):
    """
    操作 MongoDB 数据库
    """
    def __init__(self, connection_string, database):
        self.connection_string = connection_string
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        """
        一个类方法, 用于获取 setting.py 中的配置信息
        :param crawler:
        :return:
        """
        return cls(
            connection_string=crawler.setting.get('MONGODB_CONNECTION_STRING'),
            database=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        """
        当 Spider 被开启时, 该方法被调用, 进行一些初始化操作
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        """
        执行数据库的插入操作
        :param item:
        :param spider:
        :return:
        """
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """
        当 Spider 被关闭时, 该方法被调用, 关闭数据库
        :param spider:
        :return:
        """
        self.client.close()
