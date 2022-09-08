import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle

def extract_images_from_videos(folder_name,video_file):
    resources = "resources/api_face_recog/model"
    if "train" not in os.listdir(resources):
        os.mkdir(os.path.join(resources,'train'))
    
    train_folder = os.path.join(resources,'train',folder_name)
    if folder_name not in os.listdir(os.path.join(resources,'train')):
        os.mkdir(train_folder)

    # cap = cv2.VideoCapture(video_file)
    # time_skips = float(500) #skip every 2 seconds. You need to modify this
    # count = 0
    # success,image = cap.read()
    # while success:
    #     cv2.imwrite(os.path.join(train_folder,"frame%d.jpg") % count, image)     
    #     cap.set(cv2.CAP_PROP_POS_MSEC,(count*time_skips))    # move the time
    #     success,image = cap.read()
    #     count += 1
    # # release after reading    
    # cap.release()

    # ----- COUNTER WISE EXTRACT ----
    vidcap = cv2.VideoCapture(video_file)
    every_n_frame = 0.25
    fps = vidcap.get(cv2.CAP_PROP_FPS) #This is frame per second
    print("fps: ",fps)
    after_n_frame = int(every_n_frame * fps)
    success, image = vidcap.read()
    count = 0
    counter = 0
    while success:
        if count % after_n_frame == 0:
            cv2.imwrite(os.path.join(train_folder,"frame%d.jpg") % count, image)
            counter += 1
        success, image = vidcap.read()
        count += 1

    return train_folder

def train(data_path):
    encoded_face_train = []

    def findEncodings(images):
        img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        return encoded_face

    mylist = os.listdir(data_path)
    for cl in mylist:
        curImg = cv2.imread(f'{data_path}/{cl}')
        class_name = data_path.split("/")[-1]
        if "\\" in data_path:
            class_name = data_path.split("\\")[-1]
        try:
            encoded_face_train.append({class_name:findEncodings(curImg)})
        except:
            print("NO encoding found!!! ")

    with open('resources/api_face_recog/model/dataset_faces.dat', 'ab') as f:
        pickle.dump(encoded_face_train, f)

