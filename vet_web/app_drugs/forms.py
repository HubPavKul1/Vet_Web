from django.forms import ModelForm, TextInput, DateInput, FloatField
from .models import *
from django.forms.models import inlineformset_factory


# DrugMovementFormset = inlineformset_factory(models.DrugMovement, models.DrugInMovement, extra=1)


class CreateDrugMovementForm(ModelForm):
    class Meta:
        model = DrugMovement
        fields = ['operation_date', 'operation']
        widgets = {
            'operation_date': DateInput(attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd Дата поступления',
                'class': 'form-control'
                })
        }


class AddDrugsForm(ModelForm):
    class Meta:
        model = DrugInMovement
        fields = ['drug', 'batch', 'control',
                  'production_date', 'expiration_date', 'accounting_unit',
                  'packing', 'packs_amount', 'units_amount'
                  ]
        widgets = {
            'batch': TextInput(attrs={
                'class': 'form-control',
                'size': 10,
                'placeholder': 'Серия'
                }),
            'control': TextInput(attrs={
                'class': 'form-control',
                'size': 10,
                'placeholder': 'Контроль'
            }),
            'production_date': DateInput(attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd Дата изготовления',
                'class': 'form-control'
                }),
            'expiration_date': DateInput(attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd Срок годности',
                'class': 'form-control'
            }),
            'accounting_unit': TextInput(attrs={
                'class': 'form-control',
                'size': 10,
                'placeholder': 'Единицы учета'
                })
            # 'packing': FloatField(),
            # 'packs_amount': FloatField(),
            # 'units_amount': FloatField()
        }

