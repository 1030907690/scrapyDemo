# -*-coding: UTF-8 -*-
import scrapy
from ..items import *
import os
from scrapyDemo.utils import *
from concurrent.futures import ThreadPoolExecutor


'''
2020年02月07日16:49:16
zhouzhongqing
下载gitblit的项目
'''

# 写死的cookie
COOKIE = "Gitblit=0f78d6b60ecba41158545226fc1e00d09f02dab7; JSESSIONID=p8j2909wo83u5l46wpmh616y"
common = Utils()
host_name = '103.232.84.79:7777'
pool = ThreadPoolExecutor(5)


class DownloadGitblitRepository(scrapy.Spider):
    # 运行 scrapy crawl 800cms
    name = "downloadGitblitRepository"
    allowed_domains = ["103.232.84.79:7777"]
    start_urls = ['http://' + host_name + '/repositories/']
    cookies = TransCookie(COOKIE).stringToDict()

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], cookies=self.cookies,
                             callback=self.parse)

    def cmd(self,command):
        os.chdir("/home/zzq/work/history")
        #subprocess.run(command)
        os.system(command)


    def parse(self, response):
        # print(str(response.body, 'utf-8'))
        table_element = response.xpath("/html/body/div[3]/div[2]/table")
        trs = table_element.xpath('tbody[1]/tr')
        for tr in trs:
            # print(tr.xpath('@class').extract_first())
            if "group" != tr.xpath('@class').extract_first():
                a_href = tr.xpath('td[1]/span[2]/a[1]/@href').extract_first()
                a_href = a_href.replace("%2F","/").replace("..","").replace("/summary","")
                prefix = 'http://zhouzhongqing@' + host_name + '/r'
                print(prefix + a_href)
                pool.submit(self.cmd,("git clone " + prefix + a_href))
