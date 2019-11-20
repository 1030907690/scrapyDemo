# -*-coding: UTF-8 -*-
import scrapy
from ..items import *
import os

base_href = "http://800zy12.com"


class CmsSpiders(scrapy.Spider):
    # 运行 scrapy crawl 800cms
    name = "800cms"
    allowed_domains = ["800zy12.com"]
    start_urls = []
    #类型
    video_type = 6;
    #+1页
    maxPage = 57;


    for index in range(1, maxPage):
        start_urls.append("http://800zy12.com/list-" + str(video_type) + "-" + str(index) + ".html")

    def parse(self, response):
        # print("body " +str(response.body))
        # video_list = response.xpath("//ul[@class='videoContent']");
        video_list = response.xpath("//ul[@class='videoContent']/li");
        print(str(video_list) + "-------------")
        for item in video_list:
            item_video = item.xpath("a[1]/text()").extract()[0]
            item_href = item.xpath("a[1]/@href").extract()[0];
            item_type = item.xpath("span[1]/text()").extract()[0];
            item_videoType = item.xpath("span[2]/text()").extract()[0];
            updateTime = item.xpath("span[3]/text()").extract()[0];
            torrent = ScrapydemoItem()
            torrent['name'] = item_video;
            torrent['url'] = base_href + item_href;
            torrent['type'] = item_type;
            torrent['videoType'] = item_videoType;
            torrent['updateTime'] = updateTime;
            yield torrent;
