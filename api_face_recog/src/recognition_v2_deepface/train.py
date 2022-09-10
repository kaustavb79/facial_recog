from api_face_recog.src.recognition_v2_deepface.train_utils import update_database
import os
from django.conf import settings
import glob,shutil
import logging

log = logging.getLogger("api_face_recog")

def train_recognition_model(classes_to_train_folder_path):
    status = "failure"
    message = ""
    is_valid = False
    db_path = "/".join(classes_to_train_folder_path.split('/')[:-1])
    if "to_be_trained" in classes_to_train_folder_path:
        if "student_data" not in os.listdir(db_path):
            db_path = os.path.join(db_path,"student_data")
            os.mkdir(db_path)
        else:            
            db_path = os.path.join(db_path,"student_data")
    elif "extract_from_video_train" in classes_to_train_folder_path:
        if "training_db" not in os.listdir(db_path):
            db_path = os.path.join(db_path,"training_db")
            os.mkdir(db_path)
        else:            
            db_path = os.path.join(db_path,"training_db")
    else:
        raise Exception("!!! --- INVALID PATH SPECIFIED: all files/folders for: \n attendence register should be under 'media/api_face_recog/attendence/to_be_trained' or for \n testing : 'media/api_face_recog/test_api/extract_from_video_train'---- !!!")
    
    print("db_path: ",db_path)
    for x in os.listdir(classes_to_train_folder_path):
        # COPY FILES TO DB PATH
        if not os.path.exists(os.path.join(db_path,x)):
            os.mkdir(os.path.join(db_path,x))
        for file in os.listdir(os.path.join(classes_to_train_folder_path,x)):
            shutil.copy(os.path.join(classes_to_train_folder_path,x,file),os.path.join(db_path,x,file),follow_symlinks=True)

        # start training
        try:
            update_database(db_path=os.path.join(db_path,x),trained_model_path = db_path,model_name=settings.RECOGNIION_MODEL,detector_backend=settings.RECOGNIION_DETECTOR,
            distance_metric = settings.RECOGNIION_METRICS)
        except Exception as e:
            log.exception("EXCEPTION OCCURRED during train!!! ")
            message = str(e)
        else:
            status = "success"
            message = "Model updated Successfully!!!"
            is_valid = True
    
    for f in glob.glob(os.path.join(classes_to_train_folder_path,'*')):
        shutil.rmtree(f)
    
    return {"status":status,"message":message,"is_valid":is_valid}
