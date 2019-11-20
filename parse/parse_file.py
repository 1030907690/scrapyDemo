# -*-coding: UTF-8 -*-
import json
import os

if __name__ == '__main__':
    file_array = ["data/GaoQing.json",
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
                  "data/video.json",
                  "data/WuMa.json",
                  "data/XueSheng.json",
                  "data/YouMa.json",
                  "data/ZhiFu.json",
                  "data/ZhongWenZiMu.json"];

    length = 0;
    for file_item in  file_array:
        file = open("../"+file_item, 'r', encoding='utf-8')
        jsonArr = json.load(file);
        print(file_item+ " ： "+ str(len(jsonArr)))
        length += len(jsonArr)




    print("total number ：" + str(length))
