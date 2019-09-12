from financereport.items import FinancereportItem
import scrapy
import time
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
class reportSpider(scrapy.Spider):
    name = 'financereport'
    DEBUG = False
    def start_requests(self):
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
        }
        end_year = 2019
        for year in range(2013,end_year+1): # 2013 is the api limit
            for season in range(1,4+1):
                url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=2891&SYEAR='+str(year)+'&SSEASON='+str(season)+'&REPORT_ID=C'
                yield scrapy.Request(url=url,callback=self.parse,meta={'year':year},headers=headers)
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
                if self.DEBUG:
                    print(json)
        return returnList
    def BalanceSheet_parser_two(self,soup):
        tables = soup.findAll('table')
        tab = tables[1]
        returnList = []
        for tr in tab.findAll('tr'):
            json = {'code':'N/A','ifrs_key':'N/A','ifrs_value':'N/A','report_date':tab.find_all('tr')[0].select_one('th:nth-of-type(2)').text}
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    ifrs_key = td.getText()
                    ifrs_key = ifrs_key.replace('\u3000','')
                    json['ifrs_key'] = ifrs_key
                if(idx==1):
                    ifrs_value = td.getText().strip()
                    json['ifrs_value'] = ifrs_value
            if(json['ifrs_key']!='N/A'):
                returnList.append(json)
                if self.DEBUG:
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
                if self.DEBUG:
                    print(json)
        return returnList
    def ComprehensiveIncom_parser_two(self,soup):
        tables = soup.findAll('table')
        tab = tables[2]
        returnList = []
        for tr in tab.findAll('tr'):
            json = {'code':'N/A','ifrs_key':'N/A','ifrs_value':'N/A','report_date':tab.find_all('tr')[0].select_one('th:nth-of-type(2)').text}
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    ifrs_key = td.getText()
                    ifrs_key = ifrs_key.replace('\u3000','')
                    json['ifrs_key'] = ifrs_key
                if(idx==1):
                    ifrs_value = td.getText().strip()
                    json['ifrs_value'] = ifrs_value
            if(json['ifrs_key']!='N/A'):
                returnList.append(json)
                if self.DEBUG:
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
                if self.DEBUG:
                    print(json)
        return returnList
    def CashFlow_parser_two(self,soup):
        tables = soup.findAll('table')
        tab = tables[3]
        returnList = []
        for tr in tab.findAll('tr'):
            json = {'code':'N/A','ifrs_key':'N/A','ifrs_value':'N/A','report_date':tab.find_all('tr')[0].select_one('th:nth-of-type(2)').text}
            for idx,td in enumerate(tr.findAll('td')):
                if(idx==0):
                    ifrs_key = td.getText()
                    ifrs_key = ifrs_key.replace('\u3000','')
                    json['ifrs_key'] = ifrs_key
                if(idx==1):
                    ifrs_value = td.getText().strip()
                    json['ifrs_value'] = ifrs_value
            if(json['ifrs_key']!='N/A'):
                returnList.append(json)
                if self.DEBUG:
                    print(json)
        return returnList
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html.parser')
        year = response.meta['year']
        bs_list = []
        ci_list = []
        cf_list = []
        if(len(soup.find_all('table'))<3):
            print('no data in '+str(year))
            return
        if str(year) == '2019':
            bs_list = self.BalanceSheet_parser(soup)
            ci_list = self.ComprehensiveIncom_parser(soup)
            cf_list = self.CashFlow_parser(soup)
        else :
            bs_list = self.BalanceSheet_parser_two(soup)
            ci_list = self.ComprehensiveIncom_parser_two(soup)
            cf_list = self.CashFlow_parser_two(soup)
            
        print(str(year)+' is successfully been crawled')