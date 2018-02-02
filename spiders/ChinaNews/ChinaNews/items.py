# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_link = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    pubtime = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    html_content = scrapy.Field()
    # editor = scrapy.Field()
    image = scrapy.Field()
    tag = scrapy.Field()
    classification = scrapy.Field()

