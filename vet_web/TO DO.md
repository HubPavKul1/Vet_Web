# Проект VET_WEB:
* создать гит-репозиторий для проекта 
* клонировать папку проекта из репозитория в пайчарм
```
git clone https://github.com/HubPavKul1/Vet_Web.git
```
* создать среду окружения в папке с проектом и активировать ее
```
python -m venv venv
venv\scripts\activate
```
* установить необходимые библиотеки:
```
(venv) Vet_Web> python -m pip install --upgrade pip
(venv) Vet_Web> pip install -r requirements.txt

Django==3.2.13
django-debug-toolbar==3.5.0
flake8-django==1.1.2
flake8-isort==4.1.1
Pillow==9.2.0
django-crispy-forms==1.14.0
django-modeltranslation==0.18.4
djangorestframework~=3.13.1
docutils==0.18.1
drf-yasg==1.20.0
psycopg2==2.9.3
environs==9.5.0
pytils==0.4.1
```
* Создать проект
```
(venv) Vet_Web> django-admin startproject vet_web
```
* В корне проекта разместить файл requirements.txt, .env, Readme.md
* В файл .env перенести из settings.py
```
SECRET KEY = ''

# переменные для настройки подключения к postgresql
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
```
* Создать базу данных vetweb_db на сервере postgresql 

подключиться к серверу по ssh ```sudo ssh -i sshfile username@ipserver```

подключиться к серверу postgres и создать базу данных
```
username@box-123456:~$ sudo su - postgres
postgres@box-123456:~$ psql 

postgres=# CREATE DATABASE vetweb_db;
postgres=# GRANT ALL PRIVILEGES ON DATABASE vetweb_db to username;
```
* В settings.py внести изменения:
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": "5432",
    }
}
```
* В корне проекта создать папки templates, static для размещения html шаблонов и статических файлов, в settings.py внести изменения:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # вместо []
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-STATIC_ROOT
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# DEBUG TOOLBAR
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```
* и изменить файл urls.py в директории vet_web
```
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

```
## Создать необходимые приложения 

### Пользователи (app_users)
```
python manage.py startapp app_users
```
добавить приложение в settings.py
```
INSTALLED_APPS = [
...
'app_users.apps.AppUsersConfig',

]
```

```
forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    """ Форма регистрации пользователя """
    username = forms.CharField(max_length=100,
                                 required=True,
                                 label='username',
                                 widget=forms.TextInput(attrs={'size': 100}))

    first_name = forms.CharField(max_length=100,
                                 required=False,
                                 label='first name',
                                 widget=forms.TextInput(attrs={'size': 100}))

    last_name = forms.CharField(max_length=100,
                                required=False,
                                label='last name',
                                widget=forms.TextInput(attrs={'size': 100}))

    password1 = forms.CharField(label='password', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(label='password repeat', widget=forms.PasswordInput)
    # user_photo = forms.ImageField(label='Фото')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

```
```
views.py

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, TemplateView

from .forms import RegisterUserForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация',
                     'header': 'Авторизация'
                     }


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'home'


class RegisterView(SuccessMessageMixin, CreateView):
    """ Регистрация пользователя """
    model = User
    template_name = 'app_users/register.html'
    form_class = RegisterUserForm
    success_message = 'You have successfully registered!'
    extra_context = {'title': 'Регистрация',
                     'header': 'Регистрация'
                     }

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid:
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {'form': form}
        return render(request, self.template_name, context)


```
создать в папке с приложением файл urls.py и добавить в него:
```
from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
]
```
в файл urls.py проекта внести изменения:
```
urlpatterns = [
                  path('admin/doc/', include('django.contrib.admindocs.urls')),
                  path('admin/', admin.site.urls),
                  path('', include('app_users.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
В папке templates создать файл login.html 

### Предприятия (app_companies)
```
python manage.py startapp app_companies
``` 
реализация животноводческих предприятий и ветклиник 
* Модели приложения: 
```
from django.db import models
from django.urls import reverse


class City(models.Model):
    """ Модель Город"""
    name = models.CharField(max_length=255, verbose_name='город', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class Street(models.Model):
    """ Модель Улица """
    city = models.ForeignKey(City,
                             verbose_name='город',
                             on_delete=models.CASCADE,
                             related_name='streets')
    name = models.CharField(max_length=255,
                            verbose_name='улица',
                            blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'streets'
        verbose_name = 'street'
        verbose_name_plural = 'streets'


class Company(models.Model):
    """ Модель Предприятие """
    full_name = models.CharField(max_length=255,
                                 verbose_name='полное наименование',
                                 blank=True)
    short_name = models.CharField(max_length=255,
                                  verbose_name='сокращенное наименование',
                                  blank=True)
    slug = models.SlugField(max_length=255,
                            verbose_name='url',
                            help_text='unique url fragment based on the company short_name'
                            )
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'companies'
        verbose_name = 'company'
        verbose_name_plural = 'companies'


class Address(models.Model):
    """ Модель адрес """
    street = models.ForeignKey(Street,
                               verbose_name='улица',
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='address')
    company = models.ForeignKey(Company,
                                verbose_name='предприятие',
                                null=True, on_delete=models.CASCADE,
                                related_name='address')
    house_number = models.CharField(max_length=10,
                                    verbose_name='номер дома',
                                    blank=True)
    phone_number_1 = models.CharField(max_length=12,
                                      verbose_name='телефон 1',
                                      blank=True)
    phone_number_2 = models.CharField(max_length=12,
                                      verbose_name='телефон 1',
                                      blank=True)

    def __str__(self):
        return f'{self.street}, {self.house_number}'

    class Meta:
        db_table = 'address'
        verbose_name = 'address'
        verbose_name_plural = 'address'


class Position(models.Model):
    """ Модель должность работника """
    name = models.CharField(max_length=100, verbose_name='должность', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'positions'
        verbose_name = 'position'
        verbose_name_plural = 'positions'


class Employee(models.Model):
    """ Модель сотрудник предприятия """
    company = models.ForeignKey(Company,
                                verbose_name='предприятие',
                                on_delete=models.CASCADE,
                                related_name='positions',
                                null=True
                                )
    position = models.ForeignKey(Position,
                                 verbose_name='должность',
                                 on_delete=models.CASCADE,
                                 related_name='employees')

    last_name = models.CharField(max_length=255,
                                 verbose_name='фамилия',
                                 blank=True)
    first_name = models.CharField(max_length=255,
                                  verbose_name='имя',
                                  blank=True)
    patronymic = models.CharField(max_length=255,
                                  verbose_name='отчество',
                                  blank=True)
    full_name = models.CharField(max_length=200, verbose_name='ФИО', blank=True)  # автозаполнение из предыдущих полей
    available = models.BooleanField(default=True)

    slug = models.SlugField(max_length=255,
                            verbose_name='url',
                            help_text='unique url fragment based on the employee full_name'
                            )

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'employees'
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

```



* app_animals ```python manage.py startapp app_animals```
* app_drugs ```python manage.py startapp app_drugs```



