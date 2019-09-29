# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from stockprice import settings
from stockprice.items import StockpriceItem
from pymongo import MongoClient

class StockpricePipeline(object):
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLLECTION]
        
    def process_item(self, item, spider):
        if item.__class__ == StockpriceItem:   #將不同Item插入不同的資料庫
            if self.collection.find({"date": item['date'], "stockno": item['stockno']} ).count() == 0:  #找尋資料是否已經在Mongo
                element={'date':item['date'], 'stockno':item['stockno'], 'shares':item['shares'], 'amount':item['amount'], 'open':item['open'], 'close':item['close'], 'high':item['high'], 'low':item['low'], 'diff':item['diff'], 'turnover':item['turnover']};  #一天的股價與成交量
                self.collection.insert_one(element)  #將資料插入到資料庫
            return item