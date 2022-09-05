from django.urls import path
from . import views

app_name = 'app_student_attendence'

urlpatterns = [
    path('^student/image', views.ImageFaceDetect.as_views(), name='student'),
    path('^student/live', views.LiveVideoFaceDetect.as_views(), name='student'),
]
