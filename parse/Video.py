# -*-coding: UTF-8 -*-

'''
视频对象
'''
#类定义
class Video:
    #定义基本属性
    name = ''
    type = ''
    relative_path = ''
    img = ''

    #定义构造方法
    def __init__(self,name,type,relative_path,img):
        self.name = name
        self.type = type
        self.relative_path = relative_path
        self.img = img
