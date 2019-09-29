# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class TickerpoolSpider(scrapy.Spider):
    name = 'tickerpool'

    def start_requests(self):
        url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        yield scrapy.Request(url=url,callback=self.parse)
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'lxml')
        data_table = soup.select_one('table:nth-of-type(2)')

        print(len(data_table.findAll('tr')))
