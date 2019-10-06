import scrapy
import json
import time
from stockprice.items import StockpriceItem
import datetime
from pymongo import MongoClient
import pymongo
from stockprice import settings
class PriceSpider(scrapy.Spider):
    name = 'stockprice'
    response_json = {}
    def __init__(self):    #連線資料庫，資料庫相關設定值放在settings.py
        self.client = MongoClient(settings.MONGO_STRING)
        self.db = self.client['Etfingredient']
        self.collection = self.db['cnyes']
    def start_requests(self):
        start_date = 2010
        end_date = 2019
        tickers = self.collection.find_one({"ticker":"0050"})['ingredient']
        for ticker in tickers:
            ticker = ticker['ticker']
            for year in range(start_date, end_date+1): 
                str_year = str(year) 
                for month in range(1,13):
                    str_month = str(month)
                    if len(str_month)<2:
                        str_month = '0'+str_month
                    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+ str_year +str_month+'01&stockNo='+ticker
                    yield scrapy.Request(url = url, meta={'ticker':ticker},callback = self.parse)
    def transform_date(self, date):  #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d
    def transform_data(self, data):  #資料格式轉換
        data[0] = datetime.datetime.strptime(self.transform_date(data[0]), '%Y/%m/%d')
        data[1] = int(data[1].replace(',', ''))#把千進位的逗點去除
        data[2] = int(data[2].replace(',', ''))
        data[3] = float(data[3].replace(',', ''))
        data[4] = float(data[4].replace(',', ''))
        data[5] = float(data[5].replace(',', ''))
        data[6] = float(data[6].replace(',', ''))
        data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
        data[8] = int(data[8].replace(',', ''))
        return data
    def transform(self, data):   #取出data的每一列資料進行資料格式轉換
        return [self.transform_data(d) for d in data]
    def parse(self, response):
        data_src = json.loads(response.body_as_unicode()) 
        # print(soup.text)
        item = StockpriceItem()
        if(data_src["stat"]!= 'OK'):
            print("URL: " + response.request.url) 
            return
        datas = self.transform(data_src['data'])
        for d in datas:
            item['date'] = d[0]         #資料與item結合，會傳到pipeline進行處理
            item['stockno'] = response.meta['ticker']
            item['shares'] = d[1]
            item['amount'] = d[2]
            item['open'] = d[3]
            item['close'] = d[4]
            item['high'] = d[5]
            item['low'] = d[6]
            item['diff'] = d[7]
            item['turnover'] = d[8]
            yield item
             