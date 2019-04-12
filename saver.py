from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from pymongo import MongoClient

database = PostgresqlExtDatabase(
    database="zhihu_spider", user="fjl2401", host="127.0.0.1", port="5432"
)


class ZhihuSaver(Model):
    class Meta:
        database = database

    def save_to_database(self):
        pass


class ZhihuMongoSaver:
    def __init__(self):
        self.client = MongoClient()
