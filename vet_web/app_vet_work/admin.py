from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import *


# @admin.register(Disease)
# class DiseaseAdmin(admin.ModelAdmin):
#     pass
class DiseaseResource(resources.ModelResource):
    class Meta:
        model = Disease


@admin.register(Disease)
class DiseaseAdmin(ImportExportActionModelAdmin):
    resource_class = DiseaseResource
    list_display = [field.name for field in Disease._meta.fields if field.name != 'id']

