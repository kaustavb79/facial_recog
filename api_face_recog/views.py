import json
import logging as log
import os.path
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserDataModel, q_uuid_generate
from .serializers import UserDataModelSerializer


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
    serializer_class = UserDataModelSerializer

    def get(request, *args, **kwargs):
        # todos = UserDataModel.objects.filter()
        # serializer = UserDataModelSerializer(todos, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        json_response = {
            "ERROR": "invalid request",
        }
        return Response(json_response)

    def post(self, request):
        API_URL = request.api_url
        print("API_URL: ",API_URL)

        id = q_uuid_generate()
        data = None
        status = "failure"
        message = "Invalid Data!!!"
        is_valid = False

        if request.data.get('file'):
            request_file = request.FILES['file']
            print(request_file)
        else:
            message = "No file uploaded"
        json_response = {
            "response_id": id,
            "status": status,
            "message": message,
            'is_valid': is_valid,
            "data": data
        }
        return Response(json_response)