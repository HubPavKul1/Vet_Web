from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from pytils.translit import slugify
from django.contrib import messages

from .models import *
from .forms import *


class DrugOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'app_drugs/drug_order.html'


class DrugMovementDetailView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'app_drugs/drug_movement_detail.html'
    model = DrugMovement
    context_object_name = 'drug_movement'
    form_class = AddDrugsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drugs = (DrugInMovement.objects.select_related('drug_movement', 'drug', 'accounting_unit').
                 filter(drug_movement__slug=self.object.slug, available=True))
        context['drugs'] = drugs

        return context

    def post(self, request, *args, **kwargs):
        add_drug_form = self.get_form()
        if add_drug_form.is_valid():
            return self.form_valid(add_drug_form)
        else:
            return self.form_invalid(add_drug_form)

    def form_valid(self, form):
        new_drug = form.save(commit=False)
        drug_movement = self.get_object()
        new_drug.drug_movement = drug_movement
        new_drug.save()
        messages.success(self.request, ('Препарат успешно добавлен!'))
        return redirect('drug-movement', slug=drug_movement.slug)


class DrugMovementListView(LoginRequiredMixin, ListView):
    model = DrugMovement
    context_object_name = 'drug_movements'
    template_name = 'app_drugs/drug_movements.html'
    extra_context = {'title': 'Движение препаратов',
                     'header': 'Движение препаратов'
                     }


class CreateDrugReceiptView(LoginRequiredMixin, CreateView):
    model = DrugMovement
    form_class = CreateDrugMovementForm
    template_name = 'app_drugs/add_drugs.html'
    extra_context = {'title': 'Добавить поступление',
                     'header': 'Добавить поступление'
                     }
    raise_exception = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(f'{self.object.operation}_{self.object.operation_date}')
        self.object.save()
        messages.success(self.request, "Поступление успешно создано")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('drug-movement', kwargs={'slug': self.object.slug})





