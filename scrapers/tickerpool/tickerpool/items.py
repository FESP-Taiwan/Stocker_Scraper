# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TickerpoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ticker = scrapy.Field()
    ticker_type = scrapy.Field()
    name = scrapy.Field()
    isin_code = scrapy.Field()
    listed_date = scrapy.Field()
    market_type = scrapy.Field()
    industry_type = scrapy.Field()
    cfi_code = scrapy.Field()
    last_crawl_time = scrapy.Field()