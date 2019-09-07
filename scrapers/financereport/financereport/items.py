# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class FinancereportItem(scrapy.Item):
    # define the fields for your item here like:
    balanceSheet_list = scrapy.Field()
    comprehensiveIncom_list = scrapy.Field()
    cashFlow_list = scrapy.Field()
    pass
