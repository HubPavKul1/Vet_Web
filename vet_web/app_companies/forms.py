from django.forms import ModelForm, TextInput
from .models import *


class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['full_name', 'short_name']
        widgets = {
            'full_name': TextInput(attrs={
                'class': 'form-control',
                'size': 200,
                'placeholder': 'Полное наименование предприятия'
                }),
            'short_name': TextInput(attrs={
                'class': 'form-control',
                'size': 200,
                'placeholder': 'Краткое наименование предприятия'
                }),
        }


class UpdateCompanyForm(ModelForm):
    pass
