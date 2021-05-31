'''
1. 从node接收文件名

2. 提取这个图片的特征

3. 用hnsw找到对应的id

4. 根据id找到文件名

5. 发送文件名到node端
'''
import cv2
import hnswlib
from extractor import extractSingleImage
import sys
import json
def search(img_path, k=20):
  feature_dim = 128
  max_elements = 500000


  p = hnswlib.Index(space='l2', dim=feature_dim)
  p.load_index('index.bin', max_elements=max_elements)

  #print('==================k-nn search==================================')
  # path = image_path
  # cv_img = cv2.imread(path)
  search_feature = extractSingleImage(img_path)
  labels, distances = p.knn_query(search_feature, k=20)

  return labels[0] # 返回图片对应的id


imgPath = sys.argv[1]
searchResLabels = search(imgPath)
print(searchResLabels)

# j = json.loads(sys.argv[1])
# print(j)

# imgPath = input()
# searchResLabels = search(imgPath)
# print(searchResLabels.tolist())








