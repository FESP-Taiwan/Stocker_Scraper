# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DividendItem(scrapy.Item):
    # define the fields for your item here like:
    ticker = scrapy.Field()
    belongs_year = scrapy.Field()
    pay_year = scrapy.Field()
    ex_right_date = scrapy.Field()
    ex_dividend_date = scrapy.Field()
    price_before_dividend = scrapy.Field()
    stock_dividend = scrapy.Field()
    cash_dividend = scrapy.Field()
