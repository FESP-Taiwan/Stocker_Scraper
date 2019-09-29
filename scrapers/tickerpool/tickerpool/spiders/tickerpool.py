# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from ..items import TickerpoolItem
from bs4 import BeautifulSoup
from datetime import datetime
class TickerpoolSpider(scrapy.Spider):
    name = 'tickerpool'

    def start_requests(self):
        url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        yield SplashRequest(url,callback=self.parse,args={'wait': '10'})#default method is GET
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'lxml')
        data_table = soup.select_one('table:nth-of-type(2)')
        item = TickerpoolItem()
        item['last_crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for tr_idx,tr in enumerate(data_table.findAll('tr')):
            if(tr_idx > 0):
                if(tr.find('b')):
                    item['ticker_type'] = tr.get_text().strip()
                    continue
                #print(len(list(tr.findAll('td'))))
                for td_idx,td in enumerate(tr.findAll('td')):
                    if(td_idx==0):
                        item['ticker'],item['name'] = td.get_text().split("　")
                    if(td_idx==1):
                        item['isin_code'] = td.get_text().strip()
                    if(td_idx==2):
                        item['listed_date'] = td.get_text().strip()
                    if(td_idx==3):
                        item['market_type'] = td.get_text().strip()
                    if(td_idx==4):
                        item['industry_type'] = td.get_text().strip()
                    if(td_idx==5):
                        item['cfi_code'] = td.get_text().strip()
                yield item
