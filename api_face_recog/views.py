import json
import logging as log
import os.path
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView

from api_face_recog.src.detect_face import get_face_detect_data
from api_face_recog.src.train_v1 import extract_images_from_videos, train
from .models import UserDataModel, q_uuid_generate
from .serializers import UserDataInferenceModelSerializer,UserDataTrainingModelSerializer
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
    queryset = UserDataModel.objects.all()
    serializer_class = UserDataInferenceModelSerializer

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
        print("API_URL: ",API_URL)
        print(request.data)
        id = q_uuid_generate()
        data = None
        status = "failure"
        message = "Invalid Data!!!"
        is_valid = False

        if request.data.get('input_data'):
            request_file = request.FILES['input_data']
            # file_path = str(request_file.temporary_file_path())
            filename = request_file.name
            fs = FileSystemStorage()
            file_path_without_media = fs.save("api_face_recog/" + filename, request_file)
            file_path = "media/" + file_path_without_media
            ext = os.path.splitext(file_path)[1].strip(".")
            try:
                data = get_face_detect_data(file_path)
            except:
                logger.exception("Exception occurred!!")
            else:
                if data:
                    message = "Face Recognised!!!"
                    status = "success"
                    is_valid = True
        else:
            message = "No file/data uploaded"
        json_response = {
            "response_id": id,
            "status": status,
            "message": message,
            'is_valid': is_valid,
            "data": data
        }
        return JsonResponse(json_response)



class FaceRecognitionTrainingViews(APIView):
    permission_classes = [AllowAny]
    queryset = UserDataModel.objects.all()
    serializer_class = UserDataTrainingModelSerializer

    def get(request, *args, **kwargs):
        # todos = UserDataModel.objects.filter()
        # serializer = UserDataTrainingModelSerializer(todos, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        json_response = {
            "ERROR": "invalid request",
        }
        return Response(json_response)

    def post(self, request):
        API_URL = request.api_url
        print("API_URL: ",API_URL)

        id = q_uuid_generate()
        status = "failure"
        message = "Invalid Data!!!"
        is_valid = False
        
        if request.data.get('video_file'):
            request_file = request.FILES['video_file']
            file_path = str(request_file.temporary_file_path())
            print(file_path,'----',type(file_path))
            metadata = request.data.get('metadata')
            role = request.data.get('role')
            if role:
                id = role+'_'+id
            log = {}
            try:
                data_path = extract_images_from_videos(id,file_path)
                train(data_path)
            except Exception as e:
                log['exception'] = str(e)
                logger.exception("Exception Occurred in Traing API!!!")
            else:
                status="success"
                is_valid = True
                message = role+" model training completed !!!"
                UserDataModel.objects.create(
                    user_id=id,
                    status=status,
                    is_valid=is_valid,
                    message=message,
                    logs = log,
                    input_data=file_path,
                    metadata=metadata
                )

        else:
            message = "No file/data uploaded"
        json_response = {
            "response_id": id,
            "status": status,
            "message": message,
            'is_valid': is_valid
        }
        return Response(json_response)