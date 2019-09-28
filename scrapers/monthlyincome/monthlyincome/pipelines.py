# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from monthlyincome import settings
from monthlyincome.items import MonthlyincomeItem
from pymongo import MongoClient

class MonthlyincomePipeline(object):
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client[settings.MONGO_DB]
        self.collection = self.db[settings.MONGO_COLLECTION]
        
    def process_item(self, item, spider):
        if item.__class__ == MonthlyincomeItem:   #將不同Item插入不同的資料庫
            if self.collection.find({"year": item['year'],"month": item['month'], "ticker": item['ticker']} ).count() == 0:  #找尋資料是否已經在Mongo
                element={'ticker':item['ticker'], 'year':item['year'], 'month':item['month'], 'income_type':item['income_type'], 'company_name':item['company_name'], 'current_income':item['current_income'], 'last_income':item['last_income'], 'last_year_current_income':item['last_year_current_income'],'current_accumulate_income':item['current_accumulate_income'],'last_year_accumulate_income':item['last_year_accumulate_income']};  #一天的股價與成交量
                self.collection.insert_one(element)  #將資料插入到資料庫
            return item
