from rest_framework import serializers
from .models import UserDataModel


class UserDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDataModel
        fields = (
            'input_data',
            'final_response_data'
        )