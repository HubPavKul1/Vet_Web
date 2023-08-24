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

Django==4.2.4
django-debug-toolbar==4.2.0
flake8-django==1.4
flake8-isort==6.0.0
Pillow==10.0.0
django-crispy-forms==2.0
crispy-bootstrap4==2022.1
django-modeltranslation==0.18.11
djangorestframework==3.14.0
docutils==0.20.1
drf-yasg==1.21.7
psycopg2-binary==2.9.7
environs==9.5.0
pytils==0.4.1
Pillow==10.0.0
django-import-export==3.2.0
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
* Добавить в INSTALLED_APPS необходимые библиотеки:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/admindocs/
    'django.contrib.admindocs',

    # сторонние библиотеки

    # https://django-crispy-forms.readthedocs.io/en/latest/install.html
    'crispy_forms',
    'crispy_bootstrap4',
    # https://www.django-rest-framework.org/
    'rest_framework',
    'pytils',
   
]
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
* app_users/forms.py
```python
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
* app_users/views.py
```python
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
* создать в папке с приложением файл app_users/urls.py и добавить в него:
```python
from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
]
```
* в файл vet_web/urls.py проекта внести изменения:
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
Реализация животноводческих предприятий и ветклиник 

добавить приложение в settings.py
```
INSTALLED_APPS = [
...
'app_users.apps.AppUsersConfig',
'app_companies.apps.AppCompaniesConfig'

]
```
* Модели приложения (app_companies/models.py): 
```python
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
* выполнить миграцию моделей в базу данных:
```
python manage.py makemigrations
python manage.py migrate
```
* зарегистрировать модели в админке:
файл app_companies/admin.py

```python
from django.contrib import admin

from .models import *


class StreetInline(admin.TabularInline):
    model = Street
    row_id_fields = ['city']
    extra = 0


class EmployeeInline(admin.TabularInline):
    model = Employee
    row_id_fields = ['position', 'company']
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address
    row_id_fields = ['street', 'company']
    extra = 0


# class PositionInline(admin.TabularInline):
#     model = Position
#     row_id_fields = ['company']
#     extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name", )}
    inlines = [EmployeeInline, AddressInline]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("full_name", )}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [StreetInline]


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = [EmployeeInline]
    extra = 0
```
* создадим формы добавления и обновления предприятия:

файл app_companies/forms.py
```python
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
```
* создадим представления для отображения на сайте:

файл app_companies/views.py
```python
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
```
* создадим файл app_companies/urls.py:
```python
from django.urls import path
from .views import *

