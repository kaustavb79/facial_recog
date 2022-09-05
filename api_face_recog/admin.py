from django.contrib import admin
from .models import UserDataModel


class UserDataModelAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)

admin.site.register(UserDataModel, UserDataModelAdminReadOnly)
