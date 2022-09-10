import base64
from django.http import JsonResponse
from django.views.generic import TemplateView
from app_recognition.src.calls import get_face_recognition_response
import os
import uuid

class ImageFaceDetect(TemplateView):
    template_name = 'image.html'

    def post(self, request, *args, **kwargs):
        data = request.POST.get('image')
        if data:
            if "media" not in os.listdir():
                os.mkdir("media")

            file_path = os.path.join('media','app_recognition')
            if not os.path.exists(file_path):
                os.mkdir(file_path)

            format, imgstr = data.split(';base64,') 

            file_path = file_path+"/blob_"+str(uuid.uuid4())[:10]+".jpg"
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(imgstr))
            try:                
                image_data = get_face_recognition_response(request,file_path)
                # print(image_data)
                if image_data:
                    return JsonResponse(status=200, data=image_data)
            except Exception as e:
                print(e)
        return JsonResponse(status=400, data={'errors': {'error_message': 'No face detected'}})


class LiveVideoFaceDetect(TemplateView):
    template_name = 'video.html'

    def post(self, request, *args, **kwargs):
        return JsonResponse(status=200, data={'message': 'Face detected'})