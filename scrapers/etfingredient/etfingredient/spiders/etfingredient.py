# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from ..items import EtfingredientItem
class EtfingredientSpider(scrapy.Spider):
    name = 'etfingredient'
    
    def start_requests(self):
        ticker = "0050"
        url = 'https://www.cnyes.com/twstock/Etfingredient/'+ticker+'.html'
        yield scrapy.Request(url = url, meta={'ticker':ticker},callback = self.parse)
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data,'lxml')
        tables = soup.findAll('table')
        item = EtfingredientItem()
        item['ticker'] = response.meta['ticker']
        item['last_crawl_time'] = datetime.now().strftime("%Y-%m-%d")
        ingredient = []
        for table in tables:
            for tr in table.findAll('tr'):
                if(tr.find('a')):
                    name = tr.find('a').text.strip()
                    ratio = tr.select_one('td:nth-of-type(2)').text.strip()
                    ticker = tr.find('a').get("href").split("/")[3].replace('.htm','')
                    ingredient.append({"name":name,"ratio":ratio,"ticker":ticker})
        item['ingredient'] = ingredient
        yield item
                    
