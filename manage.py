#!/usr/bin/python

from scrapy.cmdline import execute
execute('scrapy crawl 800cms -o video.json'.split())
#execute('scrapy crawl 800cms_detail'.split())