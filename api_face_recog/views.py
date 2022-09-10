import logging as log
import os.path
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework.views import APIView
from api_face_recog.src.utils import extract_images_from_videos
from api_face_recog.src.recognition_v2_deepface.train import train_recognition_model
from api_face_recog.src.recognition_v2_deepface.inference import inference_image, inference_video
from .models import q_uuid_generate, FaceRecogModel
from .serializers import FaceRecogInferenceModelSerializer, FaceRecogTrainingModelSerializer
from rest_framework.permissions import AllowAny


def setup_custom_logger(name):
    formatter = log.Formatter(fmt='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
    handler = log.StreamHandler()
    handler.setFormatter(formatter)
    logger = log.getLogger(name)
    logger.setLevel(log.INFO)
    logger.addHandler(handler)
    return logger


logger = setup_custom_logger("api_face_recog")


class FaceRecognitionInferenceViews(APIView):
    queryset = FaceRecogModel
    serializer_class = FaceRecogInferenceModelSerializer

    def get(request, *args, **kwargs):
        # todos = UserDataModel.objects.filter()
        # serializer = UserDataInferenceModelSerializer(todos, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        json_response = {
            "ERROR": "invalid request",
        }
        return Response(json_response)

    def post(self, request):
        API_URL = request.api_url
        print("API_URL: ", API_URL)
        # print(request.data)

        data = []
        status = "failure"
        message = "Invalid Data!!!"
        is_valid = False

        if request.data.get('input_data'):
            request_file = request.FILES['input_data']
            # file_path = str(request_file.temporary_file_path())
            filename = request_file.name

            fs = FileSystemStorage()

            file_path = "media/"
            if len(os.path.splitext(filename)) > 1:
                if os.path.splitext(filename)[1].strip('.') in ['jpg','jpeg','png']:
                    file_path_without_media = fs.save("api_face_recog/inference/image/" + filename, request_file)
                    file_path = "media/" + file_path_without_media
                elif os.path.splitext(filename)[1].strip('.') in ['mp4','webm','wmv','avi','flv','mkv']:
                    file_path_without_media = fs.save("api_face_recog/inference/video/" + filename, request_file)
                    file_path = "media/" + file_path_without_media
            else:
                file_path_without_media = fs.save("api_face_recog/inference/blob_video/" + filename, request_file)
                file_path = "media/" + file_path_without_media

            try:                
                db_path = "media/api_face_recog/training_db"                
                logger.info("DB_path selected --- %s",db_path)

                if "image" in file_path:
                    logger.info(" IMAGE INFERENCE STARTED ")
                    data = inference_image(file_path,db_path)                    
                    # print("\n Data Response: \n ")
                    # print(data,' ---- ',type(data))
                else:
                    logger.info(" VIDEO INFERENCE STARTED ")
                    data = inference_video(file_path,db_path)
            except Exception as e:
                logger.exception("Exception occurred!!")
            else:
                logger.info(" INFERENCE FINISHED ")
                if data:
                    message = "Face Recognised!!!"
                    status = "success"
                    is_valid = True
                else:
                    message = "No face recognised"
        else:
            message = "No file/data uploaded"
        json_response = {
            "status": status,
            "message": message,
            'is_valid': is_valid,
            "data": data
        }
        return Response(json_response)


class FaceRecognitionTrainingViews(APIView):
    permission_classes = [AllowAny]
    queryset = FaceRecogModel
    serializer_class = FaceRecogTrainingModelSerializer

    def get(request, *args, **kwargs):
        # todos = FaceRecogModel.objects.filter()
        # serializer = FaceRecogTrainingModelSerializer(todos, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        json_response = {
            "ERROR": "invalid request",
        }
        return Response(json_response)

    def post(self, request):
        API_URL = request.api_url
        print("API_URL: ", API_URL)

        id = q_uuid_generate()
        status = "failure"
        message = "Invalid Data!!!"
        is_valid = False
        log = {}

        # print("request.data: ", request.data)

        train_folder_path = ""
        file_path = None
        file_path_without_media = ""
        is_data_available = True
        if request.data.get('video_file'):
            request_file = request.FILES['video_file']
            # file_path = str(request_file.temporary_file_path())
            filename = request_file.name
            fs = FileSystemStorage()
            file_path_without_media = fs.save("api_face_recog/test_api/training_files/" + filename, request_file)
            file_path = "media/" + file_path_without_media

            # ext = os.path.splitext(file_path)[1].strip(".")
            logger.info("%s --- %s",file_path, file_path)
        else:
            message = "No file/data uploaded"
            is_data_available = False

        if is_data_available:
            try:
                if file_path:
                    db_path = "media/api_face_recog/"
                    if "extract_from_video_train" not in os.listdir(db_path):
                        os.mkdir(os.path.join(db_path,"extract_from_video_train"))
                    db_path = os.path.join(db_path,"extract_from_video_train")
                    train_folder_path = extract_images_from_videos(id,db_path,file_path)
                    train_folder_path = db_path

                response_data = train_recognition_model(train_folder_path)
                logger.info("TRAIN_FOLDER_PATH: %s",train_folder_path)
            except Exception as e:
                log['exception'] = str(e)
                logger.exception("Exception Occurred in Training API!!!")
                message = "Training failed!!!"
            else:
                logger.info("TRAINING COMPLETED")
                status = response_data['status']
                is_valid = response_data['is_valid']
                message = response_data['message']
                FaceRecogModel.objects.create(
                    user_id=id,
                    status=status,
                    is_valid=is_valid,
                    message=message,
                    logs=log,
                    input_data=file_path_without_media,
                    train_folder_path=train_folder_path,
                    name_of_person=request.data.get('name_of_person')
                )

        json_response = {
            "response_id": id,
            "status": status,
            "message": message,
            'is_valid': is_valid
        }
        return Response(json_response)
