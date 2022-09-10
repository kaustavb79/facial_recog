from django.urls import path
from . import views

app_name = 'app_recognition'

urlpatterns = [
    path('image/', views.ImageFaceDetect.as_view(), name='image'),
    path('live/', views.LiveVideoFaceDetect.as_view(), name='live'),
]
