# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/13 15:35
# --------------------------------
import os


def print_directory_contents(sPath):
    """
     这个函数接受文件夹的名称作为输入参数，
     返回该文件夹中文件的路径，
     以及其包含文件夹中文件的路径。

     """
    # 补充代码
    for sChild in  os.listdir(sPath):
        sChildPath = os.path.join(sPath, sChild)
        if os.path.isdir(sChildPath):
            print_directory_contents(sChildPath)
        else:
            print(sChildPath)


print_directory_contents('..')