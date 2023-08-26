from django.forms import ModelForm, TextInput, Select, DateInput, Form, FileField
from .models import *


class CreateAnimalForm(ModelForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['animal_group'].empty_label = 'группа не выбрана'
        self.fields['species'].empty_label = 'вид не выбран'
        self.fields['type_of_use'].empty_label = 'тип использования не выбран'
        self.fields['sex'].empty_label = 'пол не выбран'

    class Meta:
        model = Animal
        fields = ['animal_group', 'species', 'type_of_use', 'sex', 'nickname', 'date_of_birth', 'identification']
        widgets = {
            # 'animal_group': Select(attrs={'style': 'min-height: 2em'}),
            # 'species': Select(attrs={'style': 'min-height: 2em'}),
            # 'type_of_use': Select(attrs={'style': 'min-height: 2em'}),
            # 'sex': Select(attrs={'style': 'min-height: 2em'}),
            'nickname': TextInput(attrs={
                'class': 'form-control',
                'size': 200,
                'placeholder': 'Кличка животного'
                }),
            'date_of_birth': DateInput(attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd Дата рождения',
                'class': 'form-control'
                }),
            'identification': TextInput(attrs={
                'class': 'form-control',
                'size': 20,
                'placeholder': 'Идентификация'
                })
        }


class UploadAnimalForm(Form):
    file = FileField()