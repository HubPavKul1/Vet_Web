from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='home'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
]
