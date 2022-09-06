from django.urls import path
from . import views

app_name = 'api_face_recog'

urlpatterns = [
    path('detect_face/', views.FaceRecognitionInferenceViews.as_view(), name='face_recog'),
    path('train/', views.FaceRecognitionTrainingViews.as_view(), name='face_recog'),
]