urlpatterns = [
    path('companies/', CompaniesListView.as_view(), name='companies'),
    path('companies/add_company/', CreateCompanyView.as_view(), name='add_company'),
    path('companies/<str:slug>', CompanyDetailView.as_view(), name='company_detail'),
]
```
* в файл vet_web/urls.py проекта внести изменения:
```
urlpatterns = [
                  path('admin/doc/', include('django.contrib.admindocs.urls')),
                  path('admin/', admin.site.urls),
                  path('', include('app_users.urls')),
                  path('', include('app_companies.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
В папке templates/app_companies создадим шаблоны:
* companies.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% load static %}
{% block content %}
<div id="colorlib-services">
		<div class="container">
			<div class="row animate-box">
				<div class="col-md-6 col-md-offset-3 text-center colorlib-heading">
					<h2>Предприятия</h2>
					<p><a class="btn btn-primary btn-lg" href="{% url 'add_company' %}">Добавить предприятие</a>
                                    </p>
				</div>
			</div>
			<div class="row">
				{% if companies %}
				{% if companies|length > 1 %}
				{% for company in companies %}
				<div class="col-md-4 animate-box">
					<div class="services">
						<span class="icon">
							<i class="flaticon-healthy-1"></i>
						</span>
						<div class="desc">
							<h3><a href="{% url 'company_detail' company.slug %}">{{company.short_name}}</a></h3>
							<p>The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli</p>
						</div>
					</div>
				</div>
				{% endfor %}
				{% else %}
				<div class="col-md-4 animate-box">
					<div class="services">
						<span class="icon">
							<i class="flaticon-healthy-1"></i>
						</span>
						<div class="desc">
							<h3><a href="{% url 'company_detail' companies.first.slug %}">{{companies.first.short_name}}</a></h3>
							<p>The Big Oxmox advised her not to do so, because there were thousands of bad Commas</p>
						</div>
					</div>
				</div>
				{% endif %}
				{% endif %}

			</div>
		</div>
</div>
{% endblock %}
```
* company_detail.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% load static %}
{% block content %}

	<div id="colorlib-blog">
		<div class="container">
			<div class="row">
				<div class="col-md-8">
					<div class="blog-wrap">
						<div class="row">
							<div class="col-md-12">
								<img class="img-responsive" src="images/blog-3.jpg" alt=""><br>
							</div>
							<div class="col-md-12">
								<div class="blog-desc col-paddingbottom">
									<h2><a href="#">{{ company.full_name }}</a></h2>
									<div class="post-meta">
										<span><a href="#">Health</a></span>
										<span>01 Feb. 2017</span>
										<span><a href="blog-single.html">3 Comments</a></span>
									</div>
									<p>Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia.</p>
									<p>It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar.</p>
									<blockquote>
										The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way.
									</blockquote>
									<p>When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then</p>
								</div>
							</div>
							<div class="col-md-12">
								<div class="comment-area">
									<h2>3 Comments</h2>
									<div class="row">
										<div class="comment-wrap">
											<div class="col-sm-1">
												<div class="thumbnail">
													<img class="img-responsive user-photo" src="https://ssl.gstatic.com/accounts/ui/avatar_2x.png">
												</div><!-- /thumbnail -->
											</div><!-- /col-sm-1 -->
											<div class="col-sm-11">
												<div class="panel panel-default">
													<div class="panel-heading">
														<strong>Louie Master</strong> <span class="text-muted">commented 5 days ago</span>
													</div>
													<div class="panel-body">
														<p>Very Nice Template.. Any Wordpress Version?</p>
													</div><!-- /panel-body -->
												</div><!-- /panel panel-default -->
											</div><!-- /col-sm-5 -->
										</div>
										<div class="comment-wrap">
											<div class="col-sm-1">
												<div class="thumbnail">
													<img class="img-responsive user-photo" src="https://ssl.gstatic.com/accounts/ui/avatar_2x.png">
												</div><!-- /thumbnail -->
											</div><!-- /col-sm-1 -->
											<div class="col-sm-11">
												<div class="panel panel-default">
													<div class="panel-heading">
														<strong>Mike Smith</strong> <span class="text-muted">commented 5 days ago</span>
													</div>
													<div class="panel-body">
														<p>Very Nice Template.. Any Wordpress Version?</p>
													</div><!-- /panel-body -->
												</div><!-- /panel panel-default -->
											</div><!-- /col-sm-5 -->
										</div>
										<div class="comment-wrap">
											<div class="col-sm-1">
												<div class="thumbnail">
													<img class="img-responsive user-photo" src="https://ssl.gstatic.com/accounts/ui/avatar_2x.png">
												</div><!-- /thumbnail -->
											</div><!-- /col-sm-1 -->
											<div class="col-sm-11">
												<div class="panel panel-default">
													<div class="panel-heading">
														<strong>John Doe</strong> <span class="text-muted">commented 5 days ago</span>
													</div>
													<div class="panel-body">
														<p>Very Nice Template.. Any Wordpress Version?</p>
													</div><!-- /panel-body -->
												</div><!-- /panel panel-default -->
											</div><!-- /col-sm-5 -->
										</div>
									</div>
								</div>
							</div>

							<div class="col-md-12">
								<div class="comment-area">
									<h2>Leave a comment</h2>
									<form action="#">
										<div class="row form-group">
											<div class="col-md-6">
												<!-- <label for="fname">First Name</label> -->
												<input type="text" id="fname" class="form-control marginbottom" placeholder="Your firstname">
											</div>
											<div class="col-md-6">
												<!-- <label for="lname">Last Name</label> -->
												<input type="text" id="lname" class="form-control" placeholder="Your lastname">
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-12">
												<!-- <label for="email">Email</label> -->
												<input type="text" id="email" class="form-control" placeholder="Your email address">
											</div>
										</div>

										<div class="row form-group">
											<div class="col-md-12">
												<!-- <label for="message">Message</label> -->
												<textarea name="message" id="message" cols="30" rows="10" class="form-control" placeholder="Say something about us"></textarea>
											</div>
										</div>
										<div class="form-group">
											<input type="submit" value="Post Comment" class="btn btn-primary">
										</div>

									</form>	
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-md-4">
					<aside class="sidebar">
						<div class="side">
							<h2>Categories</h2>
							<ul class="list">
								<li><a href="#">Inspirational <i class="icon-check"></i> <span class="badge badge-default badge-pill">7</span></a></li>
								<li><a href="#">Medicines <i class="icon-check"></i> <span class="badge badge-default badge-pill">9</span></a></li>
								<li><a href="#">Operational <i class="icon-check"></i> <span class="badge badge-default badge-pill">10</span></a></li>
								<li><a href="#">Laboratories <i class="icon-check"></i> <span class="badge badge-default badge-pill">12</span></a></li>
							</ul>
						</div>

						<div class="side">
							<h2>Recent Posts</h2>
							<div class="post">
								<a href="blog.html">
									<div class="blog-img" style="background-image: url(images/blog-1.jpg);"></div>
									<div class="desc">
										<span>01 Feb. 2017</span>
										<h3>Far far away, behind the word mountains, far from the countries</h3>
									</div>
								</a>
							</div>
							<div class="post">
								<a href="blog.html">
									<div class="blog-img" style="background-image: url(images/blog-2.jpg);"></div>
									<div class="desc">
										<span>01 Feb. 2017</span>
										<h3>Far far away, behind the word mountains, far from the countries</h3>
									</div>
								</a>
							</div>
							<div class="post">
								<a href="blog.html">
									<div class="blog-img" style="background-image: url(images/blog-3.jpg);"></div>
									<div class="desc">
										<span>01 Feb. 2017</span>
										<h3>Far far away, behind the word mountains, far from the countries</h3>
									</div>
								</a>
							</div>
						</div>
						<div class="side">
							<h2><span>Para</span>graph</h2>
							<p>The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen.</p>
						</div>
					</aside>
				</div>
			</div>
		</div>
	</div>
{% endblock %}
```
* add_company.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% load static %}
{% block content %}

<div class="container">
    <div class="row">
        <div class="col-md-10 col-md-offset-1 animate-box">
            <h3>Регистрация Предприятия</h3>
                <form method="post">
                    {% csrf_token %}
                    {{ form.full_name }} <br>
                    {{ form.short_name}} <br>
                    <div class="form-group text-center">
                        <input type="submit" value="Зарегистрировать" class="btn btn-primary">
                    </div>
                </form>
        </div>
    </div>
</div>
{% if form.errors %}
<p>{{ form.errors.error }}</p>
{% endif %}
{% endblock %}
```
## Биопрепараты (app_drugs)
Реализация учета биопрепаратов в клинике

```
python manage.py startapp app_drugs
```
* Зарегистрируем приложение в vet_web/settings.py
```
INSTALLED_APPS = [
...
'app_users.apps.AppUsersConfig',
'app_companies.apps.AppCompaniesConfig',
'app_drugs.apps.AppDrugsConfig',

]
```
* Модели приложения (app_drugs/models.py)
```python
from django.db import models
from datetime import datetime

from app_vet_work.models import Disease


class DrugManufacturer(models.Model):
    """Модель Производитель препарата"""
    name = models.CharField(max_length=255,
                            verbose_name='производитель препарата',
                            blank=True
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'drug_manufacturers'
        verbose_name = 'drug_manufacturer'
        verbose_name_plural = 'drug_manufacturers'


class AccountingUnit(models.Model):
    """Модель Единица учета препарата"""
    name = models.CharField(max_length=30,
                            verbose_name='единица учета',
                            blank=True
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'accounting_units'
        verbose_name = 'accounting_unit'
        verbose_name_plural = 'accounting_units'


class Dosage(models.Model):
    """Модель Дозировка препарата"""
    dosage = models.TextField(verbose_name='дозировка препарата', blank=True)

    def __str__(self):
        return self.dosage

    class Meta:
        db_table = 'dosages'
        verbose_name = 'dosage'
        verbose_name_plural = 'dosages'


class AdministrationMethod(models.Model):
    """Модель Способ применения препарата"""
    name = models.CharField(max_length=20,
                            verbose_name='способ применения'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'administration_methods'
        verbose_name = 'administration_method'
        verbose_name_plural = 'administration_methods'


class PlaceOfAdministration(models.Model):
    """Модель Место введения препарата"""
    place = models.CharField(max_length=255,
                             verbose_name='место введения препарата',
                             blank=True
                             )

    def __str__(self):
        return self.place

    class Meta:
        db_table = 'place_of_administration'
        verbose_name = 'place_of_administration'
        verbose_name_plural = 'place_of_administration'


class Drug(models.Model):
    """Модель Препарат"""

    class Budget(models.TextChoices):
        Federal = 'Fed'
        Regional = 'Reg'
        Commercial = 'Com'

    disease = models.ForeignKey(Disease,
                                verbose_name='заболевание',
                                on_delete=models.CASCADE,
                                related_name='drugs',
                                help_text='ссылка на заболевание'
                                )
    name = models.CharField(max_length=255,
                            verbose_name='наименование препарата'
                            )
    drug_manufacturer = models.ForeignKey(DrugManufacturer,
                                          verbose_name='производитель препарата',
                                          on_delete=models.CASCADE,
                                          related_name='drugs',
                                          help_text='ссылка на производителя препарата'
                                          )
    budget = models.CharField(max_length=3,
                              choices=Budget.choices,
                              default=Budget.Federal
                              )
    image = models.ImageField(upload_to='drugs/images/')
    instruction = models.FileField(verbose_name='инструкция к препарату',
                                   upload_to='drugs/'
                                   )

    def __str__(self):
        return self.name


class DrugMovement(models.Model):
    class Operation(models.TextChoices):
        Receipt = 'поступление'
        Expense = 'расход'
        Destruction = 'уничтожение'

    operation = models.CharField(max_length=20,
                                 choices=Operation.choices,
                                 verbose_name='операция'
                                 )
    operation_date = models.DateField(verbose_name='дата операции',
                                      null=True,
                                      blank=True
                                      )


class DrugInMovement(models.Model):
    """Модель Перемещаемый препарат"""
    drug_movement = models.ForeignKey(DrugMovement,
                                      verbose_name='вид перемещения',
                                      on_delete=models.CASCADE,
                                      related_name='drug_in_movement'
                                      )
    drug = models.ForeignKey(Drug,
                             verbose_name='препарат',
                             on_delete=models.CASCADE,
                             blank=True,
                             related_name='drug_in_movement',
                             help_text='ссылка на модель препарат'
                             )

    batch = models.CharField(max_length=10,
                             verbose_name='серия',
                             blank=True
                             )
    control = models.CharField(max_length=10,
                               verbose_name='контроль',
                               blank=True
                               )
    production_date = models.DateField(verbose_name='дата выпуска',
                                       null=True,
                                       blank=True
                                       )
    expiration_date = models.DateField(verbose_name='срок годности',
                                       null=True,
                                       blank=True
                                       )
    accounting_unit = models.ForeignKey(AccountingUnit,
                                        verbose_name='единицы учета',
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True,
                                        related_name='drug_in_movement'
                                        )
    packing = models.FloatField(verbose_name='фасовка',
                                null=True,
                                help_text='количество единиц учета в единице упаковки'
                                )
    packs_amount = models.PositiveSmallIntegerField(verbose_name='количество упаковок',
                                                    null=True
                                                    )
    units_amount = models.FloatField(verbose_name='количество единиц учета',
                                     null=True
                                     )
    available = models.BooleanField(verbose_name='в наличии',
                                    default=True
                                    )

    def __str__(self):
        return f'{self.drug.name} серия:{self.batch}'

    def is_expired(self) -> bool:
        current_date = datetime.today().date()
        if current_date > self.expiration_date:
            return False
        return True
```
* выполним миграции
```
python manage.py makemigrations
python manage.py migrate
```
* зарегистрируем модели в админке:
```python
from django.contrib import admin
from .models import *


class DrugInMovementInline(admin.TabularInline):
    model = DrugInMovement
    row_id_fields = ['drug']
    extra = 0


@admin.register(DrugManufacturer)
class DrugManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountingUnit)
class AccountingUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Dosage)
class DosageAdmin(admin.ModelAdmin):
    pass


@admin.register(AdministrationMethod)
class AdministrationMethod(admin.ModelAdmin):
    pass


@admin.register(PlaceOfAdministration)
class PlaceOfAdministration(admin.ModelAdmin):
    pass


@admin.register(DrugMovement)
class DrugMovement(admin.ModelAdmin):
    inlines = [DrugInMovementInline]


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    pass


@admin.register(DrugInMovement)
class DrugInMovementAdmin(admin.ModelAdmin):
    pass
```

## Ветеринарная работа (app_vet_work) 
Реализация работы ветврача
```
python manage.py startapp app_vet_work
```
* зарегистрируем приложение в vet_web/settings.py:
```
INSTALLED_APPS = [
...
'app_users.apps.AppUsersConfig',
'app_companies.apps.AppCompaniesConfig',
'app_drugs.apps.AppDrugsConfig',
'app_vet_work.apps.AppVetWorkConfig,

]
```
* Добавим необходимые модели:
```python
from django.db import models


class Disease(models.Model):
    """Модель Заболевание"""
    name = models.CharField(max_length=255,
                            verbose_name='наименование болезни'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'diseases'
        verbose_name = 'disease'
        verbose_name_plural = 'diseases'

```
* Зарегистрируем модели в админке:
```python
from django.contrib import admin


from .models import *


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    pass
```
## Реализация возможности импортировать в базу данные из excel
* Устанавливаем необходимую библиотеку:
```
pip install django-import-export
```
* Добавляем приложение в vet_web/settings.py
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_users.apps.AppUsersConfig',
    'app_companies.apps.AppCompaniesConfig',
    'app_drugs.apps.AppDrugsConfig',
    'app_vet_work.apps.AppVetWorkConfig',

    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/admindocs/
    'django.contrib.admindocs',

    # сторонние библиотеки

    # https://django-crispy-forms.readthedocs.io/en/latest/install.html
    'crispy_forms',
    'crispy_bootstrap4',
    # https://www.django-rest-framework.org/
    'rest_framework',
    'pytils',
    # https://django-import-export.readthedocs.io/en/latest/
    'import_export',

]
```
* выполним команду:
```
python manage.py collectstatic
```
* Внесем изменения в app_vet_work/admin.py
```python
from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import *


# @admin.register(Disease)
# class DiseaseAdmin(admin.ModelAdmin):
#     pass
class DiseaseResource(resources.ModelResource):
    class Meta:
        model = Disease


@admin.register(Disease)
class DiseaseAdmin(ImportExportActionModelAdmin):
    resource_class = DiseaseResource
    list_display = [field.name for field in Disease._meta.fields if field.name != 'id']
```

*app_animals ```python manage.py startapp app_animals```