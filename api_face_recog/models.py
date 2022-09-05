from django.db import models
from django.db.models import JSONField
import uuid


def q_uuid_generate():
    return str(uuid.uuid4())

class UserDataModel(models.Model):
    user_id = models.CharField(max_length=512, primary_key=True, default=q_uuid_generate)
    status = models.CharField(max_length=20, blank=False, null=False, default="failure")
    is_valid = models.BooleanField(blank=True, null=True, default=False)
    message = models.CharField(max_length=512, blank=True, null=True)
    logs = JSONField(blank=True, null=True)
    input_data = models.FileField(blank=False, null=False, max_length=500)
    final_response_data = JSONField(blank=False, null=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "USER: %s" , self.user_id

    class Meta:
        ordering = ('-date_time',)