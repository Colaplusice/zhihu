# encoding=utf-8
from pymongo import mongo_client
from datetime import datetime, timedelta
import pickle
import zlib

# from bson.binary import  Binary
# from playground import Link_crawler
max_length = 255


class Mongo_cache:
    """
    将数据存放在MongoDb中
    数据库名称:zhihu
    表名称:message
    """
    def __init__(self, client=None,expired_time=timedelta(days=30)):
        self.client = mongo_client.MongoClient('localhost', 27017) if client is None else client
        # if client.cache is not Non
        self.db = self.client.zhihu
        # 创建时间戳index  过期后mongodb会自动删除

        self.db.message.create_index('timestamp', expireAfterSeconds=expired_time.total_seconds())
        self.expired_time = expired_time

        # 如果现在的时间比 当时时间戳和过期天数大，就return true 表示过期了
    # def has_expaired(self,timestamp):
    #     return datetime.utcnow()>timestamp+self.expired_time

    def __setitem__(self, url, result):
        # result为dict类型 包括 url code html 三个属性
        # 将result 转换为pickle 然后压缩后传入数据库
        record = {'result': result, 'timestamp': datetime.utcnow()}
        try:
        # 插入
            self.db.message.update({'_id': url}, {'$set': record}, upsert=True)
        except:
            print("数据库插入出现错误")

    def get_all_message(self):
        list=[i for i in self.db.message.find()]
        return list




    def __getitem__(self, url):
        # record 类似于一个字典
        record = self.db.message.find_one({'_id': url})
        # 从数据库中把压缩的信息取出来，然后反序列化
        if record:
            return record
        else:
            raise KeyError(url + '不存在')

    def drop_data(self):
        self.db.zhihu.drop()


class Mongo_html_cache:
    """
    将数据存放在MongoDb中
    数据库名称:zhihu
    表名称:message
    """
    def __init__(self, client=None,expired_time=timedelta(days=30)):
        self.client = mongo_client.MongoClient('localhost', 27017) if client is None else client
        # if client.cache is not Non
        self.db = self.client.zhihu
        # 创建时间戳index  过期后mongodb会自动删除

        self.db.html_message.create_index('timestamp', expireAfterSeconds=expired_time.total_seconds())
        self.expired_time = expired_time

        # 如果现在的时间比 当时时间戳和过期天数大，就return true 表示过期了

    # def has_expaired(self,timestamp):
    #     return datetime.utcnow()>timestamp+self.expired_time

    def __setitem__(self, url, result):
        # result为dict类型 包括 url code html 三个属性
        # 将result 转换为pickle 然后压缩后传入数据库
        record = {'result': result, 'timestamp': datetime.utcnow()}
        try:
        # 插入
            self.db.html_message.update({'_id': url}, {'$set': record}, upsert=True)
        except:
            print("数据库插入出现错误")

    def __getitem__(self, url):
        # record 类似于一个字典
        record = self.db.html_message.find_one({'_id': url})
        # 从数据库中把压缩的信息取出来，然后反序列化
        if record:
            return record
        else:
            raise KeyError(url + '不存在')

    def drop_data(self):
        self.db.zhihu.drop()
