#!/usr/bin/python

import os
from scrapy.cmdline import execute
if os.path.exists("video.json"):
    os.remove("video.json")
execute('scrapy crawl 800cms -o video.json'.split())