import scrapy


class DemoSpiders(scrapy.Spider):
    name = "demo"
    allowed_domains = ["wolongzy.net"]
    base_href = "http://wolongzy.net";
    start_urls = [
        "http://wolongzy.net",
    ]


    def parse(self, response):
        video_list = response.xpath("/html/body/div[5]/ul/li");
        for item in video_list:
            item_video = item.xpath("a[1]/text()");
            item_href = item.xpath("a[1]/@href");
            print("item " + (item_video.extract())[0] +"---" + (item_href.extract())[0])
            demo['name'] = (item_video.extract())[0];
            torrent = ScrapydemoItem()