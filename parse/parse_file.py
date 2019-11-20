# -*-coding: UTF-8 -*-
import json
import os
import requests
from urllib.parse import urlparse
import shutil
'''
zhouzhongqing
2019年11月20日21:24:18
解析m3u8文件
'''


def parse_m3u8_file(item):
    url = item["url"];
    print("parse " + url);

    urlRes = urlparse(url)
    savePath = urlRes.path[1:];
    download_file(savePath, url);
    for line in open(savePath):
        print("----"+line)


def download_file(path, url):
    #os.path.exists(path)
    r = requests.get(url, timeout=99999);
    with open(path, "wb") as f:
        f.write(r.content)
    f.close()


if __name__ == '__main__':
    file_array = ["data/GaoQing.json"]
    '''
    "data/GuoChan.json",
    "data/HEYZO.json",
    "data/JuRu.json",
    "data/KaTong.json",
    "data/LingLei.json",
    "data/LuanLun.json",
    "data/OuMei.json",
    "data/RenQi.json",
    "data/RiHan.json",
    "data/SanJi.json",
    "data/TouPaiZiPai.json",
    "data/WuMa.json",
    "data/XueSheng.json",
    "data/YouMa.json",
    "data/ZhiFu.json",
    "data/ZhongWenZiMu.json"];
'''
    length = 0;
    for file_item in file_array:
        file = open("../" + file_item, 'r', encoding='utf-8')
        jsonArr = json.load(file);
        print(file_item + " ： " + str(len(jsonArr)))
        length += len(jsonArr)
        for item in jsonArr:
            parse_m3u8_file(item)

    print("total number ：" + str(length))
