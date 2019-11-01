# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EtfingredientItem(scrapy.Item):
    # define the fields for your item here like:
    last_crawl_time = scrapy.Field()
    ticker = scrapy.Field()
    ingredient = scrapy.Field()
