from pymongo import MongoClient

def get_db():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['faces']
  return db


def get_collection(db):
  face_table = db['face_infos']
  return face_table

def insert_multi_docs(db, info):
    # 批量插入documents,插入一个数组
    face_table = db['face_infos']
    
    faceInfo_id = face_table.insert(info)
    print (faceInfo_id )


