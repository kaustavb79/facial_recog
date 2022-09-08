import cv2
import numpy as np
import urllib.request as ur
from .utils import *
import cv2
import face_recognition
import numpy as np
from datetime import datetime
import pickle


def inference_image(image):
    final_response = []

    with open('resources/api_face_recog/model/dataset_faces.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)

    # Grab the list of names and the list of encodings
    classNames = [list(dct.keys())[0] for dct in all_face_encodings]
    encoded_face_train = np.array([list(dct.values())[0] for dct in all_face_encodings])
    img = face_recognition.load_image_file(image)
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #----------Finding face Location for drawing bounding boxes-------
    faces_in_frame = face_recognition.face_locations(img_rgb)
    print("faces_in_frame -- ",faces_in_frame)
    encoded_faces = face_recognition.face_encodings(img_rgb, faces_in_frame)
    print("encoded_faces: ",encoded_faces)
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        print("matches: ",matches)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        print("faceDist: ",faceDist)
        matchIndex = np.argmin(faceDist)
        print("matchIndex: ",matchIndex)
        # print(matchIndex)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            y1,x2,y2,x1 = faceloc
            final_response.append({
                "class":name,
                "coordinates":{
                    "x_min":x1,
                    "y_min":y1,
                    "x_max":x2,
                    "y_max":y2
                },
                "match":True
            })
    return final_response


def get_face_detect_data(image):
    data = inference_image(image)
    # image_data = img
    return data

