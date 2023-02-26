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

# from .forms import RegisterUserForm


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация',
                     'header': 'Авторизация'
                     }


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'home'


# class RegisterView(SuccessMessageMixin, CreateView):
#     """ Регистрация пользователя """
#     model = User
#     template_name = 'app_users/register.html'
#     form_class = RegisterUserForm
#     success_message = 'You have successfully registered!'
#     extra_context = {'title': 'Регистрация',
#                      'header': 'Регистрация'
#                      }
#
#     def post(self, request, *args, **kwargs):
#         form = RegisterUserForm(request.POST, request.FILES)
#         if form.is_valid:
#             user = form.save()
#             Profile.objects.create(user=user)
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('home')
#         context = {'form': form}
#         return render(request, self.template_name, context)

