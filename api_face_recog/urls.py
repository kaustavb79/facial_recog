from django.urls import path
from . import views

app_name = 'api_face_recog'

urlpatterns = [
    path('', views.MedPrescriptionViews.as_view(), name='face_recog'),
]
