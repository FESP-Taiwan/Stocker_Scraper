# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import DividendItem
from pymongo import MongoClient
import pymongo
from dividend import settings
class ExampleSpider(scrapy.Spider):
    name = 'dividend'
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client['Etfingredient']
        self.collection = self.db['cnyes']
    def start_requests(self):
        tickers = self.collection.find_one({"ticker":"0050"})['ingredient']
        for ticker in tickers:
            ticker = ticker['ticker']
            url = 'https://histock.tw/stock/financial.aspx?no='+ticker+'&t=2'
            yield scrapy.Request(url=url,meta={'ticker':ticker},callback=self.parse)
    def parse(self, response):
        data = response.body
        ticker = response.meta['ticker']
        soup = BeautifulSoup(data, 'html.parser')
        tab = soup.findAll('table')[0]
        item = DividendItem()
        for tr_idx,tr in enumerate(tab.findAll('tr')):
            if(tr_idx > 1):
                item['ticker'] = ticker
                for td_idx,td in enumerate(tr.findAll('td')):
                    if(td_idx==0):
                        item['belongs_year']=td.text
                    if(td_idx==1):
                        item['pay_year']=td.text
                    if(td_idx==2):
                        item['ex_right_date']=td.text
                    if(td_idx==3):
                        item['ex_dividend_date']=td.text
                    if(td_idx==4):
                        item['price_before_dividend']=td.text
                    if(td_idx==5):
                        item['stock_dividend']=td.text
                    if(td_idx==6):
                        item['cash_dividend']=td.text
                yield item