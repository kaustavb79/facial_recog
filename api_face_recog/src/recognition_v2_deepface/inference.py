from deepface import DeepFace
from api_face_recog.src.recognition_v2_deepface.inference_utils import find
from django.conf import settings
import cv2
import os,shutil

def inference_image(image_path,db_path):
    df,results = find(img_path = image_path,
        db_path = db_path, 
        model_name = settings.RECOGNIION_MODEL,
        detector_backend = settings.RECOGNIION_DETECTOR,
        distance_metric = settings.RECOGNIION_METRICS
    )
    return results

def inference_video(video_file_path,db_path):
    file_name = os.path.splitext(video_file_path)[0]
    if "\\" in video_file_path:
        video_folder = "/".join(video_file_path.split("\\")[:-1])
        file_name = file_name.split("\\")[-1]
    else:
        video_folder = "/".join(video_file_path.split("/")[:-1])
        file_name = file_name.split("/")[-1]

    temp_folder = os.path.join(video_folder,"temp_extract")
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    temp_folder = os.path.join(temp_folder,file_name)
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    
    faces_identified = []
    set_of_classes_identified = set()

    vidcap = cv2.VideoCapture(video_file_path)
    every_n_frame = 0.5
    fps = vidcap.get(cv2.CAP_PROP_FPS)  # This is frame per second
    print("fps: ", fps)
    after_n_frame = int(every_n_frame * fps)
    success, image = vidcap.read()
    count = 0
    counter = 0
    while success:
        if count % after_n_frame == 0:
            cv2.imwrite(os.path.join(temp_folder, "frame%d.jpg") % count, image)
            results = inference_image(image_path=os.path.join(temp_folder, "frame%d.jpg") % count, db_path=db_path)
            if results:
                for x in results:
                    if x['class'] not in set_of_classes_identified:
                        faces_identified.append(x)
                        set_of_classes_identified.add(x['class'])
            else:
                break
            counter += 1
        success, image = vidcap.read()
        count += 1

    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    
    return {"faces_identified":faces_identified,"set_of_classes_identified":list(set_of_classes_identified)}