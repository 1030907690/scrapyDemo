# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    videoType = scrapy.Field()
    updateTime = scrapy.Field()



class VideoDetail(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    updateTime = scrapy.Field()




