from financereport.items import FinancereportItem
import scrapy
import time
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
class reportSpider(scrapy.Spider):
    name = 'financereport'
    def start_requests(self):
        url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2891&SYEAR=2019&SSEASON=3&REPORT_ID=C'
        yield scrapy.Request(url=url,callback=self.parse)
    def BalanceSheet_parser(self,soup):
        table = 'table:nth-of-type(1) > '
        date = soup.select_one(table+"tr:nth-of-type(2) > th:nth-of-type(3) > span.en").text
        tables = soup.findAll('table')
        tab = tables[0]
        returnList = []
        for tr in tab.findAll('tr'):
            json = {'code':'','ifrs_key':'N/A','ifrs_value':'N/A','report_date':date}
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    code = td.getText()
                    json['code'] = code
                if(idx==1):
                    ifrs_key = td.select('span.zh')[0].text
                    ifrs_key = ifrs_key.replace('\u3000','')
                    json['ifrs_key'] = ifrs_key
                if(idx==2):
                    ifrs_value = td.getText()
                    json['ifrs_value'] = ifrs_value
            if(json['code']!=''):
                returnList.append(json)
                print(json)
        return returnList
    def ComprehensiveIncom_parser(self,soup):
        table = 'table:nth-of-type(2) > '
        date = soup.select_one(table+"tr:nth-of-type(2) > th:nth-of-type(3) > span.en").text
        tables = soup.findAll('table')
        tab = tables[1]
        returnList = []
        for tr in tab.findAll('tr'):
            json = {'code':'','ifrs_key':'N/A','ifrs_value':'N/A','report_date':date}
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    code = td.getText()
                    json['code'] = code
                if(idx==1):
                    ifrs_key = td.select('span.zh')[0].text
                    ifrs_key = ifrs_key.replace('\u3000','')
                    json['ifrs_key'] = ifrs_key
                if(idx==2):
                    ifrs_value = td.getText()
                    json['ifrs_value'] = ifrs_value
            if(json['code']!=''):
                returnList.append(json)
                print(json)
        return returnList
    def CashFlow_parser(self,soup):
        table = 'table:nth-of-type(2) > '
        date = soup.select_one(table+"tr:nth-of-type(2) > th:nth-of-type(3) > span.en").text
        tables = soup.findAll('table')
        tab = tables[2]
        returnList = []
        for tr in tab.findAll('tr'):
            json = {'code':'','ifrs_key':'N/A','ifrs_value':'N/A','report_date':date}
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    code = td.getText()
                    json['code'] = code
                if(idx==1):
                    ifrs_key = td.select('span.zh')[0].text
                    ifrs_key = ifrs_key.replace('\u3000','')
                    json['ifrs_key'] = ifrs_key
                if(idx==2):
                    ifrs_value = td.getText()
                    json['ifrs_value'] = ifrs_value
            if(json['code']!=''):
                returnList.append(json)
                print(json)
        return returnList
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html.parser')
        #ComprehensiveIncom = soup.select_one("table:nth-of-type(2)")
        #CashFlow = soup.select_one("table:nth-of-type(3)")
        if(len(soup.find_all('table'))==0):
            print('no data')
            return
        print("BS")
        bs_list = self.BalanceSheet_parser(soup)
        print("ci")
        ci_list = self.ComprehensiveIncom_parser(soup)
        print("cf")
        cf_list = self.CashFlow_parser(soup)
        