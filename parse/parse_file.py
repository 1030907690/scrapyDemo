# -*-coding: UTF-8 -*-
import json
import os
from urllib.parse import urlparse
import requests

BASE_PATH = os.getcwd() + "/";
PROJECT_DIR = BASE_PATH + "../"
FFMPEG_DIR = "ffmpeg-20191120-d73f062-win64-static/"
FFMPEG_BIN_DIR = PROJECT_DIR + FFMPEG_DIR + "bin/"

total_length = 0;

'''
zhouzhongqing
2019年11月20日21:24:18
解析m3u8文件
'''


def parse_m3u8_file(item):
    type = item["type"]
    img = item["img"]
    name = item["name"];
    url = item["url"];
    print("parse url [" + url + " ]" + " name [" + name + "]" + " type [" + type + "]");

    urlRes = urlparse(url)
    savePath = urlRes.path[1:];
    relativePath = create_relative_path(savePath)
    download_file_image(relativePath, img)
    download_file_m3u8(relativePath, url);

    global total_length;
    total_length  -= 1

    print("remaining number " + str(total_length));


'''
zhouzhongqing
2019年11月21日12:47:23
创建相对路径
'''
def create_relative_path(path):
    relativePath = path[:path.rfind("/")];
    if path is not None and path.strip() != "" and os.path.exists(relativePath) == False:
        os.makedirs(relativePath)
    return relativePath;


'''
下载图片
'''
def download_file_image(relativePath, url):
    file_name = url[url.rfind("/"):];
    if os.path.exists(BASE_PATH + relativePath + file_name):
        print("Already Storage Path " + BASE_PATH + relativePath + file_name)
    else:
        r = requests.get(url, timeout=99999);
        with open(BASE_PATH + relativePath + file_name, "wb") as f:
            f.write(r.content)
        f.close()


'''
下载视频文件
'''
def download_file_m3u8(relativePath, url):
    storageName = "index.mp4";
    if os.path.exists(BASE_PATH + relativePath + "/" + storageName):
        print("Already Storage Path " + BASE_PATH + relativePath + "/" + storageName)
    else:
        print(" Storage Path " + BASE_PATH + relativePath + "/" + storageName)
        os.system(
            FFMPEG_BIN_DIR + "ffmpeg.exe" + " -i " + url + " -c copy " + BASE_PATH + relativePath + "/" + storageName);


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

    for file_item in file_array:
        file = open("../" + file_item, 'r', encoding='utf-8')
        jsonArr = json.load(file);
        print(file_item + " ： " + str(len(jsonArr)))
        total_length += len(jsonArr)

    print("total number ：" + str(total_length))

    for file_item in file_array:
        file = open("../" + file_item, 'r', encoding='utf-8')
        jsonArr = json.load(file);
        print(file_item + " ： " + str(len(jsonArr)))
        for item in jsonArr:
            parse_m3u8_file(item)
