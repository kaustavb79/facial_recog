import sys,os
import django
import base64
import os
import cv2
from django.conf import settings
from asgiref.sync import sync_to_async


FACE_RECOG_PROJ = os.getenv("FACE_RECOG_PROJ")
print("FACE_RECOG_PROJ : ", FACE_RECOG_PROJ)
sys.path.append(FACE_RECOG_PROJ)
os.environ['DJANGO_SETTINGS_MODULE'] = 'face_recog.settings'
django.setup()


from api_face_recog.models import FaceRecogModel
from api_face_recog.src.utils import data_uri_to_cv2_img
from api_face_recog.src.recognition_v2_deepface.inference import inference_image


async def get_name_from_model(pk):
    return FaceRecogModel.objects.get(pk=pk)

def get_live_face_recognition(image_base_64_data):
    img = data_uri_to_cv2_img(uri=image_base_64_data)
    folder_path = "media/app_recognition/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    cv2.imwrite(os.path.join(folder_path,"live_temp.jpg"),img)
    data = inference_image(os.path.join(folder_path,"live_temp.jpg"),"media/api_face_recog/training_db")
    if os.path.exists(os.path.join(folder_path,"live_temp.jpg")):
        os.remove(os.path.join(folder_path,"live_temp.jpg"))
    
    response_image_data = image_base_64_data
    if data:
        color = (255, 0, 0)  
        # Line thickness of 2 px
        thickness = 2                    
        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px
        for x in data:
            obj = get_name_from_model(pk=x['class'])

            class_name = "Unknown"
            if obj:
                class_name = obj.name_of_person
            img = cv2.rectangle(img, (x['bbox']['x_min'],x['bbox']['y_min']), (x['bbox']['x_max'],x['bbox']['y_max']), color, thickness)
            img = cv2.rectangle(img, (x['bbox']['x_min'],x['bbox']['y_max']-35), (x['bbox']['x_max'],x['bbox']['y_max']), color, thickness)
            img = cv2.putText(img,class_name, (x['bbox']['x_min']+6,x['bbox']['y_max']-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    response_image_data = jpg_as_text.decode('utf-8')
    
    return response_image_data