# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MonthlyincomeItem
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector


class ExampleSpider(scrapy.Spider):
    name = 'monthlyincome'
    def start_requests(self):
        year = 107
        for month in range(1,13):
            qry_str = str(year)+'_'+str(month)
            url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+qry_str+'_0.html'
            yield SplashRequest(url=url,meta={'year':year,'month':month},callback=self.parse, args = {"wait": "3"})
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html.parser') # use lxml will cause error
        alltable = soup.select_one('body > center > center > table')
        if(not alltable): # if no result , return directly
            print("no result")
            return
        tables = alltable.findAll('table')
        item = MonthlyincomeItem()
        #print(soup.text)
        item['year'] = str(response.meta['year'])
        item['month'] = str(response.meta['month'])
        for tab_idx,table in enumerate(tables):
            # print(tab_idx)
            title = table.select_one('tr:nth-of-type(1) > th:nth-of-type(1)').text
            title = title.replace("產業別：","")
            income_type = table.select_one('tr:nth-of-type(1) > th:nth-of-type(2)').text
            income_type = income_type.replace("單位：","")
            print(title)
            item['income_type'] = income_type
            if(table.find("table")):
                for tr_idx,tr in enumerate(table.find("table").findAll("tr")):
                    if(tr.find('th')):
                        continue
                    if(tr_idx > 1 ):
                        for td_idx,td in enumerate(tr.select("td")):
                            if(td_idx==0):
                                item['ticker'] = td.text
                            if(td_idx==1):
                                item['company_name'] = td.get_text().strip()
                                name = td.get_text().strip()
                            if(td_idx==2):
                                item['current_income'] = td.get_text().strip().replace(",","")
                            if(td_idx==3):
                                item['last_income'] = td.get_text().strip().replace(",","")
                            if(td_idx==4):
                                item['last_year_current_income'] = td.get_text().strip().replace(",","")
                            if(td_idx==7):
                                item['current_accumulate_income'] = td.get_text().strip().replace(",","")
                            if(td_idx==8):
                                item['last_year_accumulate_income'] = td.get_text().strip().replace(",","")
                        if(name == ""):
                            continue
                        yield item