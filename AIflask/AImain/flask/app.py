from flask import Flask, request
from flask_cors import CORS

import numpy as np
import face_recognition
import os

# DB
import pymysql

# 이미지 읽기
import cv2
import requests

app = Flask(__name__)
CORS(app)



 
## 저장된 db에 url 가져오기
def getEmps():
    ret = []
    db = pymysql.connect(host='localhost', user='ssafy', db='common_pjt', password='ssafy', charset='utf8')
    curs = db.cursor()
    
    sql = "select img from imgAi";
    curs.execute(sql)
    
    rows = curs.fetchall()
    for e in rows:
        # temp = {'img':e[0] }
        ret.append(e[0])
    
    db.commit()
    db.close()
    return ret


##### 여기가 이미지 불러오고 하는 곳
dir_path = './img/'


# def get_cropped_face(image_file):
    
#     # url을 이미지 파일로 읽기
#     # image_nparray = np.asarray(bytearray(requests.get(image_file).content), dtype=np.uint8)
#     # imdeimage = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR) 

#     # 원래 코드
#     image = face_recognition.load_image_file(image_file)    # 이미지 불러오기
#     face_locations = face_recognition.face_locations(image)   # 얼굴 영역 박스 
#     a, b, c, d = face_locations[0]     # 얼굴 영역 박스 좌표
#     cropped_face = image[a:c,d:b,:]    # 얼굴 영역 박스 좌표를 이용해 얼굴 잘라내기 
#     return cropped_face # 이미지 파일


# def get_face_embedding(face):
#     return face_recognition.face_encodings(face)  # FaceNet 얼굴 임베딩 모델 이용





# v2 => 이미지  불러오고 변환하기
def get_cropped_face(image_file):
    #image = face_recognition.load_image_file(image_file)    # 이미지 불러오기
    image_nparray = np.asarray(bytearray(requests.get(image_file).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR) 
    # print(image)
    face_locations = face_recognition.face_locations(image)   # 얼굴 영역 박스 
    a, b, c, d = face_locations[0]     # 얼굴 영역 박스 좌표
    cropped_face = image[a:c,d:b,:]    # 얼굴 영역 박스 좌표를 이용해 얼굴 잘라내기 
    return cropped_face # 이미지 파일

dir_path = './img/'

def get_face_embedding(face):
    return face_recognition.face_encodings(face)

def get_face_embedding_dict(dir_path):
    # 원래 코드
    # file_list = os.listdir(dir_path)

    # DB에서 가져온 코드
    file_list = getEmps()

    embedding_dict = {}
    
    for file in file_list:
        #  원래 코드
        # img_path = os.path.join(dir_path, file) # 경로를 병합하여 새 경로 생성
        
        # 추가
        img_path = file

        try: 
            face = get_cropped_face(img_path)    # 얼굴 영역만 자른 이미지
        except:                                  # 인식하지 못하는 이미지는 넘어감
            continue
            
        embedding = get_face_embedding(face)   # 얼굴 영역에서 얼굴 임베딩 벡터를 추출
        if len(embedding) > 0:   # 얼굴 영역이 제대로 detect되지 않았을 경우를 대비
                    # os.path.splitext(file)[0]에는 이미지파일명에서 확장자를 제거한 이름이 담긴다. 
                namearr = os.path.splitext(file)[0].split('/')
                # print(namearr[-1])
                embedding_dict[namearr[-1]] = embedding[0]
    
    # print(embedding_dict) # 여기까지 됨
    return embedding_dict







## 잘 돌아가는 코드
# def get_cropped_face(image_file):
#     image = face_recognition.load_image_file(image_file)    # 이미지 불러오기
#     face_locations = face_recognition.face_locations(image)   # 얼굴 영역 박스 
#     a, b, c, d = face_locations[0]     # 얼굴 영역 박스 좌표
#     cropped_face = image[a:c,d:b,:]    # 얼굴 영역 박스 좌표를 이용해 얼굴 잘라내기 
#     return cropped_face # 이미지 파일

# dir_path = './img/'

# def get_face_embedding(face):
#     return face_recognition.face_encodings(face)

# def get_face_embedding_dict(dir_path):
#     file_list = os.listdir(dir_path)
#     embedding_dict = {}
    
#     for file in file_list:
#         img_path = os.path.join(dir_path, file) # 경로를 병합하여 새 경로 생성
#         try: 
#             face = get_cropped_face(img_path)    # 얼굴 영역만 자른 이미지
#         except:                                  # 인식하지 못하는 이미지는 넘어감
#             continue
            
#         embedding = get_face_embedding(face)   # 얼굴 영역에서 얼굴 임베딩 벡터를 추출
#         if len(embedding) > 0:   # 얼굴 영역이 제대로 detect되지 않았을 경우를 대비
#                     # os.path.splitext(file)[0]에는 이미지파일명에서 확장자를 제거한 이름이 담긴다. 
#                 embedding_dict[os.path.splitext(file)[0]] = embedding[0]
       
#     return embedding_dict













embedding_dict = get_face_embedding_dict(dir_path)

# 거리순 비교하는 것
def get_distance(name1, name2):

    return np.linalg.norm(embedding_dict[name1]-embedding_dict[name2], ord=2)

def get_sort_key_func(name1):         # name1은 미리 지정
    def get_distance_from_name1(name2):      # name2는 호출시에 인자로 받는다.
        return get_distance(name1, name2)
    return get_distance_from_name1

def get_nearest_face(name, top= 3):
    # 잘 나옴
    
    sort_key_func = get_sort_key_func(name)  
    # print(sort_key_func)
    # key=lambda x:sort_key_func(x[0])
    # print(key)

    sorted_faces = sorted(embedding_dict.items(), key=lambda x:sort_key_func(x[0]))   # 얼굴 임베딩 딕셔너리를 오름차순으로 정렬
    # print(sorted_faces)
    arr = ['0']*4
    
    for i in range(top+1):
        #   if i == 0:
        #       continue
          if sorted_faces[i]:
                # print('{}: {}'.format(i,len(sorted_faces[i][0])))
                print('순위 {} : 이름({}) , 거리({})'. format(i, sorted_faces[i][0], sort_key_func(sorted_faces[i][0])))
                arr[i] = '순위 {} : 이름({}), 거리({})'. format(i, sorted_faces[i][0], sort_key_func(sorted_faces[i][0]))
    return arr




@app.route('/pp', methods=['GET'])
def ajax():
    # print(get_face_embedding_dict('https://beauduckai.s3.ap-northeast-2.amazonaws.com/diamond2'))
    # print(embedding_dict['https://beauduckai.s3.ap-northeast-2.amazonaws.com/diamond2'])
    ans = get_nearest_face('kimgo')

    # ans = get_nearest_face('team7')
    # print(ans)
    
    return {'answer': ans}
    

if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=False)