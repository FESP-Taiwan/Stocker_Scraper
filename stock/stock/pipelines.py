# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class StockPipeline(object):
    def _init_(self):
        self.client = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root', #not set
            password = '', #not set
            db = '', #not set
            charset = 'utf8'
        )
        self.cur = self.client.cursor    
    def process_item(self, item, spider):
        sql = ("insert into proxyip(ip, port, type) values(%s, %s, %s)")
        lis = (item['ip'],item['item'],item['types'])
        try:
            self.cur.execute(sql, lis)
            self.client.commit()
        except Exception as e:
            print("Insert error: ", e)    
        self.cur.close()
        return item
