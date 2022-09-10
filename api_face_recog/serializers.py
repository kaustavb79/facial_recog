from random import choices
from rest_framework import serializers
from django.forms import ClearableFileInput

from .models import FaceRecogModel

class FaceRecogInferenceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceRecogModel
        fields = (
            'input_data',
        )


class FaceRecogTrainingModelSerializer(serializers.ModelSerializer):
    video_file = serializers.FileField(source="input_data")

    class Meta:
        model = FaceRecogModel
        fields = (
            'video_file',
            'name_of_person'
        )
