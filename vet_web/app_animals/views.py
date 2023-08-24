from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *


def animal_delete(request, pk: int):
    animal = Animal.objects.get(pk=pk)
    company_slug = animal.company.slug
    if request.method == 'POST':
        animal.available = False
        animal.save()
        return redirect('companies')


