# -*-coding: UTF-8 -*-
import json
import os
from urllib.parse import urlparse
import requests
import shutil
from parse.Video import *

# 存储的根目录
BASE_PATH = "G:/video/"
# 当前项目路径
PROJECT_DIR = os.getcwd() + "/" + "../"
FFMPEG_DIR = PROJECT_DIR + "ffmpeg-20191120-d73f062-win64-static/"
FFMPEG_BIN_DIR = FFMPEG_DIR + "bin/"
#key的路径
KEY_BASE_PATH = os.getcwd() + "/key/";
KEY_VIDEO_PATH = KEY_BASE_PATH + "video.key";
KEY_INFO_PATH = KEY_BASE_PATH + "videokey.info"

total_length = 0;

data_struct_array = [];

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
    print("parse " + " name [" + name + "]" + " image [" + img + "]" + " url [" + url + " ]" + " type [" + type + "]");

    urlRes = urlparse(url)
    savePath = urlRes.path[1:];
    relativePath = create_relative_path(savePath)
    img_path = download_file_image(relativePath, img)
    fullPath = download_file_m3u8(relativePath, url);
    m3u8_path = transform_mp4_to_m3u8(relativePath, fullPath);
    build_data_struct(name,type,m3u8_path.replace(BASE_PATH,""),img_path.replace(BASE_PATH,""))
    remaining_queue();
    post_process();


def post_process():
    if total_length <= 0:
        json_str = json.dumps(data_struct_array, default=st_to_dict, ensure_ascii=False);  # default参数就是告知json如何进行序列化
        print(json_str)
        if os.path.exists(BASE_PATH + "data.json"):
            os.remove(BASE_PATH + "data.json")
        file = open(BASE_PATH + "data.json", "w", encoding='utf-8')
        file.write(json_str)
        file.close()


def build_data_struct(name,type,relative_path,img):
     video = Video(name,type,relative_path,img);
     data_struct_array.append(video);




'''
mp4转m3u8
ffmpeg -i test.mp4 -c:v libx264 -c:a aac -strict -2 -f hls -hls_time 15 -hls_list_size 0 test.m3u8
or
ffmpeg.exe index.mp4 -c copy -vbsf h264_mp4toannexb  output.ts
ffmpeg -i " + outTsPath + " -c copy -map 0 -f segment -segment_list " + outM3U8StoragePath + " -segment_time 20 " + outTsItmePath


转成m3u8并加密 
ffmpeg -i index.mp4 -c copy -bsf:v h264_mp4toannexb -hls_time 30 -hls_list_size 0 -hls_key_info_file videokey.info output.m3u8
-hls_time 设置每片的时长，默认值为2。单位为秒
-hls_list_size 设置播放列表保存的最多条目，设置为0会保存所有切片信息，默认值为5
'''

def transform_mp4_to_m3u8(relativePath, fullPath):
    outM3U8StorageName = "index.m3u8";
    outM3U8StoragePath = BASE_PATH + relativePath + "/" + outM3U8StorageName;
    #复制key文件
    if os.path.exists(BASE_PATH + relativePath + "/" +"video.key") == False:
        shutil.copy(KEY_VIDEO_PATH,BASE_PATH + relativePath);


    if  os.path.exists(outM3U8StoragePath) == False:
        # 将ts切片加密，并生成m3u8文件
        os.system(FFMPEG_BIN_DIR + "ffmpeg -i "+ fullPath +" -c copy -bsf:v h264_mp4toannexb -hls_time 30 -hls_list_size 0 -hls_key_info_file  " + KEY_INFO_PATH +" " + outM3U8StoragePath)
    else:
        print("Already Storage Path " + outM3U8StoragePath)

    return outM3U8StoragePath;

'''
def transform_mp4_to_m3u8(relativePath, fullPath):
    outM3U8StorageName = "index.m3u8";
    tsName = "output.ts"
    outTsPath = BASE_PATH + relativePath + "/" + tsName
    outM3U8StoragePath = BASE_PATH + relativePath + "/" + outM3U8StorageName;
 
    # 将mp4转为完整的ts
    if os.path.exists(outTsPath):
        print("Already Storage Path " + outTsPath)
    else:
        print(FFMPEG_BIN_DIR + "ffmpeg " + fullPath + " -c copy -vbsf h264_mp4toannexb  " + outTsPath)
        os.system(FFMPEG_BIN_DIR + "ffmpeg -i " + fullPath + " -c copy -vbsf h264_mp4toannexb  " + outTsPath)

    outTsItmePath = BASE_PATH + relativePath + "/" + "output%03d.ts";
    if os.path.exists(outTsPath) and os.path.exists(outM3U8StoragePath) == False:
        # 将ts切片，并生成m3u8文件
        os.system(
            FFMPEG_BIN_DIR + "ffmpeg -i " + outTsPath + " -c copy -map 0 -f segment -segment_list " + outM3U8StoragePath + " -segment_time 30 " + outTsItmePath)
    else:
        print("Already Storage Path " + outM3U8StoragePath + " Or Can't Find " + outTsPath)
'''


'''
剩余任务数
'''


def remaining_queue():
    global total_length;
    total_length -= 1
    print(" remaining number " + str(total_length));

def st_to_dict(v):
    return {'name':v.name,'type':v.type,'relative_path':v.relative_path,"img":v.img}
'''
zhouzhongqing
2019年11月21日12:47:23
创建相对路径
'''


def create_relative_path(path):
    relativePath = path[:path.rfind("/")];
    relativePath = processor_relativePath(relativePath);
    if path is not None and path.strip() != "" and os.path.exists(BASE_PATH + relativePath) == False:
        os.makedirs(BASE_PATH + relativePath)
    return relativePath;


'''
处理相对路径地址
'''


def processor_relativePath(relativePath):
    resultPath = relativePath;
    if relativePath is not None and relativePath.find("http://") >= 0:
        # 如果是http://
        resultPath = relativePath.replace("http://", "");
        resultPath = resultPath[resultPath.find("/") + 1:]
    elif relativePath is not None and relativePath.find("https://") >= 0:
        # 如果是https://
        resultPath = relativePath.replace("https://", "");
        resultPath = resultPath[resultPath.find("/") + 1:]

    return resultPath;


'''
zhouzhongqing
2019年11月21日13:12:53
下载图片
'''


def download_file_image(relativePath, url):
    file_name = url[url.rfind("/"):];

    fullPath = BASE_PATH + relativePath + file_name;
    if os.path.exists(fullPath):
        print("Already Storage Path " + fullPath)
    else:
        r = requests.get(url, timeout=99999);
        with open(fullPath, "wb") as f:
            f.write(r.content)
        f.close()

    return fullPath;

''' 
下载视频文件 返回mp4路径
'''


def download_file_m3u8(relativePath, url):
    storageName = "index.mp4";
    fullPath = BASE_PATH + relativePath + "/" + storageName;
    if os.path.exists(fullPath):
        print("Already Storage Path " + fullPath)
    else:
        print(" Storage Path " + fullPath)
        os.system(
            FFMPEG_BIN_DIR + "ffmpeg" + " -i " + url + " -c copy " + fullPath);

    return fullPath;


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
