from django.urls import path
from .views import *

urlpatterns = [
    path('companies/', CompaniesListView.as_view(), name='companies'),
    path('companies/add_company/', CreateCompanyView.as_view(), name='add_company'),
    path('companies/<slug:slug>/', CompanyDetailView.as_view(), name='company_detail'),
    path('del_animal/<slug:slug>/', delete_animal, name='del-animal')
]