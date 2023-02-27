from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from pytils.translit import slugify  # для формирования слага из кириллицы
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from .models import *
from .forms import *


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


class CompanyDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_companies/company_detail.html'
    model = Company
    context_object_name = 'company'










