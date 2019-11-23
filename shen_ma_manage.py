# -*-coding: UTF-8 -*-
import os
from scrapy.cmdline import execute

if os.path.exists("video.json"):
   os.remove("video.json")
execute('scrapy crawl shen_ma_collection -o video.json'.split())
'''
if __name__ == '__main__':
    os.system("scrapy crawl shen_ma_collection")
'''
