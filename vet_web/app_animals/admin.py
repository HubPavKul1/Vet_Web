from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import *
from .forms import UploadAnimalForm
from utils.controllers import UploadAnimals


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

    change_list_template = 'app_animals/animals_change.html'
    def import_animals(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = UploadAnimalForm()
            context = {
                'form': form
            }
            return render(request, 'admin/upload_animals.html', context)
        form = UploadAnimalForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/upload_animals.html', context, status=400)
        file = form.files['file'].file
        uploading_file = UploadAnimals({'file': file})
        if uploading_file:
            self.message_user(request, 'Успешная загрузка!')
            return redirect('..')
        else:
            self.message_user(request, 'Ошибка при загрузке!')
            context = {
                'form': form
            }
            return render(request, 'admin/upload_animals.html', context)



    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import_animals/', self.import_animals, name='import-animals'
            )
        ]
        return new_urls + urls