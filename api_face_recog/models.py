from django.db import models
from django.db.models import JSONField
import uuid
from django.core.validators import FileExtensionValidator


def q_uuid_generate():
    return str(uuid.uuid4())


class FaceRecogModel(models.Model):
    user_id = models.CharField(max_length=512, primary_key=True, default=q_uuid_generate)
    status = models.CharField(max_length=20, blank=False, null=False, default="failure")
    is_valid = models.BooleanField(blank=True, null=True, default=False)
    message = models.CharField(max_length=512, blank=True, null=True)
    logs = JSONField(blank=True, null=True)
    input_data = models.FileField(blank=False, null=False, max_length=500, validators=[
        FileExtensionValidator(allowed_extensions=["mp4", "webm", "jpg", 'jpeg', "png"])])
    name_of_person = models.CharField(max_length=512, blank=True, null=True)
    train_folder_path = models.CharField(max_length=512, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + self.user_id

    class Meta:
        ordering = ('-date_time',)
