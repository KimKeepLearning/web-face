import os
from pathlib import Path

import cv2
import face_recognition
import hnswlib
import numpy as np
import torch
from extractor import extractor
from db import *

def add2Index(indexPath, imgDir):
  feature_dim = 128
  max_elements=500000

  p = hnswlib.Index(space='l2', dim=feature_dim) 
  p.load_index(indexPath, max_elements=max_elements)
  elements_num = len(p.get_ids_list())
  
  # 提取特征
  features, failed, img_paths = extractor(imgDir)

  # 添加到索引中
  labels_index = np.arange(elements_num, elements_num + len(features))
  p.add_items(features, labels_index)
  p.save_index(indexPath)
  #print('{} adding finished!,{} failed'.format(len(features) - failed,failed))
  msg= '{} are added successfully, {} failed, cuz we didn\'t get their features'.format(len(features) - failed,failed)

  # 就差数据库了，把img的路径和id存到数据库里
  if(len(img_paths) != len(labels_index)):
    print('error, img num !== labels num')
    return

  info = [{"id": str(labels_index[i]), 'path': img_paths[i]} for i in range(len(img_paths))]
  db = get_db()
  insert_multi_docs(db, info)

  print(msg)
  return msg, len(features)

if __name__ == '__main__':
  imgDir = "E:/2-JOB/联想小新/简历项目2/web-face/static/images/casia/pt10"
  add2Index('index.bin', imgDir)
