# -*-coding: UTF-8 -*-
from ..items import *
import json
import os

base_href = "http://800zy12.com"


class CmsVideoDetailSpiders(scrapy.Spider):
    # 运行 scrapy crawl 800cms
    name = "800cms_detail"
    allowed_domains = ["800zy12.com"]
    start_urls = []

    '''

    contents = "";
    with open('video.json', encoding='utf-8') as file_obj:
        contents = file_obj.read()

    print(contents)
    jsonArr = json.loads(contents);
    for item in jsonArr:
        print(item["url"])
    '''
    if os.path.exists('video.json'):
        file = open('video.json', 'r', encoding='utf-8')
        jsonArr = json.load(file);
        for item in jsonArr:
            print(item["url"])
            start_urls.append(item["url"])

    def parse(self, response):
        print("body " + str(response.body))
        video_name = response.xpath("//p[@class='whitetitle']/text()").extract()[0];
        type = response.xpath("//div[@class='right']/p[1]/a[1]/text()").extract()[0];
        updateTime = response.xpath("//div[@class='right']/p[2]/text()").extract()[0];
        url = response.xpath("//div[@class='playlist wbox']/text()").extract()[0];
        img = response.xpath("//div[@class='left']/img[1]/@src").extract()[0];

        torrent = VideoDetail()
        torrent['name'] = video_name.replace("影片名称：", "").strip();
        torrent['url'] = url;
        torrent['type'] = type;
        torrent['updateTime'] = updateTime.replace("更新时间：", "");
        torrent['img'] = img;
        yield torrent;