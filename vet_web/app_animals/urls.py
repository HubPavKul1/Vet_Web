from django.urls import path
from .views import *

urlpatterns = [
    path('animal_del/<int:pk>', animal_delete, name='animal-del'),
]