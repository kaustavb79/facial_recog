import base64
import base64
import os
import cv2
import numpy as np
from django.core.files.base import ContentFile


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


def base64_decode(data):
    format, imgstr = data.split(';base64,')
    return imgstr.decode('base64')


def base64_encode(data):
    if data:
        return 'data:image/png;base64,' + data

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(';base64,')[1]
    arr = base64.b64decode(encoded_data)
    nparr = np.fromstring(arr, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def extract_images_from_videos(obj_id,db_path, video_file):
    obj_id = str(obj_id)

    train_folder = os.path.join(db_path,obj_id)
    if obj_id not in os.listdir(db_path):
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
    fps = vidcap.get(cv2.CAP_PROP_FPS)  # This is frame per second
    print("fps: ", fps)
    after_n_frame = int(every_n_frame * fps)
    success, image = vidcap.read()
    count = 0
    counter = 0
    while success:
        if count % after_n_frame == 0:
            cv2.imwrite(os.path.join(train_folder, "frame%d.jpg") % count, image)
            counter += 1
        success, image = vidcap.read()
        count += 1

    return train_folder