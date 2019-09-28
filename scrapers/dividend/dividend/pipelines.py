# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from dividend import settings
from dividend.items import DividendItem
from pymongo import MongoClient

class DividendPipeline(object):
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLLECTION]
        
    def process_item(self, item, spider):
        if item.__class__ == DividendItem:   #將不同Item插入不同的資料庫
            if self.collection.find({"belongs_year": item['belongs_year'],"pay_year": item['pay_year'], "ticker": item['ticker']} ).count() == 0:  #找尋資料是否已經在Mongo
                element={'ticker':item['ticker'], 'belongs_year':item['belongs_year'], 'pay_year':item['pay_year'], 'ex_right_date':item['ex_right_date'], 'ex_dividend_date':item['ex_dividend_date'], 'price_before_dividend':item['price_before_dividend'], 'stock_dividend':item['stock_dividend'], 'cash_dividend':item['cash_dividend']};  #一天的股價與成交量
                self.collection.insert_one(element)  #將資料插入到資料庫
            return item