# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MonthlyincomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ticker = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    income_type = scrapy.Field()
    company_name = scrapy.Field()
    current_income = scrapy.Field()
    last_income = scrapy.Field()
    last_year_current_income = scrapy.Field()
    current_accumulate_income = scrapy.Field()
    last_year_accumulate_income = scrapy.Field()
