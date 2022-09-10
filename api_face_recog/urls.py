from django.urls import path
from . import views

app_name = 'api_face_recog'

urlpatterns = [
    path('inference/', views.FaceRecognitionInferenceViews.as_view(), name='inference'),
    path('train/', views.FaceRecognitionTrainingViews.as_view(), name='train'),
]
