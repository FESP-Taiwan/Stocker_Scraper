# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo import MongoClient
from etfingredient import settings
from etfingredient.items import EtfingredientItem

class EtfingredientPipeline(object):
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLLECTION]
    def process_item(self, item, spider):
        if item.__class__ == EtfingredientItem:
            if self.collection.find({"ticker":item['ticker'],"last_crawl_time":item['last_crawl_time']}).count() == 0:
                element = {"ticker":item['ticker'],"ingredient":item['ingredient'],"last_crawl_time":item['last_crawl_time']}
                self.collection.insert_one(element)
            return item