from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import *


@admin.register(TypeOfUse)
class TypeOfUseAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeOfFeeding)
class TypeOfFeedingAdmin(admin.ModelAdmin):
    pass


@admin.register(AnimalGroup)
class AnimalGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    pass


@admin.register(AnimalSex)
class AnimalSexAdmin(admin.ModelAdmin):
    pass


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass