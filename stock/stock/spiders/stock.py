import scrapy
import json
import time


class PriceSpider(scrapy.Spider):
    name = 'stock'
    response_json = {}
   
    def start_requests(self):
        for year in range(2014, 2016): 
            str_year = str(year) 
            for month in range(1,13):
                str_month = str(month)
                if len(str_month)<2:
                    str_month = '0'+str_month
                url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+ str_year +str_month+'01&stockNo=2330'
                yield scrapy.Request(url = url, callback = self.parse)
    def parse(self, response):
        data = response.body
        json_data = json.loads(data) 
        # print(soup.text)
        if(json_data["stat"]!= 'OK'):
            print("URL: " + response.request.url) 
            return
        for data in json_data["data"]:
            daily_json = {  "日期":"",
                        "成交股數":"",
                        "成交金額":"",
                        "開盤價":"",
                        "最高價":"",
                        "最低價":"",
                        "收盤價":"",
                        "漲跌價差":"",
                        "成交筆數":"" 
                }
            daily_json['日期'] = data[0]
            daily_json['成交股數'] = data[1]
            daily_json['成交金額'] = data[2]
            daily_json['開盤價'] = data[3]
            daily_json['最高價'] = data[4]
            daily_json['最低價'] = data[5]
            daily_json['收盤價'] = data[6]
            daily_json['漲跌價差'] = data[7]
            daily_json['成交筆數'] = data[8]
            print(daily_json)
             