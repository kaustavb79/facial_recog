from django.contrib import admin

# Register your models here.
from .models import FaceRecogModel


class FaceRecogModelAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


admin.site.register(FaceRecogModel, FaceRecogModelAdminReadOnly)
