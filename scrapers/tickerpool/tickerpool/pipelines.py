# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from tickerpool import settings
from tickerpool.items import TickerpoolItem
from pymongo import MongoClient

class TickerpoolPipeline(object):
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLLECTION]
        
    def process_item(self, item, spider):
        if item.__class__ == TickerpoolItem:   #將不同Item插入不同的資料庫
            if self.collection.find({"ticker": item['ticker'],"isin_code": item['isin_code'], "cfi_code": item['cfi_code']} ).count() == 0:  #找尋資料是否已經在Mongo
                element={'ticker':item['ticker'], 'ticker_type':item['ticker_type'], 'name':item['name'], 'isin_code':item['isin_code'], 'listed_date':item['listed_date'], 'market_type':item['market_type'], 'industry_type':item['industry_type'], 'cfi_code':item['cfi_code'],'last_crawl_time':item['last_crawl_time']};  #一天的股價與成交量
                self.collection.insert_one(element)  #將資料插入到資料庫
            return item
