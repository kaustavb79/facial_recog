from rest_framework import serializers
from .models import UserDataModel
from django.forms import ClearableFileInput

class UserDataInferenceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDataModel
        fields = (
            'input_data',
        )


class UserDataTrainingModelSerializer(serializers.ModelSerializer):
    video_file = serializers.FileField(source='input_data')
    role = serializers.CharField()
    class Meta:
        model = UserDataModel
        fields = (
            'video_file',
            'metadata',
            'role'
        )