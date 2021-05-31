import os
from pathlib import Path

import cv2
import face_recognition
import hnswlib
import numpy as np
import torch
from extractor import extractor
import pymongo
from db import *
# 线下建图
# 加载提取的特征，建图



    

def main():
  file_path = Path('E:/2-JOB/联想小新/简历项目2/web-face/static/images/casia/pt1')
  index_path = 'index.bin'
  # 提取特征, 顺便返回文件名
  features, failed, img_paths = extractor(file_path)


  # 建立索引
  p = hnswlib.Index(space='l2', dim=128)
  p.init_index(max_elements=500000, ef_construction=100, M=50)
  p.set_ef(100)
  p.set_num_threads(4)
  labels_index = np.arange(len(features))

  p.add_items(features, labels_index)
  p.save_index(index_path)
  info = "{} elements are built successfully,{} failed,cuz we didn't get their feature".format(len(p.get_ids_list()) - failed,failed)
  print(info)
  
  # 就差数据库了，把img的路径和id存到数据库里
  if(len(img_paths) != len(labels_index)):
    print('error, img num !== labels num')
    return

  info = [{"id": str(labels_index[i]), 'path': img_paths[i]} for i in range(len(img_paths))]
  db = get_db()
  insert_multi_docs(db, info)



if __name__ == '__main__':
  main()
