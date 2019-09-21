from ..items import FinancereportItem
import scrapy
import time
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import pymongo
class reportSpider(scrapy.Spider):
    name = 'financereport'
    DEBUG = False
    mongo_db = "Report"
    BS_DB = "BalanceSheet"
    CI_DB = "ComprehensiveIncom"
    CF_DB = "CashFlow"
    client = pymongo.MongoClient("mongodb+srv://py_scrapy:scrapy@balancesheetreport-wo30d.mongodb.net/test?retryWrites=true&w=majority")
    def start_requests(self):
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
        }
        ticker = 2891
        start_year = 2013
        end_year = 2013
        for year in range(start_year,end_year+1): # 2013 is the api limit
            for season in range(1,4+1):
                url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID='+str(ticker)+'&SYEAR='+str(year)+'&SSEASON='+str(season)+'&REPORT_ID=C'
                yield scrapy.Request(url=url,callback=self.parse,meta={'year':year,'season':season,"ticker":ticker},headers=headers)
    def BalanceSheet_parser(self,soup):
        table = 'table:nth-of-type(1) > '
        date = soup.select_one(table+"tr:nth-of-type(2) > th:nth-of-type(3) > span.en").text
        tables = soup.findAll('table')
        tab = tables[0]
        json = {'code':'N/A','report_date':date}
        for tr in tab.findAll('tr'):
            ifrs_key = ''
            ifrs_value = ''
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    code = td.getText()
                    json['code'] = code
                if(idx==1):
                    ifrs_key = td.select('span.zh')[0].text
                    ifrs_key = ifrs_key.replace('\u3000','')
                if(idx==2):
                    ifrs_value = td.getText()
            if(json['code']!='N/A'):
                json[ifrs_key] = ifrs_value
                if self.DEBUG:
                    print(json)
        return json
    def BalanceSheet_parser_two(self,soup):
        tables = soup.findAll('table')
        tab = tables[1]
        json = {'code':'N/A','report_date':tab.find_all('tr')[0].select_one('th:nth-of-type(2)').text}
        for tr in tab.findAll('tr'):
            ifrs_key = ''
            ifrs_value = ''
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    ifrs_key = td.getText()
                    ifrs_key = ifrs_key.replace('\u3000','')
                if(idx==1):
                    ifrs_value = td.getText().strip()
            if(ifrs_key!=''):
                json[ifrs_key] = ifrs_value
                if self.DEBUG:
                    print(json)
        return json
    def ComprehensiveIncom_parser(self,soup):
        table = 'table:nth-of-type(2) > '
        date = soup.select_one(table+"tr:nth-of-type(2) > th:nth-of-type(3) > span.en").text
        tables = soup.findAll('table')
        tab = tables[1]
        json = {'code':'N/A','report_date':date}
        for tr in tab.findAll('tr'):
            ifrs_key = ''
            ifrs_value = ''
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    code = td.getText()
                    json['code'] = code
                if(idx==1):
                    ifrs_key = td.select('span.zh')[0].text
                    ifrs_key = ifrs_key.replace('\u3000','')
                if(idx==2):
                    ifrs_value = td.getText()
            if(json['code']!='N/A'):
                json[ifrs_key] = ifrs_value
                if self.DEBUG:
                    print(json)
        return json
        
    def ComprehensiveIncom_parser_two(self,soup):
        tables = soup.findAll('table')
        tab = tables[2]
        ifrs_key = ''
        ifrs_value = ''
        json = {'code':'N/A','report_date':tab.find_all('tr')[0].select_one('th:nth-of-type(2)').text}
        for tr in tab.findAll('tr'):
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    ifrs_key = td.getText()
                    ifrs_key = ifrs_key.replace('\u3000','')
                if(idx==1):
                    ifrs_value = td.getText().strip()
            if(ifrs_key!=''):
                json[ifrs_key] = ifrs_value
                if self.DEBUG:
                    print(json)
        return json
        
    def CashFlow_parser(self,soup):
        table = 'table:nth-of-type(3) > '
        date = soup.select_one(table+"tr:nth-of-type(2) > th:nth-of-type(3) > span.en").text
        tables = soup.findAll('table')
        tab = tables[2]
        json = {'code':'N/A','report_date':date}
        for tr in tab.findAll('tr'):
            ifrs_key = ''
            ifrs_value = ''
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    code = td.getText()
                    json['code'] = code
                if(idx==1):
                    ifrs_key = td.select('span.zh')[0].text
                    ifrs_key = ifrs_key.replace('\u3000','')
                if(idx==2):
                    ifrs_value = td.getText()
            if(json['code']!='N/A'):
                json[ifrs_key] = ifrs_value
                if self.DEBUG:
                    print(json)
        return json
        
    def CashFlow_parser_two(self,soup):
        tables = soup.findAll('table')
        tab = tables[3]
        ifrs_key = ''
        ifrs_value = ''
        json = {'code':'N/A','report_date':tab.find_all('tr')[0].select_one('th:nth-of-type(2)').text}
        for tr in tab.findAll('tr'):
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    ifrs_key = td.getText()
                    ifrs_key = ifrs_key.replace('\u3000','')
                if(idx==1):
                    ifrs_value = td.getText().strip()
            if(ifrs_key!=''):
                json[ifrs_key] = ifrs_value
                if self.DEBUG:
                    print(json)
        return json
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html.parser')
        year = str(response.meta['year'])
        season = str(response.meta['season'])
        ticker = str(response.meta['ticker'])
        temp_json = {'year':year,'season':season,'ticker':ticker}
        if(len(soup.find_all('table'))<3):
            print('no data in '+year)
            return
        if year == '2019':
            bs_json = self.BalanceSheet_parser(soup)
            ci_json = self.ComprehensiveIncom_parser(soup)
            cf_json = self.CashFlow_parser(soup)
        else :
            bs_json = self.BalanceSheet_parser_two(soup)
            ci_json = self.ComprehensiveIncom_parser_two(soup)
            cf_json = self.CashFlow_parser_two(soup)
            
        print('%s season (%s) is successfully been crawled'%(year,season))
        bs_json.update(temp_json)
        ci_json.update(temp_json)
        cf_json.update(temp_json)
        self.client[self.mongo_db][self.BS_DB].insert_one(bs_json)
        self.client[self.mongo_db][self.CI_DB].insert_one(ci_json)
        self.client[self.mongo_db][self.CF_DB].insert_one(cf_json)