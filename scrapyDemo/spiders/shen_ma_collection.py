# -*-coding: UTF-8 -*-
from ..items import *
import json
import os

'''
神马资源采集
'''
base_href = "https://www.smzy9.tv"



class ShenMaCollection(scrapy.Spider):
    # 运行 scrapy crawl shen_ma_collection
    name = "shen_ma_collection"
    allowed_domains = ["www.smzy9.tv"]
    start_urls = [
        "https://www.smzy9.tv/index.php/vod/type/id/1/page/1.html"
        "https://www.smzy9.tv/index.php/vod/type/id/2/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/3/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/4/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/5/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/6/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/7/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/8/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/25/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/26/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/27/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/28/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/29/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/30/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/31/page/1.html",
        "https://www.smzy9.tv/index.php/vod/type/id/32/page/1.html"
    ]

    #def start_requests(self):

    def parse(self, response):
        #print("body " + str(response.body))
        ul_list = response.xpath("//ul[@class='nr']");
        for item_ul in ul_list:
            item_video = item_ul.xpath("li/span[2]/a[1]/text()").extract()[0]
            item_href = item_ul.xpath("li/span[2]/a[1]/@href").extract()[0];
            item_type = item_ul.xpath("li/span[3]/text()").extract()[0];
            item_videoType = item_ul.xpath("li/span[3]/text()").extract()[0];
            updateTime = item_ul.xpath("li/span[1]/text()").extract()[0];
            torrent = ScrapydemoItem()
            torrent['name'] = item_video;
            torrent['url'] = base_href + item_href;
            torrent['type'] = item_type;
            torrent['videoType'] = item_videoType;
            torrent['updateTime'] = updateTime;
            #yield torrent;
            yield scrapy.Request(base_href + item_href, callback=self.parse_video_detail)


        #拿到最大的页数
        max_page = response.xpath("//div[@id='page2']/a[9]/@href").extract_first();
        next_page = response.xpath("//div[@id='page2']/a[8]/@href").extract_first();
        current_page = response.xpath("//div[@id='page2']/text()").extract_first();
        current_page = current_page[current_page.find(":")+1:current_page.rfind("/")]
        print("max_page " + str(max_page))
        if max_page is not None:
            max_page_number = max_page[max_page.rfind("/")+1:].replace(".html","");
            print(str(current_page) + " max_page_number " + str(max_page_number))
            if int(current_page) < int(max_page_number):
                yield scrapy.Request(base_href + next_page,callback=self.parse)
        else:
            print("最大页数异常")


    def parse_video_detail(self,response):
        video_list = response.xpath("//div[@class=\"vodplayinfo\"]");
        url = "";
        for item in video_list:
            h3_text = item.xpath("div[1]/h3[1]/text()").extract_first();
            if h3_text is not None:
                #print("h3_text " + h3_text)
                if h3_text.find("m3u8") >= 0:
                    url = item.xpath("div[1]/ul[1]/li[1]/input[1]/@value").extract_first().replace("在线播放$","")

        torrent = VideoDetail()
        torrent['name'] = response.xpath("//div[@class=\"vodh\"]/h3[1]/text()").extract_first().strip();
        torrent['url'] = url;
        torrent['type'] =  response.xpath("//div[@class=\"vodInfo\"]/a[1]/text()").extract()[1].replace("分类：","");
        torrent['updateTime'] = response.xpath("//div[@class=\"vodInfo\"]/a[7]/text()").extract()[1].replace("更新时间：", "");
        torrent['img'] = response.xpath("//div[@class='vodImg']/img[1]/@src").extract_first();
        yield torrent