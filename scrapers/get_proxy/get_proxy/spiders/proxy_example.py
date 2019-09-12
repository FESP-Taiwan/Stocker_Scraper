# -*- coding: utf-8 -*-
import scrapy
from lxml.html import fromstring
from bs4 import BeautifulSoup
import json
class ProxyExampleSpider(scrapy.Spider):
    name = 'proxy_example'
    #allowed_domains = ['www.us-proxy.org']
    start_urls = ['https://free-proxy-list.net/']
    def proxy_check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']
        #print(proxy_ip,json.loads(response.text)['origin'])
        if proxy_ip == json.loads(response.text)['origin']:
            whiteList = {
                'scheme': response.meta['_proxy_scheme'],
                'proxy': response.meta['proxy'],
                'port': response.meta['port']
            }
            print(whiteList)
            yield {
                'scheme': response.meta['_proxy_scheme'],
                'proxy': response.meta['proxy'],
                'port': response.meta['port']
            }
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        #print(soup)
        trs = soup.select("#proxylisttable tr")
        for tr in trs:
            tds = tr.select("td")
            if len(tds) > 3:
                ip = tds[0].text
                port = tds[1].text
                isScheme = tds[6].text
                anonymouty = tds[4].text
                if isScheme == 'yes':
                    scheme = 'https'
                else:
                    scheme = 'http'
                proxy = "%s://%s:%s"%(scheme, ip, port)
                meta = {
                    'port': port,
                    'proxy': proxy,
                    'dont_retry': True,
                    'download_timeout': 5,
                    '_proxy_scheme': scheme,
                    '_proxy_ip': ip
                }
                #if anonymouty == 'anonymous':
                    #print(meta)
                yield scrapy.Request('https://httpbin.org/ip', callback=self.proxy_check_available, meta=meta, dont_filter=True)

