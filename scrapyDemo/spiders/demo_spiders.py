import scrapy
from ..items import *

base_href = "http://wolongzy.net";

class DemoSpiders(scrapy.Spider):
    #运行 scrapy crawl demo
    name = "demo"
    allowed_domains = ["wolongzy.net"]
    start_urls = []
    for index in range(1,657):
        start_urls.append("http://wolongzy.net/?page="+ str(index))




    def parse(self, response):
        video_list = response.xpath("/html/body/div[5]/ul/li");
        for item in video_list:
            item_video = item.xpath("a[1]/text()");
            item_href = item.xpath("a[1]/@href");
            item_type = item.xpath("span[1]/text()").extract()[0];
            item_videoType = item.xpath("span[2]/text()").extract()[0];
            updateTime = item.xpath("span[3]/text()").extract()[0];
            torrent = ScrapydemoItem()
            torrent['name'] = (item_video.extract())[0];
            torrent['url'] = base_href + (item_href.extract())[0];
            torrent['type'] = item_type;
            torrent['videoType'] = item_videoType;
            torrent['updateTime'] = updateTime;
            yield torrent;