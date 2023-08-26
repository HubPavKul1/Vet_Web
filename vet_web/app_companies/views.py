from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from pytils.translit import slugify  # для формирования слага из кириллицы
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import *
from .forms import *
from app_animals.models import Animal
from app_animals.forms import CreateAnimalForm
from utils.controllers import UploadAnimals


class CompaniesListView(LoginRequiredMixin, ListView):
    model = Company
    context_object_name = 'companies'
    template_name = 'app_companies/companies.html'
    extra_context = {'title': 'Предприятия',
                     'header': 'Предприятия'
                     }


class CreateCompanyView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CreateCompanyForm
    template_name = 'app_companies/add_company.html'
    extra_context = {'title': 'Добавить предприятие',
                     'header': 'Добавить предприятие'
                     }
    raise_exception = True

    # success_url = reverse_lazy('companies')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.short_name)
        self.object.save()
        messages.success(self.request, "Предприятие успешно создано")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('company_detail', kwargs={'slug': self.object.slug})


class CompanyDetailView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'app_companies/company_detail.html'
    model = Company
    context_object_name = 'company'
    form_class = CreateAnimalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animals = (Animal.objects.select_related('company', 'animal_group', 'species', 'type_of_use', 'sex').
                   filter(company__slug=self.object.slug, available=True))
        employees = (Employee.objects.select_related('company', 'position').
                     filter(company__slug=self.object.slug, available=True).first())
        context['animals'] = animals
        context['employees'] = employees
        return context

    def post(self, request, *args, **kwargs):
        create_animal_form = self.get_form()
        if create_animal_form.is_valid():
            return self.form_valid(create_animal_form)
        else:
            return self.form_invalid(create_animal_form)

    def form_valid(self, form):
        new_animal = form.save(commit=False)
        company = self.get_object()
        new_animal.company = company
        new_animal.save()
        messages.success(self.request, ('Животное успешно добавлено!'))
        return redirect('company_detail', slug=company.slug)


def delete_animal(request, slug):
    """Функция удаления животного из детальной страницы предприятия при помощи чекбокса"""
    if request.method == 'POST':
        animal_ids = request.POST.getlist('boxes')
        for item in animal_ids:
            Animal.objects.filter(id=int(item)).update(available=False)
        messages.success(request, ('Животное успешно удалено!'))
        return redirect('company_detail', slug=slug)
    else:
        return render(request, 'app_companies/company_detail.html')


def download_animals(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        file = request.FILES['file']
        uploading_file = UploadAnimals({'file': file})
        if uploading_file:
            messages.success(request, 'Успешная загрузка!')
        else:
            messages.error(request, 'Ошибка при загрузке!')
    # return render(request, 'app_companies/company_detail.html')
    return render(request, 'app_companies/companies')
