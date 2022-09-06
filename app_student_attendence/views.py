from django.http import JsonResponse
from django.views.generic import TemplateView
from app_student_attendence.src.calls import get_face_recognition_response


class ImageFaceDetect(TemplateView):
    template_name = 'image.html'

    def post(self, request, *args, **kwargs):
        data = request.POST.get('image')
        try:
            image_data = get_face_recognition_response(request,data)
            if image_data:
                return JsonResponse(status=200, data={'image': image_data, 'message': 'Face detected'})
        except Exception as e:
            print(e)
        return JsonResponse(status=400, data={'errors': {'error_message': 'No face detected'}})


class LiveVideoFaceDetect(TemplateView):
    template_name = 'video.html'

    def post(self, request, *args, **kwargs):
        return JsonResponse(status=200, data={'message': 'Face detected'})