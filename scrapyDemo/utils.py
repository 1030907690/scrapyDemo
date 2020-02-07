# -*-coding: UTF-8 -*-
import pymongo

import os
import jieba
import shutil
from scrapy.utils.project import get_project_settings
'''
一些常量和公共方法
'''
class Utils():
    # 项目前缀
    PROJECT_PATH_PREFIX = os.getcwd()


    def conn_mongo(self):
        self.client = pymongo.MongoClient(self.get_config("MONGO_DB_URI"))
        self.db = self.client[self.get_config("MONGO_DB_NAME")]
        return  self.db;


    def close_mongo(self):
        self.client.close()

    def del_folder(self,path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path);
                print("remove " + path);
            else:
                shutil.rmtree(path)  # 递归删除文件夹
                print("removedirs " + path);

        else:
            print(" not path" + path);

    # 创建文件夹
    def create_folder(self,path):
        if os.path.exists(path) == False:
            os.makedirs(path)

    def execCmd(self,command):
        r = os.popen(command)
        text = r.read()
        r.close()
        print(text)
        return text


    def get_config(self,key,def_value=''):
        '''
        获取配置
        :param key:
        :param def_value:
        :return:
        '''
        settings = get_project_settings()
        value = settings.get(key)
        if value:
            return value
        else:
            return def_value

        # 切分标签
    def cut_tags(self, tags):
        if tags:
            return list(jieba.cut(tags))
        else:
            return None

    def list_file(slef,path,file_list=[]):
        PHOTO_FILE_SUFFIX = slef.get_config("PHOTO_FILE_SUFFIX")
        '''
        文件列表
        :param file_list:
        :return:
        '''
        for item in os.listdir(path):
            if os.path.isfile(path + item):
                if (path + item).rfind(PHOTO_FILE_SUFFIX) < 0:
                    file_list.append(path + item)
                    print("find "+path + item)
            elif os.path.isdir(path + item):
                 slef.list_file(path + item+"/",file_list)





class TransCookie:
    '''
    对cookie分割
    '''
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


class RequestFaced():
    url = ''