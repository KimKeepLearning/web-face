import os
from pathlib import Path

import cv2
import face_recognition
import hnswlib
import numpy as np
import torch


def extractor(files_list):
    count = 0
    #print('==================extracting features==============================')
    features = []
    img_paths = []

    for root, dirs, files, in os.walk(files_list):
      for file in files:
        imgpath =os.path.join(root, file)
        img = cv_imread(imgpath)
        if(len(img.shape)!=3): continue

        img_paths.append(imgpath)
        tmp_feature = face_recognition.face_encodings(face_image=img, known_face_locations=None, num_jitters=1)
        
        if len(tmp_feature) == 0:
            tmp_feature.append([0 for i in range(128)])
            count+=1
        
        tmp_feature = np.array(tmp_feature)
        features.append(tmp_feature[0])
      print(root + ' has been extracted')

    features = np.array(features)
    return features,count, img_paths

def extractSingleImage(imgpath):
  #print('==================extracting features==============================')
  features = []

  img = cv_imread(imgpath)
  tmp_feature = face_recognition.face_encodings(face_image=img, known_face_locations=None, num_jitters=1)
  
  if len(tmp_feature) == 0:
      tmp_feature.append([0 for i in range(128)])
      
  tmp_feature = np.array(tmp_feature)
  features.append(tmp_feature[0])
  features = np.array(features)
  return features




def cv_imread(file_path):
  cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8),-1)
  return cv_img